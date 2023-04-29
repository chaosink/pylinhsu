import numpy as np


def dft(x):
    """
    Function to calculate the
    Discrete Fourier Transform
    of a 1D real-valued signal x
    """

    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)

    X = e.dot(x)

    return X


def fft(x):
    """
    A recursive implementation of
    the 1D Cooley-Tukey FFT, the
    input should have a length of
    power of 2.
    """
    N = len(x)

    if N == 1:
        return x
    else:
        X_even = fft(x[::2])
        X_odd = fft(x[1::2])
        factor = np.exp(-2j * np.pi * np.arange(N) / N)

        X = np.concatenate([
            X_even + factor[:N // 2] * X_odd,
            X_even + factor[N // 2:] * X_odd])
        return X


def fft_vectorized(x):
    """
    A vectorized, non-recursive version of the Cooley-Tukey FFT.
    """
    x = np.asarray(x, dtype=float)
    N = x.shape[0]

    if np.log2(N) % 1 > 0:
        raise ValueError("size of x must be a power of 2")

    # N_min here is equivalent to the stopping condition above,
    # and should be a power of 2
    N_min = min(N, 32)

    # Perform an O[N^2] DFT on all length-N_min sub-problems at once
    n = np.arange(N_min)
    k = n[:, None]
    M = np.exp(-2j * np.pi * n * k / N_min)
    X = np.dot(M, x.reshape((N_min, -1)))

    # build-up each level of the recursive calculation all at once
    while X.shape[0] < N:
        X_even = X[:, :X.shape[1] // 2]
        X_odd = X[:, X.shape[1] // 2:]
        factor = np.exp(-1j * np.pi * np.arange(X.shape[0])
                        / X.shape[0])[:, None]
        X = np.vstack([X_even + factor * X_odd,
                       X_even - factor * X_odd])

    return X.ravel()


def dft_simple(x):
    N = len(x)
    n = np.arange(N)
    k = n.reshape((N, 1))
    cos_waves = np.cos(2 * np.pi * k * n / N)
    sin_waves = np.sin(2 * np.pi * k * n / N)
    cos_ampls = cos_waves.dot(x)
    sin_ampls = sin_waves.dot(x)
    X = cos_ampls - 1j * sin_ampls
    return X


from sympy import oo, Symbol, integrate
def convolve(f, g, t, lower_limit=-oo, upper_limit=oo):
    tau = Symbol('__very_unlikely_name__', real=True)
    return integrate(f.subs(t, tau) * g.subs(t, t - tau),
        (tau, lower_limit, upper_limit))
