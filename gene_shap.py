from shiny import ui, render, reactive, App
import pandas as pd
from ploting_profiles import violin_plot_grouped_by_sex_and_age_group
import matplotlib.pyplot as plt
from shinywidgets import output_widget
from io import BytesIO
import base64
import pickle
import shap
# UI for the Sample tab


# Load the datasets
# data/shap_values_ridge.pkl' has the shap_values
shap_values_ridge = pickle.load(open("data/shap_values_ridge.pkl", "rb"))
shap_values_catboost = pickle.load(open("data/shap_values_catboost.pkl", "rb"))
# the data of the samples is in "data/test_sample_data.csv"
sample_data = pd.read_csv("data/validation_sample_data.csv")



max_n = len(sample_data)
# UI for the SHAP tab
shap_ui = ui.nav_panel(
    "SHAP",
    
    # Model selection combobox
    ui.input_select("model", "Model", choices=["Ridge", "Catboost"]),
    
    # Disabled sample info section
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_text("sample_index", "Sample:", value="1"),
            ui.input_text("actual_age", "Actual Age:", value="23"),
            ui.input_text("predicted_age", "Predicted Age:", value="21"),
            ui.input_text("sarcopenic", "Sarcopenic:", value="NO"),
            ui.input_text("sample_id", "Sample id:", value="SRR13759025"),
            ui.input_text("experiment", "Experiment:", value="GSE1767186"),
        ),
        
        # SHAP plot placeholder
        ui.output_plot("shap_plot"),
        
        # Sample navigation controls
        ui.layout_columns(
            ui.input_action_button("prev_sample", "⬅️"),
            ui.input_numeric("sample_number", "", 1, min=1, max=max_n),
            ui.input_action_button("next_sample", "➡️"),
        )
    )
)

# Server logic for the SHAP tab
def shap_server(input, output, session):
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
        # Placeholder for your SHAP function
        return shap.plots.waterfall(shap_values[sample_number])
    # Navigation logic
    @reactive.effect
    def update_sample():
        
        current_sample = input.sample_number()
        if type(current_sample) == int:
            if current_sample is None or current_sample < 1:
                current_sample=1
        else:
            current_sample=1
        
        # Handle previous sample button click
        #if input.prev_sample():
        #    new_sample = max(1, current_sample - 1)
        #    ui.update_numeric("sample_number", value=new_sample)
        
        # Handle next sample button click
        #if input.next_sample():
        #    new_sample = min(max_n, current_sample + 1)
        #    ui.update_numeric("sample_number", value=new_sample)
        
        sample_info = sample_data.loc[current_sample-1]
        model_name = input.model()

        ui.update_text("sample_index", value=str(current_sample))
        ui.update_text("actual_age", value=str(sample_info["Age"]))
        ui.update_text("predicted_age", value=str(sample_info[model_name+'P']))
        ui.update_text("sarcopenic", value=str(sample_info["Status"]))
        ui.update_text("sample_id", value=str(sample_info["Sample"]))
        ui.update_text("experiment", value=str(sample_info["Experiment"]))
