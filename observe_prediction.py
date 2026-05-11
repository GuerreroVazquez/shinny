from shiny import ui, render, reactive
import shap
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import numpy as np
from ploting_profiles import get_top_n_shap_values
from  analysis import Analysis
from observe_lead_genes import top_genes_rv


sample_data = Analysis.sample_data
shap_values_ridge = Analysis.shap_values_ridge
shap_values_catboost = Analysis.shap_values_catboost

max_n = len(sample_data)

# UI for the SHAP visualization
observe_pred_ui = ui.nav_panel(
    "Observe",
    ui.output_plot("shap_plot"),
        
        # Sample navigation controls
    ui.layout_columns(
        ui.input_action_button("prev_sample", "⬅️"),
        ui.input_numeric("sample_number", "", 1, min=1, max=max_n),
        ui.input_action_button("next_sample", "➡️"),
    )
)

# Server logic for SHAP
def observe_pred_server(input, output, session):
    @output
    @render.plot
    def shap_plot():
        
        current_sample = input.sample_number()
        if type(current_sample) == int:
            if current_sample is None or current_sample < 1:
                current_sample=1
        else:
            current_sample=1
        sample_number = current_sample-1
        model_name = input.model()
        shap_values = None
        if model_name == "Ridge":
            shap_values = shap_values_ridge
        else:
            shap_values = shap_values_catboost
        shap_values_at_index = shap_values[sample_number]
        feature_names = shap_values.feature_names
        #top_genes = get_top_n_shap_values(shap_values_at_index=shap_values_at_index, feature_names=feature_names, n=10)
        top_genes = get_top_n_shap_values(shap_values_at_index=shap_values_at_index, feature_names=feature_names, n=10)
        Analysis.top_genes = top_genes
        top_genes_rv.set(list(top_genes))
        # Placeholder for your SHAP function
        return shap.plots.waterfall(shap_values[sample_number])
