from shiny import ui, render
import pandas as pd
from ploting_profiles import box_plot_expression_by_age_and_sex
from data_cache import load_expression_data


with open("data/selected_genes.txt") as f:
    choices = f.read().splitlines()

sample_ui = ui.nav_panel(
    "Sample",
    ui.input_select("gene", "Select Gene:", choices=choices),
    ui.output_plot("boxplot_output"),
)

def sample_server(input, output, session):
    @output
    @render.plot
    def boxplot_output():
        selected_gene = input.gene()
        if not selected_gene:
            return
        fig = box_plot_expression_by_age_and_sex(
            gene_data=load_expression_data(),
            gene=selected_gene,
            save=None, plot=False, sex_palette=None,
        )
        return fig
