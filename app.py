from shiny import App, ui
from welcome import welcome_ui
from selected_gene_table import gene_ui, gene_server
from sample_explorer import sample_ui, sample_server
from gene_lfc import gene_lfc_ui, gene_lfc_server
from catboost_validation import catboost_validation_ui, catboost_validation_server
from expression_violinBox import expression_ui, expression_server
from gene_influence import gene_influence_ui, gene_influence_server
from gsea_pathways import gsea_pathways_ui, gsea_pathways_server
from sample_predictions import samples_ui, samples_server
# Define the UI
app_ui = ui.page_fluid(
    ui.navset_pill(
        welcome_ui,
        samples_ui,
        gene_ui,
        #sample_ui,
        #sample_violin_ui,
        gene_lfc_ui,
        catboost_validation_ui,
        
        #shap_ui,
        expression_ui,
        gene_influence_ui,
        gsea_pathways_ui,

        id="tab",  # ID for the navigation set
    )
)

# Define the server logic
def server(input, output, session):
    # Call the Gene and Sample server logic
    gene_server(input, output, session)
    sample_server(input, output, session)
    #violin_server(input, output, session)
    gene_lfc_server(input, output, session)
    catboost_validation_server(input, output, session)
    samples_server(input, output, session)
    #shap_server(input, output, session)
    expression_server(input, output, session)
    gene_influence_server(input=input, output=output, session=session)
    gsea_pathways_server(input, output, session)

# Create the app
app = App(app_ui, server)
