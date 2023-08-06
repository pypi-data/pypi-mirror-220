import numpy as np
from pandas import Series, DataFrame, concat
from patsy import dmatrices, build_design_matrices
from typing import Literal
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression


class LogisticRegression(LogisticRegression):
    
    def __init__(self, penalty: Literal['l1', 'l2', 'elasticnet'] = "none", *, dual = False, tol = 0.0001, C = 1, fit_intercept = False, intercept_scaling = 1, class_weight = None, random_state = 2023, solver: Literal['lbfgs', 'liblinear', 'newton-cg', 'newton-cholesky', 'sag', 'saga'] = "lbfgs", max_iter = 100, multi_class: Literal['auto', 'ovr', 'multinomial'] = "auto", verbose = 0, warm_start: bool = False, n_jobs = -1, l1_ratio = 0.5):
        super().__init__(penalty=penalty, dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, class_weight=class_weight, random_state=random_state, solver=solver, max_iter=max_iter, multi_class=multi_class, verbose=verbose, warm_start=warm_start, n_jobs=n_jobs, l1_ratio=l1_ratio)

    @classmethod
    def from_formula(cls, formula, data):
        y, X = dmatrices(formula, data)
        cls.y = y.reshape(-1)
        cls.formula = formula
        cls.X = X
        return cls()

    def __log_likelihood(self):
        z = np.dot(self.X, self.coef_.flatten())
        log_likelihood = np.sum(self.y * z - np.log(1 + np.exp(z)))
        return log_likelihood


    def fit(self):
        super().fit(self.X, self.y)
        return self
    
    def conf_int(self, conf_level = 0.95):
        z_score = norm.ppf(1 - (1 - conf_level) / 2)
        standard_errors = np.sqrt(np.diag(self.cov_matrix))
        lower_limits = self.coef_[0] - z_score * standard_errors
        upper_limits = self.coef_[0] + z_score * standard_errors
        ci = DataFrame({
            "[Lower,": lower_limits,
            "Upper]": upper_limits
        }, index = self.X.design_info.column_names)
        return ci
    
    def se(self):
        return Series(np.sqrt(np.diag(self.cov_matrix)), index=self.X.design_info.column_names, name="S.E.")

    def z_values(self):
        z_est = self.coef_[0] / self.se()
        return Series(z_est, index=self.X.design_info.column_names, name="z")
    
    def p_values(self):
        p_values = 2 * norm.cdf(-np.abs(self.z_values()))
        return Series(p_values, index=self.X.design_info.column_names, name="Pr(>|z|)")
    
    def summary(self, conf_level = 0.95):
        summary = concat(
            objs = [self.params, self.se(), self.z_values(), self.p_values(), self.conf_int(conf_level)], 
            axis = 1
        )
        return summary
    
    def predict(self, new_data: DataFrame):
        dsg = build_design_matrices([self.X.design_info], new_data)[0].view()
        return super().predict_proba(dsg)[:, 1]

        
    @property
    def cov_matrix(self):
        p = self.predict_proba(self.X)[:, 1]
        hess_matrix = np.dot(self.X.T, np.dot(np.diag(p * (1 - p)), self.X))
        cov_matrix = np.linalg.inv(hess_matrix)
        return cov_matrix
    

    @property
    def params(self):
        return Series(self.coef_.flatten().tolist(), index=self.X.design_info.column_names, name="Estimate")
    
    @property
    def aic(self):
        aic = -2 * self.__log_likelihood() + 2 * self.coef_.shape[0] - 1
        return aic.item()
    
    @property
    def bic(self):
        bic = -2 * self.__log_likelihood() + np.log(self.X.shape[0]) * (self.coef_.shape[0] - 1)
        return bic.item()
    
    
    def __repr__(self) -> str:
        return "LogisticRegression()"
