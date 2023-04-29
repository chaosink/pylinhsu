from joblib import Parallel, delayed
import multiprocessing

def parallel_for(func, params):
    n_cpu = multiprocessing.cpu_count()
    results = Parallel(n_jobs=n_cpu)(delayed(func)(param) for param in params)
    return results
