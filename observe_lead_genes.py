from shiny import ui, render, reactive
import shap
import pandas as pd
import matplotlib.pyplot as plt
from shinywidgets import output_widget, render_widget  
from ploting_profiles import print_radar_spyder, generate_goScatter
from analysis import Analysis

proportion_cell_expression= Analysis.proportion_cell_expression
top_genes = Analysis.top_genes
# UI for the SHAP visualization
observe_lead_ui = ui.nav_panel(
    "Lead_genes",
     ui.input_select(  
        "see_genes",  
        "Select options below:",  
        {gene: gene for gene in top_genes},  
        multiple=True,  
    ),  
    ui.output_text("value"),
    output_widget("spidy_plot")
)

# Server logic for SHAP
def observe_lead_server(input, output, session):
    @reactive.Calc
    def get_top_genes():
        print(Analysis.top_genes)
        return ui.input_select(
            "see_genes",  
            "Select options below:",  
            {gene: gene for gene in Analysis.top_genes},  # Use top_genes to populate options
            multiple=True,
        )
    
        # Assuming you might update top_genes in Analysis class
        #return {gene: gene for gene in Analysis.top_genes}
    
    @output
    @render.ui
    def dynamic_select():
        print(Analysis.top_genes)
        return ui.input_select(
            "see_genes",  
            "Select options below:",  
            get_top_genes(),  # Use top_genes to populate options
            multiple=True,
        )
    
    @render.text
    def value():
        return f"{input.see_genes()}"
    
    @output
    @render_widget
    def spidy_plot():
        see_genes = list(input.see_genes())
        plot = generate_goScatter(genes = see_genes, expression=proportion_cell_expression)
        return plot