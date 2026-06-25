from functools import cache
import pandas as pd
import pickle


class Analysis:

    sample_data = pd.read_csv("data/validation_sample_data.csv")
    proportion_cell_expression = pd.read_csv("data/single_cell/proportion_cell_type_div.csv", index_col=0)
    top_genes = ["FEZ2"]

    @staticmethod
    @cache
    def shap_values_ridge():
        return pickle.load(open("data/shap_values_ridge.pkl", "rb"))

    @staticmethod
    @cache
    def shap_values_catboost():
        return pickle.load(open("data/shap_values_catboost.pkl", "rb"))
    