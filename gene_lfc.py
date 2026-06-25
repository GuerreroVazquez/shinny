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

lfc_data = pd.read_csv("data/lfc_from_dds.csv", index_col=0)
lfc_data.index.name = None
lfc_data = lfc_data.reset_index().rename(columns={"index": "Symbol"})

columns_to_plot = ['young.vs.middle_female', 'male.vs.female_middle', 'middle.vs.old_male',
            'male.vs.female_Young', 'young.vs.middle_male', 'male.vs.female_Middle',
            'middle.vs.old_female', 'MO', 'male.vs.female_old', 'young.vs.old_male',
            'young.vs.old_female', 'male.vs.female_Old', 'middle.vs.old',
            'young.vs.old', 'male.vs.female_young', 'young.vs.middle']

# UI for the LogFoldChange tab
gene_lfc_ui = ui.nav_panel(
    "LogFoldChange",
    ui.input_select(
        "gene_lfc", 
        "Select Gene:", 
        choices=choices,
    ),
    ui.output_plot("lfc_output"),
)

# Server logic for the LogFoldChange tab
def gene_lfc_server(input, output, session):
    @output
    @render.plot
    def lfc_output():
        selected_gene = input.gene_lfc()
        
        if not selected_gene:
            return

        fig = plot_lfc(symbol=selected_gene, candidate_genes=lfc_data, columns_to_plot=columns_to_plot)
        
        return fig


