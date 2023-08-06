import pytest
import uqpylab.sessions as uq_session
#from uqlab_standalone import sessions as uq_session
import numpy as np


def test_input_aux_funs(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    iOptsTrue = {
        'Marginals': [
            {
                'Type': 'Gaussian',
                'Parameters': [-1,1]
            },
            {
                'Type': 'Exponential',
                'Parameters': [1]
            },
            {
                'Type': 'Uniform',
                'Parameters': [-1,3]
            }
        ]
    }
    myInputTrue = uq.createInput(iOptsTrue)

    X = uq.getSample(myInputTrue,200)

    iOpts = {
        'Inference': 
            {
                'Data': X.tolist()
            },
    }
    iOpts['Copula'] = {
        'Type': 'auto',
        'Inference': {
            'BlockIndepTest': {
                'Alpha': 0.05
            }
        },
        'Parameters': []
    }
    InputHat1c = uq.createInput(iOpts)
    
    # make sure that the session is properly terminated (no dangling background stuff)
    assert X.shape == (200,3)

def test_marginal_funs(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    iOptsTrue = {       
        'Marginals': [
            {
                'Type': 'Gaussian',
                'Parameters': [-1,1]
            },
            {
                'Type': 'Exponential',
                'Parameters': [1]
            },
            {
                'Type': 'Uniform',
                'Parameters': [-1,3]
            }
        ]
    }

    myInputTrue = uq.createInput(iOptsTrue)

    X = uq.getSample(myInputTrue,200, response_format='JSON')
    U = uq.all_cdf(X, myInputTrue['Marginals'], request_format='JSON', response_format='JSON')
    assert X.shape == U.shape

def enrichSampling(request, helpers, SamplingType, FunctionName):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')    

    Input = {"Marginals": [uq.Marginals(1, "Gaussian", [2, .5])]+
                          [uq.Marginals(1, "Gaussian", [1, 1])]}
    myInput = uq.createInput(Input)

    X = uq.getSample(myInput, 100, SamplingType)   
    numEnr = 50
    # one output argument
    XX = eval(FunctionName+"(X0=X, N=numEnr)")
    assert XX.shape == (numEnr,2)
    # two output arguments
    X, U = eval(FunctionName+"(X0=X, N=numEnr, nargout=2)")
    assert X.shape == (numEnr,2)
    assert U.shape == (numEnr,2)

def test_enrichLHS(request, helpers):
    enrichSampling(request, helpers, 'LHS', 'uq.enrichLHS')
def test_enrichSobol(request, helpers):
    enrichSampling(request, helpers, 'Sobol', 'uq.enrichSobol')
def test_enrichHalton(request, helpers):
    enrichSampling(request, helpers, 'Halton', 'uq.enrichHalton')
def test_LHSify(request, helpers):
    enrichSampling(request, helpers, 'MC', 'uq.LHSify')

def test_appendVariables(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    iOpts = {"Marginals": uq.StdNormalMarginals(2)}
    myInput = uq.createInput(iOpts)
    X = uq.getSample(myInput, 200)
    assert X.shape == (200,2)
    iOpts['Marginals'].extend(uq.StdNormalMarginals(1))
    myInput = uq.createInput(iOpts)
    X = uq.getSample(myInput, 200)
    assert X.shape == (200,3)

def test_CopulaSummary(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    # Marginals - 2 random variables
    iOpts = {"Marginals": uq.StdNormalMarginals(2)}
    myInput = uq.createInput(iOpts)
    msg = uq.CopulaSummary(myInput['Copula'], no_print=True)
    assert msg is not None
    # Pair copula
    iOpts['Copula'] = {
        'Type': 'Pair',
        'Family': 'Clayton',
        'Rotation': 90,
        'Parameters': 1.5
    }
    myInput = uq.createInput(iOpts)
    msg = uq.CopulaSummary(myInput['Copula'], no_print=True)
    assert msg is not None
    # Marginals - 3 random variables
    iOpts = {'Marginals': uq.StdNormalMarginals(2) + 
                          [uq.Marginals(1, 'Exponential', [1.5])]}
    # Gaussian copula
    iOpts['Copula'] = uq.GaussianCopula([[1, .5, -.3], [.5, 1, .2],[-.3, .2, 1]], 'Linear')
    myInput = uq.createInput(iOpts)
    msg = uq.CopulaSummary(myInput['Copula'], no_print=True)
    
    # #TODO: Vine copula
    # iOpts['Copula'] = uq.VineCopula('Cvine', [2,1,3],['Gumbel', 'Gaussian', 'Frank'],[1.5, -0.4, [0.3]])          
    # msg = uq.CopulaSummary(iOpts['Copula'], no_print=True)
    # myInput = uq.createInput(iOpts)
    # msg = uq.CopulaSummary(myInput['Copula'], no_print=True)
    # assert msg is not None

def test_ConstantVariables(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    Input = {
        'Marginals': [
            {
                'Type': 'Gaussian',
                'Parameters': [0,1],
                'Bounds': [0,0]
            },   
            {
                'Type': 'Gaussian',
                'Parameters': [1, 0]
            },        
            {
                'Type': 'Constant',
                'Parameters': [2]
            }
        ]
    }
    myInput = uq.createInput(Input)
    X = uq.getSample(myInput, 1)
    assert (X == np.array([0,1,2])).all()

def test_estimateMoments(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    Input = {
        'Marginals': 
            {
                'Type': 'Lognormal',
                'Parameters': [2, 0.5]
            }
    }
    moments = uq.estimateMoments(Input['Marginals'])   
    assert abs(moments[0]-np.exp(2+.5**2/2)) < 1e-5
    assert abs(moments[1]-((np.exp(.5**2)-1)*np.exp(2*2+.5**2))**.5) < 1e-5

def test_Transforms(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')    

    # 2D Gaussian Independent variables and Gaussian copula
    Input1 = {
        'Marginals': [uq.Marginals(1, 'Gaussian', [1,1])]+ 
                        [uq.Marginals(1, 'Gaussian', [2,.5])],
        'Copula': {
            'Type': 'Gaussian',
            'Parameters': [[1, 0.8],[0.8, 1]] 
        }
    }
    myInput1 = uq.createInput(Input1)

    # 2D Standard normal independent variables 
    Input2 = {
        'Marginals': uq.StdNormalMarginals(2),
        'Copula'   :  {'Type': 'Independent'}
    }

    # 2D Standard uniform independent variables
    Input3 = {"Marginals": uq.StdUniformMarginals(2)}

    X = uq.getSample(myInput1, 100)
    assert X.shape == (100, 2)

    ## General isoprobabilistic transform
    U = uq.GeneralIsopTransform(X, 
            Input1['Marginals'], Input1['Copula'], 
            Input2['Marginals'], Input2['Copula'])  
    assert U.shape == (100, 2)

    ## Isoprobabilistic transform
    V = uq.IsopTransform(X, Input2['Marginals'], Input3['Marginals'])
    assert V.shape == (100, 2)

    ## Nataf transform
    Unew = uq.NatafTransform(X, Input1['Marginals'], Input1['Copula'])
    assert Unew.shape == (100, 2)

    ## Inverse Nataf transform
    Xnew = uq.invNatafTransform(U, Input1['Marginals'], Input1['Copula'])
    assert Xnew.shape == (100, 2)

    ## Rosenblatt transform
    Vnew = uq.RosenblattTransform(X, Input1['Marginals'], Input1['Copula'])    
    assert Vnew.shape == (100, 2)

    ## Inverse Rosenblatt transform
    Xnew2 = uq.invRosenblattTransform(V, Input1['Marginals'], Input1['Copula'])
    assert Xnew2.shape == (100, 2)

def test_MarginalFields(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    Input = {
        'Marginals':  [
            {'Type': 'Constant',    'Parameters': [1]},
            {'Type': 'Gaussian',    'Parameters': [2, 0.5]},
            {'Type': 'Lognormal',   'Parameters': [0, .1]},
            {'Type': 'Uniform',     'Parameters': [-.5, .5]},
            {'Type': 'Exponential', 'Parameters': [1.5]},
            {'Type': 'Beta',        'Parameters': [.8, .2, .5, 1.5]},
            {'Type': 'Weibull',     'Parameters': [1.5, 1]},
            {'Type': 'Gumbel',      'Parameters': [0, .2]},
            {'Type': 'GumbelMin',   'Parameters': [0, .2]},
            {'Type': 'Gamma',       'Parameters': [1, 1]},
            {'Type': 'Triangular',  'Parameters': [0, 2, 1]},
            {'Type': 'Logistic',    'Parameters': [5, 2]},
            {'Type': 'Laplace',     'Parameters': [0, 1]},
            {'Type': 'Rayleigh',    'Parameters': [1]},
        ]
    }

    marginals = uq.MarginalFields(Input['Marginals'])
    Moments = [marginal['Moments'] for marginal in marginals]
    MomentsUQLab = np.array([
        [1,	0],
        [2,	0.5], 
        [1.00501252085940,	0.100753029446204], 
        [0,	0.288675134594813], 
        [0.666666666666667,	0.666666666666667],
        [1.3,	0.282842712474619],
        [1.5,	1.5],
        [0.115443132980306,	0.256509966032373],
        [-0.115443132980306,	0.256509966032373],
        [1,	1],
        [1,	0.408248290463863],
        [5,	3.62759872846844], 
        [0,	1.41421356237310],
        [1.25331413731550,	0.655136377562034]])

    assert (abs(Moments - MomentsUQLab) < 1e-5).all()

def test_Copulas(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    iOpts = {
        "Marginals" : uq.StdNormalMarginals(2),
        "Copula":  uq.PairCopula('Gumbel', 1.5)
    }
    myInput = uq.createInput(iOpts)
    X = uq.getSample(myInput,50)
    assert X.shape == (50,2)

    iOpts = {
        "Marginals": uq.StdNormalMarginals(2) +
                    [uq.Marginals(1, 'Exponential', [1.5])],
        "Copula": uq.VineCopula('Cvine', [2,1,3],['t', 'Frank', 'Independence'],[[.4, 2], .5, []])
    }

    myInput = uq.createInput(iOpts)
    X = uq.getSample(myInput,50)
    assert X.shape == (50,3)

def test_PairCopulaParameterRange(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    families = ['Gaussian', 'Clayton', 'Gumbel', 'Frank', 't'] # 'Independent', and 'Independence' families have no parameters
    for family in families:
        R = uq.PairCopulaParameterRange(family)
        assert R     

def test_sampleU(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    U = uq.sampleU(30,3)
    assert U.shape == (30,3)
    options = {'Method': 'LHS','LHSiterations': 2}
    U = uq.sampleU(30,3,options)
    assert U.shape == (30,3)
    options = {'Method': 'Sobol'}
    U = uq.sampleU(30,3,options)
    assert U.shape == (30,3)

def test_setDefaultSampling(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    Input = {"Marginals": uq.Marginals(2, "Gaussian", [0,1])}
    myInput = uq.createInput(Input)    
    success = uq.setDefaultSampling(myInput, 'LHS')
    assert success == 1
    assert uq.getInput(myInput['Name'])['Sampling']['DefaultMethod'] == 'LHS'

def test_subsample(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    Input = {
        "Marginals": [uq.Marginals(1, "Gaussian", [2, .5])]+
                     [uq.Marginals(1, "Gaussian", [1, 1])]}
    myInput = uq.createInput(Input)
    X = uq.getSample(myInput, N = 100, Method = 'LHS')
    Xnew, idx = uq.subsample(X, NK=20, Method='kmeans', Name='Distance_nn', Value='euclidean', nargout=2)
    assert Xnew.shape == (20,2)
    assert idx.shape == (20,1)

def test_KernelMarginals(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    X = np.random.rand(10,3)
    Input = {"Marginals": uq.KernelMarginals(X)}
    myInput = uq.createInput(Input)
    X = uq.getSample(myInput, N=20)
    assert X.shape == (20,3)

def test_Inference(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # generate data
    iOptsTrue = {'Marginals': uq.StdNormalMarginals(1) + [uq.Marginals(1, "Beta", [6,4])]}
    iOptsTrue['Marginals'][0]['Bounds'] = [1,10]
    myInputTrue = uq.createInput(iOptsTrue)
    X = uq.getSample(myInputTrue,100)

    # inference of marginals
    InputOpts = {
        "Inference": {"Data": X.tolist()},
        "Marginals": [{"Type": "auto"} for i in range(2)],
    }
    # full inference with Kolmogorov-Smirnov selection criterion for the second input marginal
    InputOpts["Marginals"][1]["Inference"] = {"Criterion": 'KS'}
    InputHat1 = uq.createInput(InputOpts)
    X1 = uq.getSample(InputHat1,50)
    assert X1.shape == (50,2)
    # assign data to the second marginal and get samples
    InputOpts['Marginals'][1]['Inference']['Data'] = X[:,1].tolist()
    InputHat2 = uq.createInput(InputOpts)
    X2 = uq.getSample(InputHat2,50)
    assert X2.shape == (50,2)  
    # constrained set of marginal families
    InputOpts["Marginals"][0]["Type"] = ["Gaussian", "Exponential", "Weibull"]
    InputHat3 = uq.createInput(InputOpts)
    X3 = uq.getSample(InputHat3,50)  
    assert X3.shape == (50,2)    
    # full inference with truncated marginal
    InputOpts["Marginals"][0]["Bounds"] = [1, 10]
    InputHat4 = uq.createInput(InputOpts)
    X4 = uq.getSample(InputHat4,50)  
    assert X4.shape == (50,2)   
    InputOpts["Marginals"][0]["Bounds"] = [1, float('inf')]
    InputHat4a = uq.createInput(InputOpts)
    X4a = uq.getSample(InputHat4a,50)  
    assert X4a.shape == (50,2) 
    # parameter fitting of a fixed marginal family
    InputOpts["Marginals"][0]["Type"] = "Gaussian"
    InputOpts['Marginals'][0]['Parameters'] = [0,1]
    InputHat5 = uq.createInput(InputOpts)
    X5 = uq.getSample(InputHat5,50)  
    assert X5.shape == (50,2)
    # inference by kernel smoothing
    InputOpts["Marginals"][1]['Type'] =  "ks" 
    InputOpts["Marginals"][1]["Options"] = {
        "Kernel": "Epanechnikov", # Gaussian, Normal, Triangle, Triangular, Box, Epanechnikov
        # "Bandwidth": 0.1
    }
    InputHat6 = uq.createInput(InputOpts)
    X6 = uq.getSample(InputHat6,50)  
    assert X6.shape == (50,2)    
    # inference of selected marginals
    InputOpts["Marginals"][0] = {
        "Type": "Gaussian",
        "Parameters": [0, 1],
        "Bounds": [1,10]
    }
    InputHat7 = uq.createInput(InputOpts)
    X7 = uq.getSample(InputHat7,50)  
    assert X7.shape == (50,2)     
    # specification of inference options for each marginal
    del InputOpts
    InputOpts = {
        'Marginals': [
            {
                'Type': 'auto',
                'Inference': {
                    'Criterion': 'BIC',
                    'Data': X[:,0].tolist()
                }
            },
            {
                'Type': 'Beta',
                'Inference': {
                    'Data': X[:,1].tolist()
                }
            }
        ],
        
    }
    InputHat8 = uq.createInput(InputOpts)    
    X8 = uq.getSample(InputHat8,50)  
    assert X8.shape == (50,2)

def test_InferenceCopula(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # data generation
    iOptsTrue = {'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])] + [uq.Marginals(1, 'Uniform',[-1,3])]}
    iOptsTrue['Copula'] = {
        'Type': 'CVine',
        'Structure': [[3,1,2]],
        'Families': ['Gaussian', 'Gumbel', 't'],
        'Rotations': [0,90,0],
        'Parameters': [.4, 2, [-.2, 2]]
    }
    myInputTrue = uq.createInput(iOptsTrue)
    X = uq.getSample(myInputTrue,100)
    assert X.shape == (100,3)
    U = uq.all_cdf(X,myInputTrue['Marginals'])
    assert U.shape == (100,3)
    # Inference of marginals and copula
    iOpts = {'Inference': {'Data': X.tolist()}}
    InputHat1 = uq.createInput(iOpts)
    X1 = uq.getSample(InputHat1,100)
    assert X1.shape == (100,3)
    # Testing for block independence
    iOpts['Inference']['BlockIndepTest'] = {
        'Alpha': 0.05,
        'Type': 'Kendall', # Kendall, Spearman, Pearson
        'Correction': 'auto' # none, fdr, Bonferroni, auto
    }
    InputHat2a = uq.createInput(iOpts)
    X2a = uq.getSample(InputHat2a,100)
    assert X2a.shape == (100,3)
    # Turn the block independence test
    iOpts['Inference']['BlockIndepTest']['Alpha'] = 0
    InputHat2b = uq.createInput(iOpts)   
    X2b = uq.getSample(InputHat2b,100)
    assert X2b.shape == (100,3)
    # Block independence test options can be provided as copula inference options rather than general options
    iOpts['Copula'] = {
        'Type': 'auto',
        'Inference': {
            'BlockIndepTest':
            {
                'Alpha': 0.05
            }
        }
    }
    InputHat2c = uq.createInput(iOpts)
    X2c = uq.getSample(InputHat2c,100)
    assert X2c.shape == (100,3)
    # Specify data for copula inference
    iOpts['Copula']['Inference']['Data'] = X.tolist()
    InputHat3a = uq.createInput(iOpts)
    X3a = uq.getSample(InputHat3a,100)
    assert X3a.shape == (100,3)
    # Specify the data for data as pseudo-observations in [0,1]<sup>M</sup>
    del iOpts['Copula']['Inference']['Data']
    iOpts['Copula']['Inference']['DataU'] = U.tolist()
    InputHat3b = uq.createInput(iOpts)
    X3b = uq.getSample(InputHat3b,100)
    assert X3b.shape == (100,3)   
    # Inference among a selected list of copula types
    iOpts['Copula']['Type'] = ['DVine', 'CVine']
    InputHat4 = uq.createInput(iOpts)
    X4 = uq.getSample(InputHat4,100)
    assert X4.shape == (100,3)      
    # Testing for pair independence
    iOpts['Copula']['Inference'] = {
        'PairIndepTest': {
            'Type': 'Pearson', # Kendall, Spearman, Pearson
            'Alpha': 0.05
        }
    }
    InputHat5a = uq.createInput(iOpts)
    X5a = uq.getSample(InputHat5a,100)
    assert X5a.shape == (100,3)
    # set Bonferroni correction
    iOpts['Copula']['Inference']['PairIndepTest']['Correction'] = 'Bonferroni' # auto, none, fdr, Bonferroni
    InputHat5b = uq.createInput(iOpts)
    X5b = uq.getSample(InputHat5b,100)
    assert X5b.shape == (100,3)

    # Different selection criteria for marginals and copula inference
    iOpts['Inference']['Criterion'] = 'BIC' # AIC, ML, BIC, KS
    InputHat6 = uq.createInput(iOpts)
    X6 = uq.getSample(InputHat6,100)
    assert X6.shape == (100,3)
    # Copula ionference with fixed copula type
    # Gaussian copula
    iOpts['Copula'] = {'Type': 'Gaussian'}
    InputHat7a = uq.createInput(iOpts)
    X7a = uq.getSample(InputHat7a,100)
    assert X7a.shape == (100,3)
    # Vine copulas
    iOpts['Copula'] = {
        'Type': 'CVine',
        'Inference': {
            'CVineStructure': [[3,1,2]],
            'PCFamilies': ['Gaussian', 'Gumbel', 't']
        }
    }
    InputHat7b = uq.createInput(iOpts)
    X7b = uq.getSample(InputHat7b,100)
    assert X7b.shape == (100,3)
    # # Marginals inference with fully specified copula
    iOpts['Copula'] = {'Type': 'Gaussian'}
    iOpts['Copula']['Parameters'] = [[1, -.4, .3], [-.4, 1, -.6], [.3, -.6, 1]]
    InputHat8 = uq.createInput(iOpts)
    X8 = uq.getSample(InputHat8,100)
    assert X8.shape == (100,3)
    # # Copula inference with fixed marginals
    del iOpts
    iOpts = {
        'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1, 'Exponential', [1])] + [uq.Marginals(1,'Uniform',[-1,3])],
        'Inference': {'Data': X.tolist()} 
    }
    InputHat9 = uq.createInput(iOpts)
    X9 = uq.getSample(InputHat9,100)
    assert X9.shape == (100,3)
    # Copula inference using different data
    iOpts['Copula'] = {
        'Type': 'auto',
        'Inference': {'Data': X[::2].tolist()}
    }
    InputHat10 = uq.createInput(iOpts)
    X10 = uq.getSample(InputHat10,100)
    assert X10.shape == (100,3)  
    # Copula inference on pseudo-observations in the unit hypercube 
    del iOpts
    iOpts = {
        'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])] + [uq.Marginals(1,'Uniform',[-1,3])],
        'Copula': {
            'Type': 'auto',
            'Inference': {'DataU': U.tolist()}
        }
    }
    InputHat11 = uq.createInput(iOpts)
    X11 = uq.getSample(InputHat11,100)
    assert X11.shape == (100,3)

def test_InferencePairCopula(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # data generation
    iOptsTrue = {'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])] + [uq.Marginals(1, 'Uniform',[-1,3])]}
    iOptsTrue['Copula'] = {
        'Type': 'CVine',
        'Structure': [[3,1,2]],
        'Families': ['Gaussian', 'Gumbel', 't'],
        'Rotations': [0,90,0],
        'Parameters': [.4, 2, [-.2, 2]]
    }
    myInputTrue = uq.createInput(iOptsTrue)
    X = uq.getSample(myInputTrue,100)
    assert X.shape == (100,3)

    # Inference of pair copulas
    iOpts = {
        'Inference': {'Data': X[:,:2].tolist()},
        'Copula': {'Type': 'Pair'}
    }
    InputHat5c = uq.createInput(iOpts)
    X5c = uq.getSample(InputHat5c,100)
    assert X5c.shape == (100,2)
    # select among all supported pair copula families
    iOpts['Copula']['Inference'] = {
        'PCfamilies' : ['Gaussian', 'Frank', 'Clayton']
    }
    InputHat5d = uq.createInput(iOpts)
    X5d = uq.getSample(InputHat5d,100)
    assert X5d.shape == (100,2)    
    # infer the copula on data Xnew
    iOptsTrue2 = {'Marginals': uq.StdUniformMarginals(2),
                  'Copula': {'Type': 'Pair','Family': 'Gumbel','Parameters': [1.5]}
                 }
    myInputTrue2 = uq.createInput(iOptsTrue2)
    Xnew = uq.getSample(myInputTrue2,100)
    iOpts['Copula']['Inference']['Data'] = Xnew.tolist()
    InputHat5e = uq.createInput(iOpts)
    X5e = uq.getSample(InputHat5e,100)
    assert X5e.shape == (100,2)
    # presudo-observations U directly provided for copula inference
    Unew = uq.all_cdf(Xnew,myInputTrue2['Marginals'])
    del iOpts['Copula']['Inference']['Data']
    iOpts['Copula']['Inference']['DataU'] = Unew.tolist()
    InputHat5f = uq.createInput(iOpts) 
    X5f = uq.getSample(InputHat5f,100)
    assert X5f.shape == (100,2)
