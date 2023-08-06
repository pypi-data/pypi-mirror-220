import pytest
import uqpylab.sessions as uq_session
import numpy as np


def test_common_scenarios(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    # Construct an input object with various input distributions
    iOptsTrue  = {
       'Marginals': [
        {
            'Type': 'Gaussian',
            'Parameters': [0,1],
            # 'Bounds': [1,10]
        },
        {
            'Type': 'Beta',
            'Parameters': [6,4],
        }
    ]

        }
    print("Creating the true input...")
    myInputTrue = uq.createInput(iOptsTrue, request_format='JSON', response_format='MAT')
    print("Done.")
    print("Generating samples...")
    X = uq.getSample(myInputTrue,N=500,Method='LHS', request_format='JSON', response_format='MAT')
    print("Done.")
    InputOpts = {
    "Copula" : {
        "Type": "Independent"
        }
    }
    InputOpts["Inference"] = {
        "Data": X.tolist()
    }

    print("Performing Inference...")
    M = 2
    InputOpts["Marginals"] = [{"Type": "auto"} for i in range(M)]
    InputOpts["Marginals"][0]["Inference"] =  {"Criterion": "KS"}
    InputOpts["Marginals"][0]["Type"] = ['Gaussian', 'Uniform', 'Beta']
    InputHat2 = uq.createInput(InputOpts, request_format='JSON', response_format='MAT')

    print("Validating results...")
    for idx, m in enumerate(myInputTrue['Marginals']):
        print(f"{m['Type']} vs {InputHat2['Marginals'][idx]['Type']}")
        print(f"{m['Parameters']} vs {InputHat2['Marginals'][idx]['Parameters']}")
        assert m['Type'] == InputHat2['Marginals'][idx]['Type']
        p1 = np.array(m['Parameters'])
        p2 = np.array(InputHat2['Marginals'][idx]['Parameters'])
        assert np.max(np.abs(p1 - p2)) < 5e-2

def test_non_parametric_marginals_inference(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    iOptsTrue = {
    'Marginals': [
        {
            'Type': 'Gaussian',
            'Parameters': [0,1],
            'Bounds': [1,10]
        },
        {
            'Type': 'Beta',
            'Parameters': [6,4],
        }
            ]
        }

    myInputTrue = uq.createInput(iOptsTrue)

    X = uq.getSample(myInputTrue,10)

    InputOpts = {
        "Copula" : {
            "Type": "Independent"
        },
        "Inference": {
            "Data": X.tolist()
        }
    }

    M = 2
    InputOpts["Marginals"] = [{"Type": "auto"} for i in range(M)]

    InputOpts["Marginals"][1]['Type'] =  "ks" 

    InputOpts["Marginals"][1]["Options"] = {
        "Kernel": "triangle",
        "Bandwidth": 0.1
    }

    InputHat = uq.createInput(InputOpts)
    assert 'GoF' in InputHat['Marginals'][0]
    assert 'GoF' in InputHat['Marginals'][1]
    assert 'KS'  in InputHat['Marginals'][1]

def test_gaussian_copula_inference(request, helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    X = np.random.rand(200,3)

    iOpts = {
        'Inference': {'Data': X.tolist()},
        'Copula': {
                'Type': 'Gaussian'
            }
    }

    InputHat = uq.createInput(iOpts)
    assert 'Inference' in InputHat['Copula']
    assert 'GoF' in InputHat['Copula']
    assert 'Criterion' in InputHat['Copula']['Inference']
    assert 'PairIndepTest' in InputHat['Copula']['Inference']
    assert 'Alpha' in InputHat['Copula']['Inference']['PairIndepTest']
    assert 'Type' in InputHat['Copula']['Inference']['PairIndepTest']
    

