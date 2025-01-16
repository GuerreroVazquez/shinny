from shiny import ui, render
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from shinywidgets import output_widget, render_widget  
from upsetplot import plot
from matplotlib import pyplot
from upsetplot import from_memberships
from upsetplot import from_contents

lfc_intersections_df = pd.read_csv("data/Intersection_Genes.csv")
choices = lfc_intersections_df.columns.tolist()
# UI for the Sample tab
upset_ui = ui.nav_panel(
    "DE Genes Intersections",
    #output_widget("boxplot_output")  # Widget to render the boxplot
    output_widget("upset_output"),
    ui.input_select(
        "set1", 
        "Select Comparison 1:", 
        choices=choices,  # Populate dropdown with gene options
    ),
    ui.input_select(
        "set2", 
        "Select Comparison 2:", 
        choices=choices,  # Populate dropdown with gene options
    ),
)

# Server logic for the Sample tab
def upset_server(input, output, session):
    @output
    @render_widget
    def upset_output():
        # Capture selected gene from dropdown
        upset_data = from_contents(lfc_intersections_df)
        fig = plot(upset_data, min_subset_size=15, show_counts=True)
        
        return fig


