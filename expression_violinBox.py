from shiny import ui, render, App
import pandas as pd
from ploting_profiles import violin_plot_grouped_by_sex_and_age_group, box_plot_expression_by_age_and_sex, prepare_box_plot_expression, prepare_violin_plot_expression
import matplotlib.pyplot as plt

# Load the datasets
expression_data = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols.csv")
male_expression = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_male.csv", index_col=0)
female_expression = pd.read_csv("data/RNAseq_z_score_adjustedCombat_symbols_female.csv", index_col=0)
expression_data_mf = pd.concat([male_expression, female_expression], axis=0)

selected_genes_file = "data/selected_genes.txt"
with open(selected_genes_file, "r") as file:
    choices = file.read().splitlines()

# UI
expression_ui = ui.nav_panel(
    "Violin",
    ui.page_fluid(
        ui.page_sidebar(
            ui.sidebar(
                ui.input_select("gene_vb", "Gene", choices),
                ui.input_select("plot_type", "Plot", ["Violin Plot", "Box Plot"]),
                ui.input_checkbox("grouping", "Group by age group", True),
                ui.input_checkbox("split_sex", "Divide sex", False)
            ),
            ui.output_plot("ploting_plot")
        )
    )
)

# Server
def expression_server(input, output, session):
    @output
    @render.plot
    def ploting_plot():
        gene = input.gene_vb()
        plot_type = input.plot_type()
        grouping = input.grouping()
        split_sex = input.split_sex()

        if plot_type == "Violin Plot":
            fig = prepare_violin_plot_expression(gene_data = expression_data_mf,  gene= gene, age_group=grouping, sex_div=split_sex, save=None, plot=False, check_significance=True)
        elif plot_type == "Box Plot":
            fig = prepare_box_plot_expression(gene_data=expression_data_mf, gene= gene, age_group=grouping, sex_div=split_sex, save=None, plot=False, check_significance=True)
        return fig
