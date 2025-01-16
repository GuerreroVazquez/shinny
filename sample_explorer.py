from shiny import ui

# UI for the Sample tab
sample_ui = ui.nav_panel(
    "Sample",
    ui.p("Sample content will go here.")  # Placeholder for the Sample tab
)

# Server logic for the Sample tab (if needed)
def sample_server(input, output, session):
    pass  # Add any server logic specific to the Sample tab here





from shiny import ui, render, reactive, App
import pandas as pd
from ploting_profiles import box_plot_expression_by_age_and_sex
import matplotlib.pyplot as plt
from shinywidgets import output_widget
from io import BytesIO
import base64


# Load the datasets
expression_data = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols.csv")
male_expression = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_male.csv", index_col=0)
female_expression = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_female.csv", index_col=0)
expression_data_mf = pd.concat([male_expression, female_expression], axis=0)

selected_genes_file = "data/selected_genes.txt"
with open(selected_genes_file, "r") as file:
    choices = file.read().splitlines()

# UI for the Sample tab
sample_ui = ui.nav_panel(
    "Sample",
    ui.input_select(
        "gene", 
        "Select Gene:", 
        choices=choices,  # Populate dropdown with gene options
    ),
    #output_widget("boxplot_output")  # Widget to render the boxplot
    ui.output_plot("boxplot_output"),
)

# Server logic for the Sample tab
def sample_server(input, output, session):
    @output
    @render.plot
    def boxplot_output():
        # Capture selected gene from dropdown
        selected_gene = input.gene()
        
        if not selected_gene:
            return "Please select a gene to display the boxplot."

        # Generate the boxplot for the selected gene
        
        fig = box_plot_expression_by_age_and_sex(
            gene_data=expression_data_mf, 
            gene=selected_gene, 
            save=None, 
            plot=False, 
            sex_palette=None
        )
        
        
        return fig


