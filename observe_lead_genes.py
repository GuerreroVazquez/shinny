from shiny import ui, render, reactive
import shap
import pandas as pd
import matplotlib.pyplot as plt
from shinywidgets import output_widget, render_widget  
from ploting_profiles import print_radar_spyder, generate_goScatter
from analysis import Analysis

proportion_cell_expression= Analysis.proportion_cell_expression

# Reactive value that holds the current top genes so other servers can update it
top_genes_rv = reactive.Value(list(Analysis.top_genes))

# UI for the SHAP visualization
observe_lead_ui = ui.nav_panel(
    "Lead_genes",
    ui.output_ui("dynamic_select"),
    ui.p("Single-cell data for these plots were obtained from https://www.muscleageingcellatlas.org/."),
    ui.output_text("value"),
    output_widget("spidy_plot")
)

# Server logic for SHAP
def observe_lead_server(input, output, session):
    @reactive.Calc
    def get_top_genes():
        return {gene: gene for gene in top_genes_rv()}

    @output
    @render.ui
    def dynamic_select():
        return ui.input_select(
            "see_genes",  
            "Select options below:",  
            get_top_genes(),
            multiple=True,
        )
    
    @output
    @render.text
    def value():
        return f"{input.see_genes()}"
    
    @output
    @render_widget
    def spidy_plot():
        see_genes = list(input.see_genes())
        plot = generate_goScatter(genes = see_genes, expression=proportion_cell_expression)
        return plot
