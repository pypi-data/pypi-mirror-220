import numpy as np

def XsinX(X):
    return X*np.sin(X)

def hat2d(X):
    # 2D hat function
    # see https://www.uqlab.com/reliability-2d-hat-function
    X = np.array(X,ndmin=2)
    t1 = np.square(X[:,0] - X[:,1])
    t2 = 8*np.power(X[:,0] + X[:,1] - 4, 3)
    return 20 - t1 - t2

def ishigami(X):
    # Ishigami function
    X = np.array(X,ndmin=2)
    a = 7
    b = 0.1
    T1 = np.sin(X[:,0])
    T2 = a* np.power(np.sin(X[:,1]),2)
    T3 = b*np.power(X[:,2],4)*np.sin(X[:,0])
    return  T1 + T2 + T3

def meanX(X):
    X = np.array(X,ndmin=2)
    return np.mean(X, axis=1)