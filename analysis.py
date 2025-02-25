### This is the object with the things that are going on
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np

class Analysis:

    sample_data = pd.read_csv("data/validation_sample_data.csv")
    shap_values_ridge = pickle.load(open("data/shap_values_ridge.pkl", "rb"))
    shap_values_catboost = pickle.load(open("data/shap_values_catboost.pkl", "rb"))
    proportion_cell_expression= pd.read_csv("data/single_cell/proportion_cell_type_div.csv", index_col=0)
    top_genes = ["FEZ2"]
    