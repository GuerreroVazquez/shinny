from shiny import ui, render
import shap
import pandas as pd
import matplotlib.pyplot as plt
from shinywidgets import output_widget, render_widget  
from ploting_profiles import print_radar_spyder, generate_goScatter

proportion_cell_expression= pd.read_csv("data/single_cell/proportion_cell_type_div.csv", index_col=0)

# UI for the SHAP visualization
observe_lead_ui = ui.nav_panel(
    "Lead_genes",
     ui.input_select(  
        "see_genes",  
        "Select options below:",  
        {"FEZ2": "FEZ2", "ALDOA": "ALDOA", "AC3": "AC3"},  
        multiple=True,  
    ),  
    ui.output_text("value"),
    output_widget("spidy_plot")
)

# Server logic for SHAP
def observe_lead_server(input, output, session):
    @render.text
    def value():
        return f"{input.see_genes()}"
    
    #@output
    @render_widget
    def spidy_plot():
        see_genes = list(input.see_genes())
        plot = generate_goScatter(genes = see_genes, expression=proportion_cell_expression)
        return plot