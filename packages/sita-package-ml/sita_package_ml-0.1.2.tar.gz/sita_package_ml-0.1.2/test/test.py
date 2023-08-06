import sita_package_ml.code_src as sl
import inspect
import json
import numpy as np
from pandas import json_normalize

implemented_fct=[]

all_functions = inspect.getmembers(sl, inspect.isfunction)
implemented_function = [t for t in all_functions if inspect.getmodule(t[1]) == sl]
for i in implemented_function:
    implemented_fct.append(i[0])

n_samples=20
n_features=8
problem = "classification"
stats=[]
if problem =="classification" or problem =="regression":
    #generate dataset
    X, Y = sl.generate(problem, n_samples,n_features)
    # build the model and get the error rate
    model, error_rate = sl.learn(problem,X,Y)
    # get the predictions
    final_prediction= sl.predict(model,problem)
    # get statistics
    mean_target, std_target=sl.target_statistics(Y)
    mean_features, std_features =sl.features_statistics(X)
    correlations=sl.correlation(X,Y)
    print(error_rate)
   