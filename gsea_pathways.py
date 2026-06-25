from shiny import ui, render, reactive
from functools import cache
import pandas as pd
import matplotlib.pyplot as plt
import os


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
def _merged_sig_terms(db):
    return _load(db, "merged_sig_terms_non_nan.csv")


@cache
def _terms_genes(db):
    p = f"{BASE_DIR}/{db}/terms_genes_{db}.csv"
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


@cache
def _lead_genes(db):
    p = f"{BASE_DIR}/{db}/significant_terms_lead_genes_{db}.csv"
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


@cache
def _genes_lab(db):
    p = f"{BASE_DIR}/{db}/genes_lab_pathways_{db}.csv"
    return pd.read_csv(p) if os.path.exists(p) else pd.DataFrame()


# --- Build samples list (samples with enriched terms) ---
def _samples_with_terms(db):
    df = _samples_term_df(db)
    return sorted(df.loc[df["Enriched_terms_count"] > 0, "Sample"].tolist())


# --- Plots ---

def _plot_term_frequencies(db, min_samples=1):
    pres = _term_presence(db)
    freq = pres.sum(axis=1).sort_values()
    freq = freq[freq >= min_samples]
    if freq.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No terms meet the frequency threshold", ha="center", va="center")
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


def _plot_sample_enrichment(db, sample):
    enf = _term_enrichment(db)
    if sample not in enf.columns:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, f"No enrichment data for {sample}", ha="center", va="center")
        return fig
    vals = enf[sample].dropna().sort_values()
    if vals.empty:
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.text(0.5, 0.5, "No enriched terms for this sample", ha="center", va="center")
        return fig
    colors = ["#0072B2" if v >= 0 else "#E69F00" for v in vals.values]
    fig, ax = plt.subplots(figsize=(8, max(3, len(vals) * 0.4)))
    ax.barh(range(len(vals)), vals.values, color=colors)
    ax.set_yticks(range(len(vals)))
    short = [t[:50] + "..." if len(t) > 50 else t for t in vals.index]
    ax.set_yticklabels(short)
    ax.set_xlabel("Enrichment Score (NES)")
    ax.set_title(f"Enriched Terms for {sample}")
    ax.axvline(0, color="gray", linewidth=0.5)
    plt.tight_layout()
    return fig


# --- UI ---

gsea_pathways_ui = ui.nav_panel(
    "GSEA Pathways",
    ui.page_sidebar(
        ui.sidebar(
            ui.input_selectize("gsea_db", "Database", DATABASES, selected=DATABASES[0]),
            ui.output_ui("gsea_sample_ui"),
            ui.input_slider("gsea_min_samples", "Min samples with term", 1, 30, 1),
        ),
        ui.navset_pill(
            ui.nav_panel(
                "Term Overview",
                ui.output_plot("gsea_term_freq_plot"),
                ui.output_table("gsea_term_table"),
            ),
            ui.nav_panel(
                "Sample Detail",
                ui.output_plot("gsea_sample_plot"),
                ui.output_table("gsea_sample_lead_genes"),
            ),
            ui.nav_panel(
                "Genes & Pathways",
                ui.markdown(
                    "Pathway annotations "
                    "based on the significant enriched terms."
                ),
                ui.output_table("gsea_genes_pathways"),
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
    @render.plot
    def gsea_term_freq_plot():
        return _plot_term_frequencies(_db(), input.gsea_min_samples())

    @output
    @render.table
    def gsea_term_table():
        db = _db()
        pres = _term_presence(db)
        freq = pres.sum(axis=1).sort_values(ascending=False)
        freq = freq[freq >= input.gsea_min_samples()]
        tg = _terms_genes(db)
        lg = _lead_genes(db)
        data = []
        for term in freq.index:
            n_genes = 0
            if not tg.empty and "Term" in tg.columns and "Genes" in tg.columns:
                match = tg[tg["Term"] == term]
                if not match.empty:
                    n_genes = len(match["Genes"].iloc[0].split(";"))
            n_lead = len(lg[lg["Term"] == term]) if not lg.empty else 0
            related = ""
            gl = _genes_lab(db)
            if not gl.empty:
                lab_genes = gl[gl["Pathway"] == term]["Gene"].tolist()
                related = ", ".join(lab_genes) if lab_genes else ""
            data.append({
                "Term": term,
                "Samples": int(freq[term]),
                "Genes": n_genes,
                "Lead entries": n_lead,
                "Selected genes": related,
            })
        return pd.DataFrame(data).head(50)

    @output
    @render.plot
    def gsea_sample_plot():
        sample = input.gsea_sample()
        if not sample:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.text(0.5, 0.5, "Select a sample from the sidebar", ha="center", va="center")
            return fig
        return _plot_sample_enrichment(_db(), sample)

    @output
    @render.table
    def gsea_sample_lead_genes():
        sample = input.gsea_sample()
        if not sample:
            return pd.DataFrame({"Info": ["Select a sample from the sidebar"]})
        lg = _lead_genes(_db())
        if lg.empty:
            return pd.DataFrame({"Info": ["No lead gene data available"]})
        sub = lg[lg["Sample"] == sample][["Term", "Lead_genes"]]
        sub.columns = ["Term", "Lead Genes"]
        return sub

    @output
    @render.table
    def gsea_genes_pathways():
        gl = _genes_lab(_db())
        if gl.empty:
            return pd.DataFrame({"Info": ["No pathway data for this database"]})
        return gl
