from shiny import ui, render, reactive
import pandas as pd
from observe_prediction import observe_pred_ui, observe_pred_server
from observe_lead_genes import observe_lead_server, observe_lead_ui


sample_data = pd.read_csv("data/validation_sample_data.csv")
max_n = len(sample_data)

gene_influence_ui = ui.nav_panel(
    "SHAP",
    ui.input_select("model", "Model", choices=["Ridge", "Catboost"]),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_text("sample_index", "Sample:", value="1"),
            ui.input_text("actual_age", "Actual Age:", value="23"),
            ui.input_text("predicted_age", "Predicted Age:", value="21"),
            ui.input_text("sarcopenic", "Sarcopenic:", value="NO"),
            ui.input_text("sample_id", "Sample id:", value="SRR13759025"),
            ui.input_text("experiment", "Experiment:", value="GSE1767186"),
        ),
        ui.page_fluid(
            ui.navset_pill(
                observe_pred_ui,
                observe_lead_ui,
                id="geneInfluence",
            )
        )
    )
)

def gene_influence_server(input, output, session):
    observe_pred_server(input=input, output=output, session=session)
    observe_lead_server(input=input, output=output, session=session)

    @reactive.effect
    def update_sample():
        current_sample = input.sample_number()
        if type(current_sample) == int:
            if current_sample is None or current_sample < 1:
                current_sample = 1
        else:
            current_sample = 1

        sample_info = sample_data.loc[current_sample - 1]
        print(sample_info)
        model_name = input.model()

        ui.update_text("sample_index", value=str(current_sample))
        ui.update_text("actual_age", value=str(sample_info["Age"]))
        ui.update_text("predicted_age", value=str(sample_info[model_name + 'P']))
        ui.update_text("sarcopenic", value=str(sample_info["Status"]))
        ui.update_text("sample_id", value=str(sample_info["Sample"]))
        ui.update_text("experiment", value=str(sample_info["Experiment"]))
