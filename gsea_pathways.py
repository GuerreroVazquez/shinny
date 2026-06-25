from shiny import ui, render, reactive
from functools import cache
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from itables.widget import ITable
from shinywidgets import render_widget, output_widget


BASE_DIR = "data/pers_pathways"
DATABASES = [
    "GO_Biological_Process_2023",
    "GO_Molecular_Function_2023",
    "KEGG_2021_Human",
]


def _load(db, filename, **kwargs):
    return pd.read_csv(f"{BASE_DIR}/{db}/{filename}", **kwargs)


@cache
def _samples_term_df(db):
    return _load(db, "samples_and_term_df.csv", index_col=0)


@cache
def _term_presence(db):
    return _load(db, "terms_sample_presence_df.csv", index_col=0)


@cache
def _term_enrichment(db):
    return _load(db, "terms_sample_enrichment_scores_pval_0.2.csv", index_col=0)


@cache
def _lead_genes(db):
    p = f"{BASE_DIR}/{db}/significant_terms_lead_genes_{db}.csv"
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


@cache
def _genes_ml(db):
    p = f"{BASE_DIR}/{db}/genes_lab_pathways_{db}.csv"
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


@cache
def _samples_terms_json(db):
    p = f"{BASE_DIR}/{db}/all_samples_terms.json"
    if not os.path.exists(p):
        return {}
    with open(p) as f:
        return json.load(f)


def _samples_with_terms(db):
    df = _samples_term_df(db)
    return sorted(df.loc[df["Enriched_terms_count"] > 0, "Sample"].tolist())


def _terms_for_sample(db, sample):
    data = _samples_terms_json(db)
    terms = data.get(sample, [])
    return [
        t for t in terms
        if os.path.exists(_gsea_svg_path(db, sample, t))
    ]


def _gsea_svg_path(db, sample, term):
    fname = f"GSEA_plot_{term.replace('/', '_').replace(' ', '_')}.svg"
    return f"{BASE_DIR}/{db}/{sample}/{fname}"


# --- Plots ---

def _plot_term_frequencies(db, min_samples=1):
    pres = _term_presence(db)
    freq = pres.sum(axis=1).sort_values()
    freq = freq[freq >= min_samples]
    if freq.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No terms meet the frequency threshold",
                ha="center", va="center", transform=ax.transAxes)
        return fig
    fig, ax = plt.subplots(figsize=(8, max(4, len(freq) * 0.35)))
    ax.barh(range(len(freq)), freq.values, color="#0072B2")
    ax.set_yticks(range(len(freq)))
    short = [t[:50] + "..." if len(t) > 50 else t for t in freq.index]
    ax.set_yticklabels(short)
    ax.set_xlabel("Samples (count)")
    ax.set_title("Term Frequency Across Samples")
    plt.tight_layout()
    return fig


# --- ORA SVG path ---

def _ora_svg_path(db):
    p = f"{BASE_DIR}/{db}/ora_results_top10.svg"
    return p if os.path.exists(p) else None


# --- ITable builder ---

def _it(data):
    if data.empty:
        return ITable(df=data, scrollY="200px")
    return ITable(df=data, scrollY="400px", scrollX=True, paging=True, autoWidth=True)


# --- UI ---

gsea_pathways_ui = ui.nav_panel(
    "GSEA Pathways",
    ui.page_sidebar(
        ui.sidebar(
            ui.input_selectize("gsea_db", "Database", {db: db.replace("_", " ") for db in DATABASES}, selected=DATABASES[0]),
        ),
        ui.navset_pill(
            ui.nav_panel(
                "General",
                ui.navset_pill(
                    ui.nav_panel(
                        "ORA",
                        ui.h4("Over-Representation Analysis (SHAP genes)"),
                        ui.output_ui("gsea_ora_plot"),
                    ),
                    ui.nav_panel(
                        "Term Frequency",
                        ui.output_ui("gsea_min_samples_ui"),
                        ui.output_plot("gsea_term_freq_plot"),
                    ),
                    ui.nav_panel(
                        "Leading Genes",
                        ui.markdown(
                            "Pathway mapping for the 9 ML-selected genes "
                            "based on significant enriched terms from "
                            "per-sample GSEA using SHAP values as ranking."
                        ),
                        output_widget("gsea_genes_pathways"),
                    ),
                ),
            ),
            ui.nav_panel(
                "Sample Analysis",
                ui.output_ui("gsea_sample_ui"),
                ui.output_ui("gsea_sample_gsea_plots"),
                output_widget("gsea_sample_lead_genes"),
            ),
        ),
    ),
)


# --- Server ---

def gsea_pathways_server(input, output, session):

    @reactive.Calc
    def _db():
        return input.gsea_db()

    @output
    @render.ui
    def gsea_sample_ui():
        samples = _samples_with_terms(_db())
        return ui.input_selectize("gsea_sample", "Sample", choices=samples, selected=None)

    @output
    @render.ui
    def gsea_sample_gsea_plots():
        sample = input.gsea_sample()
        if not sample:
            return ui.p("Select a sample above")
        terms = _terms_for_sample(_db(), sample)
        if not terms:
            return ui.p("No GSEA plots available for this sample.")
        items = []
        for term in terms:
            path = _gsea_svg_path(_db(), sample, term)
            if not os.path.exists(path):
                continue
            with open(path) as f:
                svg = f.read()
            items.append(
                ui.div(
                    ui.h5(term, style="margin-top: 1.5em;"),
                    ui.HTML(svg),
                )
            )
        return ui.div(*items)

    @output
    @render.ui
    def gsea_ora_plot():
        path = _ora_svg_path(_db())
        if not path:
            return ui.p("ORA results not available for this database.")
        with open(path) as f:
            svg = f.read()
        return ui.HTML(svg)

    @output
    @render.ui
    def gsea_min_samples_ui():
        db = _db()
        pres = _term_presence(db)
        freq = pres.sum(axis=1)
        max_val = int(freq.max()) if not freq.empty else 1
        return ui.input_slider("gsea_min_samples", "Min samples with term", 1, max_val, 1)

    @output
    @render.plot
    def gsea_term_freq_plot():
        return _plot_term_frequencies(_db(), input.gsea_min_samples())

    @output
    @render_widget
    def gsea_sample_lead_genes():
        sample = input.gsea_sample()
        if not sample:
            return _it(pd.DataFrame({"Info": ["Select a sample above"]}))
        lg = _lead_genes(_db())
        if lg.empty:
            return _it(pd.DataFrame({"Info": ["No lead gene data available"]}))
        sub = lg[lg["Sample"] == sample][["Term", "Lead_genes"]]
        sub.columns = ["Term", "Lead Genes"]
        return _it(sub)

    @output
    @render_widget
    def gsea_genes_pathways():
        gm = _genes_ml(_db())
        if gm.empty:
            return _it(pd.DataFrame({"Info": ["No pathway data for this database"]}))
        return _it(gm)
