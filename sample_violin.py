from shiny import ui, render, reactive, App
import pandas as pd
from ploting_profiles import violin_plot_grouped_by_sex_and_age_group
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
sample_violin_ui = ui.nav_panel(
    "Violin",
    ui.input_select(
        "gene_v", 
        "Select Gene:", 
        choices=choices,  # Populate dropdown with gene options
    ),
    #output_widget("boxplot_output")  # Widget to render the boxplot
    ui.output_plot("violin_output"),
)

# Server logic for the Sample tab
def violin_server(input, output, session):
    @output
    @render.plot
    def violin_output():
        # Capture selected gene from dropdown
        selected_gene = input.gene_v()
        
        if not selected_gene:
            return "Please select a gene to display the boxplot."

        # Generate the boxplot for the selected gene
        
        fig = violin_plot_grouped_by_sex_and_age_group(
            gene_data=expression_data_mf, 
            gene=selected_gene, 
            save=None, 
            plot=False
        )
        
        
        return fig


