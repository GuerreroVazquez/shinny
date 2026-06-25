from shiny import ui, render, reactive, App
import pandas as pd
from ploting_profiles import plot_lfc
import matplotlib.pyplot as plt
from io import BytesIO
import base64


selected_genes_file = "data/selected_genes.txt"
with open(selected_genes_file, "r") as file:
    selected_genes = file.read().splitlines()

COLUMN_ALIASES = {
    "MO": "middle.vs.old",
    "male.vs.female_Young": "male.vs.female_young",
}

DISPLAY_ORDER = [
    "young.vs.middle",
    "middle.vs.old",
    "young.vs.old",
    "young.vs.middle_female",
    "middle.vs.old_female",
    "young.vs.old_female",
    "young.vs.middle_male",
    "middle.vs.old_male",
    "young.vs.old_male",
    "male.vs.female_young",
    "male.vs.female_middle",
    "male.vs.female_old",
]

DISPLAY_LABELS = {
    "young.vs.middle": "Young vs Middle Age",
    "middle.vs.old": "Middle Age vs Old",
    "young.vs.old": "Young vs Old",
    "young.vs.middle_female": "Young vs Middle Age (Female)",
    "middle.vs.old_female": "Middle Age vs Old (Female)",
    "young.vs.old_female": "Young vs Old (Female)",
    "young.vs.middle_male": "Young vs Middle Age (Male)",
    "middle.vs.old_male": "Middle Age vs Old (Male)",
    "young.vs.old_male": "Young vs Old (Male)",
    "male.vs.female_young": "Male vs Female (Young)",
    "male.vs.female_middle": "Male vs Female (Middle Age)",
    "male.vs.female_old": "Male vs Female (Old)",
}

lfc_data = pd.read_csv("data/lfc_from_dds.csv", index_col=0)
lfc_data.index.name = None

aliased_in_data = [c for c in lfc_data.columns if c in COLUMN_ALIASES]
if aliased_in_data:
    lfc_data = lfc_data.drop(columns=aliased_in_data)

lfc_data = lfc_data.reset_index().rename(columns={"index": "Symbol"})

columns_to_plot = [c for c in DISPLAY_ORDER if c in lfc_data.columns]
display_labels = [DISPLAY_LABELS.get(c, c) for c in columns_to_plot]

selected_set = set(selected_genes)
all_genes = sorted(lfc_data['Symbol'].unique())
gene_choices = {}
for g in all_genes:
    if g in selected_set:
        gene_choices[g] = f"★ {g}"
for g in all_genes:
    if g not in selected_set:
        gene_choices[g] = g

gene_lfc_ui = ui.nav_panel(
    "LogFoldChange",
    ui.input_selectize(
        "gene_lfc", 
        "Select Gene:", 
        choices=gene_choices,
    ),
    ui.output_plot("lfc_output"),
)

def gene_lfc_server(input, output, session):
    @output
    @render.plot
    def lfc_output():
        selected_gene = input.gene_lfc()

        if not selected_gene:
            return

        fig = plot_lfc(
            symbol=selected_gene,
            candidate_genes=lfc_data,
            columns_to_plot=columns_to_plot,
            labels=display_labels,
        )

        return fig


