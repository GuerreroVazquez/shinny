from shiny import ui, render
import pandas as pd
from itables.widget import ITable
from shinywidgets import render_widget, output_widget

# UI for the Gene tab
gene_ui = ui.nav_panel(
    "Gene",
    ui.input_file("file_gene", "Upload your Gene CSV file", accept=[".csv"]),
    output_widget("gene_table"),  # For the interactive gene table
)

# Server logic for the Gene tab
def gene_server(input, output, session):
    @output
    @render_widget
    def gene_table():
        if not input.file_gene():
            # Placeholder when no file is uploaded
            return ITable(
                caption="No file uploaded. Please upload a Gene CSV file.",
                df=pd.DataFrame({"Message": ["No data to display"]}),
            )

        # Read the uploaded file
        file_info = input.file_gene()[0]
        df = pd.read_csv(file_info["datapath"])

        # Limit to first 10 rows and columns
        columns_keep = df.columns[:11]
        #rows_keep = df.index[:10]
        #df = df.loc[rows_keep, columns_keep]
        df = df[columns_keep]

        return ITable(caption="A table rendered with ITable", df=df,  scrollY="300px", scrollX=True, height="600px", paging=True, autoWidth=True, 
                     )

