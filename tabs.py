from shiny import App, ui, render
import pandas as pd
from itables.widget import ITable
from shinywidgets import render_widget, output_widget

# Define the UI
app_ui = ui.page_fluid(
    ui.navset_pill(  # Create the tabs
        ui.nav_panel(
            "Gene",
            ui.input_file("file", "Upload your Gene CSV file", accept=[".csv"]),
            output_widget("gene_table"),  # For the interactive gene table
        ),
        ui.nav_panel(
            "Sample",
            ui.p("Sample content will go here.")  # Placeholder for the Sample tab
        ),
        id="tab",  # ID for the navigation set
    )
)

# Define the server logic
def server(input, output, session):
    @output
    @render_widget
    def gene_table():
        # Check if a file is uploaded
        if not input.file():
            return pd.DataFrame({"Message": ["Please upload a file."]})

        # Read the uploaded file
        file_info = input.file()[0]
        df = pd.read_csv(file_info["datapath"])

        # Debugging: Log dataframe to ensure it's being read correctly
        print(f"DataFrame loaded for pandas table:\n{df.head()}")

        columns_keep = df.columns[:10]  # Limiting to the first 10 columns
        rows_keep = df.index[:10]      # Limiting to the first 10 rows
        df = df[columns_keep]
        df = df.loc[rows_keep]
        return ITable(caption="A table rendered with ITable", df=df)


# Create the app
app = App(app_ui, server)
