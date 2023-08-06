import pytest
import numpy as np

def test_analysis(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    mySession.timeout = 400 
    # Prepare the experimental design
    # & validation set from a simple model
    InputOpts = {
        'Marginals': [
            {
            'Name':'X1',
            'Type':'Gaussian',
            'Parameters' : [0.25, 1]
            },
            {
            'Name':'X2',
            'Type':'Gaussian',
            'Parameters' : [0.25, 1]
            }]
        }
    print("Creating an input...")
    uq.createInput(InputOpts)
    print("Done.")
    print("Creating a true model object...")
    ModelOpts = {'Type' : 'Model',
        'ModelFun': 'uqpylab.test.true_models.hat2d'}
    #MCSOpts.Type = 'Reliability'
    myModel = uq.createModel(ModelOpts)
    print("Done.")
    # do an AK-MCS analysis
    AKMCSOpts = {
        'Type': 'Reliability',
        'Method' : 'AKMCS',
        'Simulation': {
            'MaxSampleSize': 1e4},
        'AKMCS': {
            'MaxAddedED' : 20,
            'IExpDesign':{
                'N': 100,
                'Sampling': 'LHS',
            },
            'Kriging':{
                'Corr':{
                    'Family': 'Gaussian'
                }
            },
        'Convergence': 'stopPf',
        'LearningFunction': 'EFF'
        },
    }
    print("Starting an AKMCS analysis...")
    myAKMCSAnalysis = uq.createAnalysis(AKMCSOpts)
    print("Done.")
    assert myAKMCSAnalysis['Results']['Pf'] < 0.001
    print("Done.")

def R_S_input_and_model(uq):
    print("Creating a true model object...")
    ModelOpts = {'Type': 'Model', 'mString': 'X(:,1) - X(:,2)', 'isVectorized': 1}
    myModel = uq.createModel(ModelOpts)
    print("Done.")

    print("Creating the input...")
    InputOpts = {
        "Marginals": [
            {"Name": "R", "Type": "Gaussian", "Moments": [5.0 , 0.8]},
            {"Name": "S", "Type": "Gaussian", "Moments": [2.0 , 0.6]}
        ]
    }
    myInput = uq.createInput(InputOpts)
    print("Done.")
    return myModel, myInput

def R_S_run_Analysis_print_display(uq, myOpts):
    Analysis = uq.createAnalysis(myOpts)
    print("Done.")
    print(f"Checking print functionality...")       
    uq.print(Analysis)
    print("Done.")    
    print(f"Checking display functionality...")
    uq.display(Analysis,test_mode=True);
    print("Done.")    
    return Analysis

def test_sse_reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    print("Creating an input...")
    InputOpts = {
            "Marginals": [
                {"Name": "R",               # Resistance
                "Type": "Gaussian",
                "Moments": [5.0 , 0.8]
                },
                {"Name": "S",               # Stress
                "Type": "Gaussian",
                "Moments": [2.0 , 0.6]
                }
            ]
        }
    myInput = uq.createInput(InputOpts)
    print("Done.")
    print("Creating a model...")
    ModelOpts = { 
        'Type': 'Model', 
        'mString': 'X(:,1) - X(:,2)',
        'isVectorized': 1
    }
    myModel = uq.createModel(ModelOpts)
    print("Done.")
    SSEROpts = {
    "Type": "Reliability",
    "Method": "SSER"
    }
    print("Performing SSE Reliability...")
    SSERAnalysis = uq.createAnalysis(SSEROpts)
    print("Done.")
    print("Testing print...")
    uq.print(SSERAnalysis)
    print("Testing display...")
    uq.display(SSERAnalysis,test_mode=True)
    print("All good.")


def test_MCS_Reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    R_S_input_and_model(uq)
    print("Running Monte Carlo simulation...")    
    MCSOpts = {
        "Type": "Reliability",
        "Method":"MCS",
        "Simulation": {"MaxSampleSize": 1e4, "BatchSize": 1e3, "TargetCoV": 5e-2}
    }
    MCSAnalysis = R_S_run_Analysis_print_display(uq, MCSOpts)
    assert abs(MCSAnalysis['Results']['Pf'] - 0.001349898031630) < 0.001

def test_FORM_Reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    R_S_input_and_model(uq)
    print("Running FORM...") 
    FORMOpts = {
        "Type": "Reliability",
        "Method":"FORM"
    }
    FORMAnalysis=R_S_run_Analysis_print_display(uq, FORMOpts)
    assert abs(FORMAnalysis['Results']['Pf'] - 0.001349898031630) < 0.001

def test_IS_Reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    R_S_input_and_model(uq)
    print("Running Inportance sampling...")    
    ISOpts = {
        "Type": "Reliability",
        "Method":"IS",
        "Simulation": {"MaxSampleSize": 1e4, "BatchSize": 1e3, "TargetCoV": 5e-2}
    }
    ISAnalysis=R_S_run_Analysis_print_display(uq, ISOpts)
    assert abs(ISAnalysis['Results']['Pf'] - 0.001349898031630) < 0.001

def test_Subset_Reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    R_S_input_and_model(uq)
    print("Running Subset simulation...")    
    SubsetSimOpts = {
        "Type": "Reliability",
        "Method":"Subset",
        "Simulation": {"MaxSampleSize": 1e4, "BatchSize": 1e3, "TargetCoV": 5e-2}
    }
    SubsetSimAnalysis=R_S_run_Analysis_print_display(uq, SubsetSimOpts)
    assert abs(SubsetSimAnalysis['Results']['Pf'] - 0.001349898031630) < 0.001

def test_APCKMCS_Reliability(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')   

    R_S_input_and_model(uq)
    print("Running Adaptive-Polynomial-Chaos-Kriging-Monte-Carlo-Simulation...")    
    APCKOpts = {
        "Type": "Reliability",
        "Method": "AKMCS",
        "AKMCS": {
            "MetaModel": "PCK",
            "PCK": {
                "Kriging": {
                    "Corr": {
                        "Family": "Gaussian"
                    }
                }
            },
            "IExpDesign": {
                "N": 5
            }
        },
        "Simulation": {
            "MaxSampleSize": 1.0E+6
        }
    }
    APCKAnalysis=R_S_run_Analysis_print_display(uq, APCKOpts)
    assert abs(APCKAnalysis['Results']['Pf'] - 0.001349898031630) < 0.001


