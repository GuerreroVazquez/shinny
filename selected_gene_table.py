from shiny import ui, render
import pandas as pd
from itables.widget import ITable
from shinywidgets import render_widget, output_widget


gene_data = pd.read_csv("data/Selected_genes_orthologs_pathway_lfc_tissues.csv")

gene_ui = ui.nav_panel(
    "Selected Genes",
    output_widget("gene_table"),
)

def gene_server(input, output, session):
    @output
    @render_widget
    def gene_table():
        return ITable(
            caption="Selected genes — orthologs, pathways, and tissue expression",
            df=gene_data,
            scrollY="300px", scrollX=True, height="600px", paging=True, autoWidth=True,
        )

