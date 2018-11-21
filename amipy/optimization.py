import numpy as np
import cvxopt as opt
from cvxopt import blas, solvers

# Turn off progress printing
solvers.options['show_progress'] = False


class Optimization_CVXOPT:

    def __init__(self, returns_vec):
        self.returns_vec = returns_vec

    def optimal_portfolio(self, returns):
        n = len(returns)
        print("Size: " + str(n))
        returns = np.asmatrix(returns)

        N = 100
        mus = [10**(10.0 * t / N - 1.0) for t in range(N)]
        # print(mus)

        # Convert to cvxopt matrices
        S = opt.matrix(np.cov(returns))
        print("S", S.size)

        pbar = opt.matrix(np.mean(returns, axis=1))
        print("pbar", pbar.size)

        print("Covariance")
        print(S)

        print("Expected Return")
        print(pbar)

        # Create constraint matrices
        G = -opt.matrix(np.eye(n))   # negative n x n identity matrix
        h = opt.matrix(0.0, (n, 1))
        A = opt.matrix(1.0, (1, n))
        b = opt.matrix(1.0)

        # Calculate efficient frontier weights using quadratic programming
        # The following uses least square trade-off discussed in page 5 section 1.2 (https://web.stanford.edu/%7Eboyd/cvxbook/bv_cvxbook.pdf)
        portfolios = [solvers.qp(mu * S, -pbar, G, h, A, b)["x"] for mu in mus]

        # CALCULATE RISKS AND RETURNS FOR FRONTIER
        returns = [blas.dot(pbar, x) for x in portfolios]
        risks = [np.sqrt(blas.dot(x, S * x)) for x in portfolios]
        # # CALCULATE THE 2ND DEGREE POLYNOMIAL OF THE FRONTIER CURVE
        # m1 = np.polyfit(returns, risks, 2)
        # print(m1)
        # x1 = np.sqrt(m1[2] / m1[0])
        # # CALCULATE THE OPTIMAL PORTFOLIO
        # wt = solvers.qp(opt.matrix(x1 * S), -pbar, G, h, A, b)['x']
        # return np.asarray(wt), returns, risks
        return returns, risks

    def random_portfolio(self, returns):
        ''' 
        Returns the mean and standard deviation of returns for a random portfolio
        '''

        p = np.asmatrix(np.mean(returns, axis=1))
        w = np.asmatrix(self.rand_weights(returns.shape[0]))
        C = np.asmatrix(np.cov(returns))

        mu = w * p.T
        sigma = np.sqrt(w * C * w.T)

        # This recursion reduces outliers to keep plots pretty
        # if sigma > 2:
        #     return random_portfolio(returns)
        return mu, sigma

    def rand_weights(self, n):
        ''' Produces n random weights that sum to 1 '''
        k = np.random.rand(n)
        return k / sum(k)
