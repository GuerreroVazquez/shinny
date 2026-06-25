from shiny import ui, render
from ploting_profiles import prepare_box_plot_expression, prepare_violin_plot_expression
from data_cache import load_expression_data


with open("data/selected_genes.txt") as f:
    selected_genes = f.read().splitlines()

gene_choices = {g: f"★ {g}" for g in selected_genes}

expression_ui = ui.nav_panel(
    "Violin",
    ui.page_fluid(
        ui.page_sidebar(
            ui.sidebar(
                ui.input_selectize("gene_vb", "Gene", choices=gene_choices, options={"create": True}),
                ui.input_select("plot_type", "Plot", ["Violin Plot", "Box Plot"]),
                ui.input_checkbox("grouping", "Group by age group", True),
                ui.input_checkbox("split_sex", "Divide sex", False)
            ),
            ui.output_plot("ploting_plot")
        )
    )
)

def expression_server(input, output, session):
    @output
    @render.plot
    def ploting_plot():
        gene = input.gene_vb()
        plot_type = input.plot_type()
        grouping = input.grouping()
        split_sex = input.split_sex()
        gene_data = load_expression_data()

        if plot_type == "Violin Plot":
            fig = prepare_violin_plot_expression(gene_data=gene_data, gene=gene, age_group=grouping, sex_div=split_sex, save=None, plot=False, check_significance=True)
        elif plot_type == "Box Plot":
            fig = prepare_box_plot_expression(gene_data=gene_data, gene=gene, age_group=grouping, sex_div=split_sex, save=None, plot=False, check_significance=True)
        return fig
