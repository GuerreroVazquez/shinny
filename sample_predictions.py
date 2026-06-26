from shiny import ui, render
from itables.widget import ITable
from shinywidgets import render_widget, output_widget
from analysis import Analysis

samples_ui = ui.nav_panel(
    "Samples",
    output_widget("samples_table"),
)

def samples_server(input, output, session):
    @output
    @render_widget
    def samples_table():
        df = Analysis.sample_data.copy()
        df["Ridge_error"] = df["RidgeP"] - df["Age"]
        df["Catboost_error"] = df["CatboostP"] - df["Age"]
        cols = ["Sample", "Age", "Status", "RidgeP", "CatboostP", "Ridge_error", "Catboost_error"]
        return ITable(
            caption="Sample metadata, predicted ages, and prediction errors",
            df=df[cols],
            scrollY="400px", scrollX=True, height="600px", paging=True, autoWidth=True,
        )
