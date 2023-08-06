import pytest
import uqpylab.sessions as uq_session
import numpy as np


def model(X):
    return X*np.sin(X)

def create_model_and_check_display(uq, name, MetaOpts):
    print(f"Computing a {name} metamodel...")
    myMeta = uq.createModel(MetaOpts)
    print("Done.")
    print(f"Checking display functionality...")
    uq.display(myMeta, test_mode=True)
    print("All good.")

# @pytest.mark.skip(reason="Leaves garbage (open figures) in current version")
def test_PCE_display(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    # Prepare the experimental design
    # & validation set from a simple model
    m_i = {
            'Type':'Uniform',
            'Parameters' : [-np.pi, np.pi]
            }
    InputOpts = {
        'Marginals': [m_i for i in [0,1,2] ]
        }
    print("Creating the input...")
    myInput = uq.createInput(InputOpts)
    print("Done.")
    
    print("Generating samples...")
    X_val = uq.getSample(N=1000)
    print("Done.")

    # create a default model
    print("Creating a true model object...")
    ModelOpts = {'Type' : 'Model',
        'ModelFun': 'uqpylab.test.true_models.ishigami'}
    myModel = uq.createModel(ModelOpts)
    print("Done.")
    print("Doing some model evaluations...")
    Y_val = model(X_val)
    print("Done.")

    # do quadrature PCE
    MetaOptsPCE = {
        'Type': 'Metamodel',
        'MetaType' : 'PCE',
        'FullModel': myModel['Name'],
        'Input': myInput['Name'],
        'Method' : 'Quadrature',
        'Degree' : 14
    }
    create_model_and_check_display(uq, "Quadrature PCE", MetaOptsPCE)
    
    print("Test complete.")

def test_Input_display_2independentVars(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # 2 independent variables
    iOpts = {'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])]}
    myInput = uq.createInput(iOpts)
    # pytest.self_trace()
    uq.display(myInput, test_mode=True)

def test_Input_display_3independentVars(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # 3 independent variables
    iOpts = {'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])] + [uq.Marginals(1, 'Uniform',[-1,3])]}
    myInput = uq.createInput(iOpts)
    uq.display(myInput,test_mode=True)

def test_Input_display_3independentVars_PDF_CDF(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # 3 independent variables - show PDF and CDF of each component
    iOpts = {'Marginals': [uq.Marginals(1,'Gaussian',[-1,1])] + [uq.Marginals(1,'Exponential',[1])] + [uq.Marginals(1, 'Uniform',[-1,3])]}
    myInput = uq.createInput(iOpts)
    uq.display(myInput, plot_density=True,test_mode=True)
    # show PDF and CDF for only marginal 1 and 3
    uq.display(myInput, idx=[1,3], plot_density=True,test_mode=True)

def test_Input_display_VineCopula(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')

    # show vine
    iOpts = {
        "Marginals": uq.StdNormalMarginals(2) +
                    [uq.Marginals(1, 'Exponential', [1.5])],
        "Copula": uq.VineCopula('Cvine', [2,1,3],['t', 'Frank', 'Independence'],[[.4, 2], .5, []])
    }
    myInput = uq.createInput(iOpts)
    uq.display(myInput,show_vine=True,test_mode=True)   







