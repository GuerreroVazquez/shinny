from shiny import App, ui
from selected_gene_table import gene_ui, gene_server
from sample_explorer import sample_ui, sample_server
from sample_violin import sample_violin_ui, violin_server
from gene_lfc import gene_lfc_ui, gene_lfc_server
from catboost_validation import catboost_validation_ui, catboost_validation_server

# Define the UI
app_ui = ui.page_fluid(
    ui.navset_pill(
        gene_ui,
        sample_ui,
        sample_violin_ui,
        gene_lfc_ui,
        catboost_validation_ui,
        id="tab",  # ID for the navigation set
    )
)

# Define the server logic
def server(input, output, session):
    # Call the Gene and Sample server logic
    gene_server(input, output, session)
    sample_server(input, output, session)
    violin_server(input, output, session)
    gene_lfc_server(input, output, session)
    catboost_validation_server(input, output, session)

# Create the app
app = App(app_ui, server)
