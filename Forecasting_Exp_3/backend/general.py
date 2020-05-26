from .dependencies import *

def get_state(data, t, n):
    """
    data: pandas dataframe 
    t: 
    n: 
    """
    
    d = t - n + 1
    block = data[d:t + 1] if d >= 0 else -d * [data[0]] + data[0:t + 1]
    res = []

    for i in range(n - 1):
        res.append(block[i + 1] + block[i])

    return np.array([res])

