from shiny import ui, render
import pandas as pd
from ploting_profiles import plot_lfc
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget  


catboost_result_df = pd.read_csv("data/results_catboost.csv")
# UI for the Sample tab
catboost_validation_ui = ui.nav_panel(
    "Catboost_Validation",
    #output_widget("boxplot_output")  # Widget to render the boxplot
    output_widget("catboost_validation_output"),
)

# Server logic for the Sample tab
def catboost_validation_server(input, output, session):
    @output
    @render_widget
    def catboost_validation_output():
        # Capture selected gene from dropdown
        fig = px.scatter(catboost_result_df, x="Actual", y="Predicted", color="Experiment")

        
        return fig


