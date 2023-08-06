import ipywidgets as widgets
from IPython.core.display import clear_output, display
from ipywidgets import HBox, Layout, VBox

from replifactory.culture.plotting import CommonPlotterWidget


class CulturePlotWidget:
    def __init__(self, main_gui, vial_number):
        self.main_gui = main_gui
        self.title = widgets.HTML(
            "<b>Vial %d:</b>" % vial_number, layout=Layout(width="40px", height="40px")
        )
        self.vial_number = vial_number
        self.last_hours = widgets.IntText(
            description="time window",
            description_tooltip="hours before the last OD measurement",
            value=24,
            style={"description_width": "80px"},
            layout=Layout(width="135px"),
        )
        self.plot_growth_rate = widgets.Checkbox(
            description="plot doubling time",
            description_tooltip="takes a longer time than just plotting the OD",
            value=False,
            indent=False,
            layout=Layout(width="135px"),
        )
        self.output = widgets.Output(layout=Layout(width="1200px"))
        self.button = widgets.Button(description="plot", icon="fa-chart-line")
        self.button.on_click(self.handle_plot_button_click)
        config = HBox(
            [self.title, self.button, self.last_hours, self.plot_growth_rate],
            layout=Layout(width="600px"),
        )
        self.widget = VBox([config, self.output])

    def handle_plot_button_click(self, b):
        self.button.disabled = True
        self.button.description = "plotting..."
        try:
            with self.output:
                c = self.main_gui.experiment.device.cultures[self.vial_number]
                fig = c.plot(
                    last_hours=self.last_hours.value,
                    plot_growth_rate=self.plot_growth_rate.value,
                )
                clear_output()
                display(fig)
        finally:
            self.button.description = "plot"
            self.button.disabled = False


class ExperimentPlotTab:
    title = "Graph"

    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.culture_plots = [
            CulturePlotWidget(main_gui=main_gui, vial_number=v) for v in range(1, 8)
        ]
        self.plots = [culture_plot.widget for culture_plot in self.culture_plots]
        self.plot_all = widgets.Button(
            description="plot all vials", icon="fa-chart-area"
        )
        self.plot_all.on_click(self.handle_plot_all_button)
        self.common_plot = CommonPlotterWidget(self.main_gui)

        self.widget = VBox([self.common_plot.widget, self.plot_all, VBox(self.plots)])

    def handle_plot_all_button(self, button):
        button.disabled = True
        for culture_plot in self.culture_plots:
            culture_plot.button.click()
        button.disabled = False
