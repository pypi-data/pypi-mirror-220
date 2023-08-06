import pytest
import uqpylab.sessions as uq_session
import numpy as np


def model(X):
    return X*np.sin(X)

def create_and_eval_model(uq, name, MetaOpts, X_val, Y_val):
    print(f"Computing a {name} metamodel...")
    myMeta = uq.createModel(MetaOpts)
    print("Done.")
    print(f"Performing {name} model evaluations...")
    Y_Meta_val = uq.evalModel(myMeta, X_val)
    print("Done.")
    print(f"Checking {name} responses...")
    assert Y_Meta_val.shape == Y_val.shape
    print("All good.")

def test_model(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    # Prepare the experimental design
    # & validation set from a simple model
    InputOpts = {
        'Marginals': [
            {
            'Type':'Uniform',
            'Parameters' : [1, 5]
            }]
        }
    print("Creating an input...")
    myInput = uq.createInput(InputOpts)
    print("Done.")
    print("Generating samples...")
    X_ED = uq.getSample(myInput, 100)
    print("Done.")

    print("Generating samples...")
    X_val = uq.getSample(N=1000)
    print("Done.")


    # create a default model
    print("Creating a true model object...")
    ModelOpts = {'Type' : 'Model',
        'ModelFun': 'uqpylab.test.true_models.XsinX'}
    myModel = uq.createModel(ModelOpts)
    print("Done.")
    print("Doing some model evaluations...")
    Y_val = model(X_val)
    Y_ED = model(X_ED)
    print(Y_ED)

    print("Done.")

    # do PCE
    MetaOptsPCE = {
        'Type': 'Metamodel',
        'MetaType' : 'PCE',
        'ExpDesign': {
            'X': X_ED.tolist(),
            'Y': Y_ED.tolist()},
        'Input': myInput['Name'],
        'Method' : 'LARS',
        'Degree' : np.arange(1,15).tolist()
    }
    create_and_eval_model(uq, "PCE", MetaOptsPCE, X_val, Y_val)
    # do Kriging
    MetaOptsKRG = {
        'Type': 'Metamodel',
        'MetaType' : 'Kriging',
        'ExpDesign': {
            'X': X_ED.tolist(),
            'Y': Y_ED.tolist()},
        # We let all other options to default values 
    }
    create_and_eval_model(uq, "Kriging", MetaOptsKRG, X_val, Y_val)
    # do PC-Kriging
    MetaOptsPCK = {
        'Type': 'Metamodel',
        'MetaType' : 'PCK',
        'ExpDesign': {
            'X': X_ED.tolist(),
            'Y': Y_ED.tolist()},
        'Mode': 'sequential',
        'PCE': {
            'Degree': np.arange(1,11).tolist()
        }
    }
    create_and_eval_model(uq, "PCK", MetaOptsPCK, X_val, Y_val)
    # do LRA
    MetaOptsLRA = {
        'Type': 'Metamodel',
        'MetaType' : 'LRA',
        'ExpDesign': {
            'X': X_ED.tolist(),
            'Y': Y_ED.tolist()},
        'Rank': np.arange(1,11).tolist(),
        'Degree': np.arange(1,11).tolist(),
    }
    create_and_eval_model(uq, "LRA", MetaOptsLRA, X_val, Y_val)
    print("Test complete.")
    
def test_multiple_outputs(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    InputOpts = {
        'Marginals': [
            {
            'Type':'Uniform',
            'Parameters' : [1, 5]
            }]
        }
    print("Creating an input...")
    myInput = uq.createInput(InputOpts)
    print("Done.")
    print("Generating samples...")
    X_ED = uq.getSample(myInput, N=5)
    X_val = uq.getSample(N=10)
    print("Done.")
    Y_val = model(X_val)
    Y_ED = model(X_ED)
    print("Creating a Kriging surrogate...")
    MetaOptsKRG = {
        'Type': 'Metamodel',
        'MetaType' : 'Kriging',
        'ExpDesign': {
            'X': X_ED.tolist(),
            'Y': Y_ED.tolist()},
        # We let all other options to default values 
    }
    myKRG = uq.createModel(MetaOptsKRG)
    print("Done.")
    print("Testing vargout=1..3 calls of uq.evalModel...")
    Ymean0 = uq.evalModel(myKRG, X_val, nargout=1)
    [Ymean1, Yvar1] = uq.evalModel(myKRG, X_val, nargout=2)
    [Ymean2, Yvar2, Ycov] = uq.evalModel(myKRG, X_val, nargout=3)
    assert (Ymean0 == Ymean1).all()
    assert (Ymean0 == Ymean2).all()
    print(np.max(np.abs(Yvar1 -  Yvar2)))
    assert np.allclose(Yvar1, Yvar2, atol=5e-7)
    assert Ycov.shape == (Ymean0.shape[0],Ymean0.shape[0])
    print("All good.")