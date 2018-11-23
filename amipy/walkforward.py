from scipy.stats import rankdata
import numpy as np
import pandas as pd


def top(x, n):
    ranks = rankdata(x, method="ordinal")
    ranks = ranks > len(x) - n
    ranks = ranks.astype(int)
    return ranks


def bottom(x, n):
    ranks = rankdata(x, method="ordinal")
    ranks = ranks <= n
    ranks = ranks.astype(int)
    return ranks


def mid(x, n):
    ranks = rankdata(x, method="ordinal")
    start = (len(x) - n) / 2
    end = start + n
    ranks = np.logical_and(ranks <= end, ranks >= start)
    ranks = ranks.astype(int)
    return ranks


def sharpe(x):
    # use ddof=1 to comply with matlab and pandas. numpy default ddof==0, which will result in a different std
    return np.sqrt(252) * x.mean() / x.std(ddof=1)


def walk_forward(dataframe, window, top_n, map_func, select_func):

    w = dataframe.rolling(window=window, axis=0).apply(map_func, raw=True)
    if select_func:
        w = w.apply(select_func, axis=1, n=top_n)
    w = w.shift(1)
    w = pd.DataFrame(dict(zip(w.index, w.values))).T
    w = w[window:]

    # result
    result = dataframe[window:] * w.values
    result = result.sum(axis=1) * (1.0 / top_n)
    result.cumsum().plot(color="C1")

    # benchmark
    benchmark = dataframe[window:]
    benchmark.mean(axis=1).cumsum().plot(color="C0")

    print("Benchmark return: {}".format(benchmark.mean(axis=1).sum()))
    print("Result.   return: {}".format(result.sum()))
    print("Benchmark sharpe: {}".format(sharpe(benchmark.mean(axis=1))))
    print("Result    sharpe: {}".format(sharpe(result)))

    return result
