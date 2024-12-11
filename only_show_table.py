from shiny import App, ui, render
import pandas as pd
from itables import show  # Import itables for the interactive table
from itables.widget import ITable
from shinywidgets import render_widget

from shinywidgets import output_widget
import datatables
from datatable import Frame, as_type

# Define the UI
app_ui = ui.page_fluid(
    ui.h1("Dynamic File Viewer"),
    ui.input_file("file", "Upload your CSV file", accept=[".csv"]),
    #ui.output_ui("table_ui"),  # For itables output
    output_widget("table_w"),  # For itables output
    ui.output_table("table")   # For datatables output
)

# Define the server logic
def server(input, output, session):
    print("Server is running...")
    # For itables
    @output
    @render.ui  # Use render.ui to render the table with itables
    def table_ui():
        # Check if a file is uploaded
        if not input.file():
            return ui.p("Please upload a file to view it as a table.")

        # Read the uploaded file
        file_info = input.file()[0]
        df = pd.read_csv(file_info["datapath"])

        # Debugging: Log dataframe to ensure it's being read correctly
        print(f"DataFrame loaded for itables:\n{df.head()}")

        # Convert the Pandas DataFrame to an interactive table using itables
        return show(df, classes="display compact", scrollX=True)
    @output
    @render_widget  # Use render.table to render the table as a static DataFrame
    def table_w():
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
    # For datatables
    @output
    @render.table  # Use render.table to render the table as a static DataFrame
    def table():
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
        return df

# Create the app
app = App(app_ui, server)
