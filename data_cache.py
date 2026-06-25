import pandas as pd
from functools import cache


@cache
def load_expression_data():
    male = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_male.csv", index_col=0)
    female = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_female.csv", index_col=0)
    return pd.concat([male, female], axis=0)
