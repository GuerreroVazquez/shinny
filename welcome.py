from shiny import ui

welcome_ui = ui.nav_panel(
    "Welcome",
    ui.markdown(
        """
# Welcome to the Muscle Ageing Explorer

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

Ridge regression achieved an R² of 0.85
and an RMSE of 8.57 years and CatBoost an R² of 0.96 and an
RMSE of 6.90 years.

Genes selected for functional
validation in a *C. elegans* model of ageing. The rationale for gene
selection is detailed in the **Selected Genes** tab.

## Using This App

| Tab | Description |
|---|---|
| **Selected Genes** | Selected genes with the reason of the selection, orthologs, and tissue expression |
| **LogFoldChange** | Log₂ fold changes across age and sex comparisons |
| **Violin** | Gene expression distributions by age group and sex |
| **Catboost_Validation** | Model validation results |
| **SHAP** | Feature importance and individual predictions (Ridge and CatBoost) and the cell type specificity of leading genes |
"""
    ),
)
