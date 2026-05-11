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
    ui.layout_columns(
        ui.output_ui("dynamic_select"),
        ui.output_ui("genes_without_data_box"),
    ),
    ui.p("Single-cell data for these plots was obtained from https://www.muscleageingcellatlas.org/."),
    output_widget("spidy_plot")
)

# Server logic for SHAP
def observe_lead_server(input, output, session):
    @reactive.Calc
    @reactive.Calc
    def split_genes_by_data():
        selected_genes = top_genes_rv()
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
    def dynamic_select():
        genes_with_data, _ = split_genes_by_data()
        return ui.input_select(
            "see_genes",
            "Select options below:",
            {gene: gene for gene in genes_with_data},
            selected=genes_with_data,
            multiple=True,
        )

    @output
    @render.ui
    def genes_without_data_box():
        _, genes_without_data = split_genes_by_data()
        value = ", ".join(genes_without_data)
        textarea_id = "genes_without_data_textarea"
        return ui.tags.div(
            ui.tags.label("Genes without enough data for radar", **{"for": textarea_id}),
            ui.tags.textarea(
                value,
                id=textarea_id,
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
