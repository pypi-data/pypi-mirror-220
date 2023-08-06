import pytest
import numpy as np

def test_discrepancy(request,helpers):
    mySession = helpers.init_session(request)
    uq = mySession.cli
    uq.rng(100, 'twister')
    ModelOpts = {
        'Type' : 'Model',
        'mString': '5/32*X(5)*X(3)^4/(X(4)*X(1)*X(2)^3)'
    }

    myModel = uq.createModel(ModelOpts)

    PriorOpts = {
    "Marginals": [
        {
        "Name": "b", # beam width
        "Type": "Constant",
        "Parameters": [0.15] # (m)
        },
        {
        "Name": "h", # beam height
        "Type": "Constant",
        "Parameters": [0.3] # (m)
        },
        {
        "Name": "L", # beam length
        "Type": "Constant",
        "Parameters": [5] # (m) 
        },
        {
        "Name": "E", # Young's modulus
        "Type": "LogNormal",
        "Moments": [30e9,4.5e9] # (N/m^2)
        },
        {
        "Name": "p", # constant distributed load   
        "Type": "Constant",
        "Parameters": [12000] # (N/m)
        }
    ]
    }

    myPriorDist = uq.createInput(PriorOpts)

    V_mid = np.array([12.84, 13.12, 12.13, 12.19, 12.67])/1000 # (m)
    myData = {
        'y': V_mid.tolist(),
        'Name': 'Beam mid-span deflection',
    }

    BayesOpts = {
        "Type" : "Inversion",
        "Data" : myData,
    }

    DiscrepancyPriorOpts = {
        'Name': 'Prior of discrepancy parameter',
        'Marginals': {
            'Name': 'Sigma2',
            'Type': 'Uniform',
            'Parameters': [0, np.mean(V_mid)**2]
        }
    }

    myDiscrepancyPrior = uq.createInput(DiscrepancyPriorOpts)

    DiscrepancyOpts = {
        'Type': 'Gaussian',
        'Prior': myDiscrepancyPrior['Name']
    }

    BayesOpts['Discrepancy'] = DiscrepancyOpts
    BayesOpts['Prior'] = myPriorDist['Name'] 

    myBayesianAnalysis2b = uq.createAnalysis(BayesOpts)
