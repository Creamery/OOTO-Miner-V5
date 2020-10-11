

import numpy as np
from scipy.stats import chi2_contingency

import Filter_support as FILS


def chiSquare(df_dataset, filter):
    FILS.applyFilter(df_dataset, filter)
    obs = np.array([[398, 0], [170, 232]])
    out = chi2_contingency(obs)
    print(out)
