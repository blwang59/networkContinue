import matplotlib.pyplot as plt
import numpy as np 
from sklearn import datasets, linear_model

diabetes = datasets.load_diabetes()

diabetes_X = diabetes.data[:, np.newaxis, ]