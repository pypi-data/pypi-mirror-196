import pandas as pd
from sklearn.datasets import load_iris, load_diabetes

from pyhard.measures import ClassificationMeasures, RegressionMeasures
from pyhard.classification import ClassifiersPool


# Comentar o código dessa célula para não printar o log.

import logging
sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
# sh.setFormatter(formatter)
logging.getLogger().addHandler(sh)

df_class = pd.read_csv(r"C:\Users\pedro.paiva\Documents\PhD\COVID\dados_sjc_internacao_14_sub_nidx.csv")

# measures_class = ClassificationMeasures(df_class)
#
# df_measures_class = measures_class.calculate_all()

pool_class = ClassifiersPool(df_class)

algo_list = [
    'svc_linear',
    'svc_rbf',
    'random_forest',
    'gradient_boosting',
    'bagging',
    'logistic_regression',
    'mlp'
]

df_perf_class = pool_class.run_all(hyper_param_optm=False, n_folds=5, n_iter=1, algo_list=algo_list)

pool_class.estimate_ih()
