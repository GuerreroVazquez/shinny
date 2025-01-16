from shiny import ui, render, reactive, App
import pandas as pd
from ploting_profiles import plot_lfc
import matplotlib.pyplot as plt
from io import BytesIO
import base64


# Load the datasets
selected_genes_file = "data/selected_genes.txt"
with open(selected_genes_file, "r") as file:
    choices = file.read().splitlines()

# UI for the Sample tab
gene_lfc_ui = ui.nav_panel(
    "LogFoldChange",
    ui.input_select(
        "gene_lfc", 
        "Select Gene:", 
        choices=choices,  # Populate dropdown with gene options
    ),
    #output_widget("boxplot_output")  # Widget to render the boxplot
    ui.output_plot("lfc_output"),
)

# Server logic for the Sample tab
def gene_lfc_server(input, output, session):
    @output
    @render.plot
    def lfc_output():
        # Capture selected gene from dropdown
        selected_gene = input.gene_lfc()
        
        if not selected_gene:
            return "Please select a gene to display the boxplot."

        # Generate the boxplot for the selected gene
        file_info = input.file_gene()[0]
        candidate_genes = pd.read_csv(file_info["datapath"])
        columns_to_plot = ['young.vs.middle_female', 'male.vs.female_middle', 'middle.vs.old_male',
                    'male.vs.female_Young', 'young.vs.middle_male', 'male.vs.female_Middle',
                    'middle.vs.old_female', 'MO', 'male.vs.female_old', 'young.vs.old_male',
                    'young.vs.old_female', 'male.vs.female_Old', 'middle.vs.old',
                    'young.vs.old', 'male.vs.female_young', 'young.vs.middle']
        fig = plot_lfc(symbol=selected_gene, candidate_genes=candidate_genes, columns_to_plot=columns_to_plot)
        
        
        return fig


