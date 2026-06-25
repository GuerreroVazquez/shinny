from shiny import ui

welcome_ui = ui.nav_panel(
    "Welcome",
    ui.div(
        {"style": "max-width: 850px; margin: 30px auto; padding: 0 20px;"},
        ui.h1("Welcome to the Muscle Ageing Explorer",
              class_="text-center mb-4"),
        ui.markdown(
            """
This Shiny application accompanies the study on
molecular signatures of skeletal muscle ageing.

## About the Study

We analysed RNA-Seq data from six independent experiments comprising
270 human muscle samples (Vastus lateralis) to identify the molecular
mechanisms driving muscle ageing across three age groups:
Young (18–35), Middle Age (35–65), and Old (65+).

Both linear (Ridge regression) and non-linear (CatBoost) models were
developed to predict chronological age from gene expression profiles and
personalised gene expression profiles.

Genes selected for functional
validation in a *C. elegans* model of ageing. The rationale for gene
selection is detailed in the **Selected Genes** tab.
"""
        ),
        ui.hr(),
        ui.h4("Model Performance (90:10 train–test split)"),
        ui.HTML(
            """
<div style="display:flex; gap:20px; margin:15px 0 25px 0;">
  <div style="flex:1; padding:12px 18px; background:#eef7fb;
              border-left:4px solid #0072B2; border-radius:4px;">
    <strong>CatBoost</strong> (non-linear)<br>
    R² = 0.96 &middot; RMSE = 6.90 years
  </div>
  <div style="flex:1; padding:12px 18px; background:#fdf6ee;
              border-left:4px solid #E69F00; border-radius:4px;">
    <strong>Ridge</strong> (linear)<br>
    R² = 0.85 &middot; RMSE = 8.57 years
  </div>
</div>
"""
        ),
        ui.h4("Using This App"),
        ui.HTML(
            """
<table class="table table-bordered" style="width:100%;">
  <thead class="table-dark">
    <tr><th style="width:25%">Tab</th><th>Description</th></tr>
  </thead>
  <tbody>
    <tr><td>Selected Genes</td><td>Selected genes with the reason of the selection, orthologs, and tissue expression</td></tr>
    <tr><td>LogFoldChange</td><td>Log₂ fold changes across age and sex comparisons</td></tr>
    <tr><td>Violin</td><td>Gene expression distributions by age group and sex</td></tr>
    <tr><td>Catboost_Validation</td><td>Model validation results</td></tr>
    <tr><td>SHAP</td><td>Feature importance and individual predictions (Ridge and CatBoost) and the cell type specificity of leading genes</td></tr>
  </tbody>
</table>
"""
        ),
    ),
)
