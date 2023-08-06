import numpy as np
import scipy.stats as sps

def bimodal_sample() -> np.ndarray:
    '''
    Generate a sample from a bimodal normal distribution (similar to in the data but simpler to see if the processing works)
    '''
    d1 = sps.norm(loc=1.3, scale=.2)
    d2 = sps.norm(loc=2.2, scale=.3)
    r1 = d1.rvs(1000, random_state=1) # 1000 random samples from d1
    r2 = d2.rvs(1000, random_state=1) # 1000 random samples from d2
    data = np.concatenate((r1, r2))
    return data