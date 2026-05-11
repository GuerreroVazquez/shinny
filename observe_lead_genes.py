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
    ui.layout_columns(
        ui.output_ui("genes_with_data_box"),
        ui.output_ui("genes_without_data_box"),
    ),
    ui.p("Single-cell data for these plots was obtained from https://www.muscleageingcellatlas.org/."),
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

    @reactive.Calc
    def split_genes_by_data():
        selected_genes = input.see_genes() or []
        genes_with_data = []
        genes_without_data = []
        for gene in selected_genes:
            if gene in proportion_cell_expression.index:
                genes_with_data.append(gene)
            else:
                genes_without_data.append(gene)
        return genes_with_data, genes_without_data

    @output
    @render.ui
    def genes_with_data_box():
        genes_with_data, _ = split_genes_by_data()
        value = ", ".join(genes_with_data)
        return ui.tags.div(
            ui.tags.label("Genes with enough data for radar"),
            ui.tags.textarea(
                value,
                readonly=True,
                rows="4",
                style="width: 100%;"
            )
        )

    @output
    @render.ui
    def genes_without_data_box():
        _, genes_without_data = split_genes_by_data()
        value = ", ".join(genes_without_data)
        return ui.tags.div(
            ui.tags.label("Genes without enough data for radar"),
            ui.tags.textarea(
                value,
                readonly=True,
                rows="4",
                style="width: 100%;"
            )
        )
    
    @output
    @render_widget
    def spidy_plot():
        see_genes = list(input.see_genes())
        plot = generate_goScatter(genes = see_genes, expression=proportion_cell_expression)
        return plot
