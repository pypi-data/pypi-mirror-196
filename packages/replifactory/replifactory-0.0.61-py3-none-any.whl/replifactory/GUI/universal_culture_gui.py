import ipywidgets as widgets

from replifactory.culture.culture_universal import CultureUniversal


def highlight(self):
    self.box.layout.border = "2px solid red"
    self.box.layout.padding = "10px"
    self.label.style.font_weight = "bold"
    self.label.style.color = "red"


def unhighlight(self):
    self.box.layout.border = "1px solid gray"
    self.box.layout.padding = "6px"
    self.label.style.font_weight = "normal"
    self.label.style.color = "black"


class ChemostatBox:
    def __init__(self):
        self.label = widgets.Label(value="Chemostat")
        self.label.style.font_weight = "bold"
        self.box = widgets.VBox(
            layout=widgets.Layout(
                border="1px solid black", padding="10px", width="640px"
            ),
            children=[],
        )
        self.widget = widgets.VBox([self.label, self.box])
        self.parameter_style = {"description_width": "230px"}
        c = CultureUniversal()

        parameters = [
            k
            for k in c.__dict__.keys()
            if k
            in [
                "volume_max",
                "volume_dead",
                "volume_added_at_dilution",
                "dilution_delay",
                "dilution_trigger_od",
            ]
        ]

        parameters_widgets = [
            widgets.FloatText(
                value=c.__dict__[par],
                description=par,
                style=self.parameter_style,
                continuous_update=True,
            )
            for par in parameters
        ]
        parameters_box = widgets.VBox(parameters_widgets)
        self.box.children = [parameters_box]

    def highlight(self):
        highlight(self)

    def unhighlight(self):
        unhighlight(self)


# create the turbidostat box
class TurbidostatBox:
    def __init__(self):
        self.label = widgets.Label(value="Turbidostat")
        self.label.style.font_weight = "bold"
        self.chemostat_box = ChemostatBox()
        self.box = widgets.VBox(
            layout=widgets.Layout(
                border="1px solid black", padding="10px", width="680px"
            ),
            children=[self.chemostat_box.widget],
        )
        self.widget = widgets.VBox([self.label, self.box])
        parameter_style = self.chemostat_box.parameter_style
        c = CultureUniversal()
        parameters = [
            k
            for k in c.__dict__.keys()
            if k
            in [
                "dilution_trigger_od",
            ]
        ]

        parameters_widgets = [
            widgets.FloatText(
                value=c.__dict__[par],
                description=par,
                style=parameter_style,
                continuous_update=True,
            )
            for par in parameters
        ]
        parameters_box = widgets.VBox(parameters_widgets)
        self.box.children = [self.chemostat_box.widget, parameters_box]

    def highlight(self):
        unhighlight(self.chemostat_box)
        highlight(self)

    def unhighlight(self):
        unhighlight(self)


# create the morbidostat box
class MorbidostatBox:
    def __init__(self):
        self.label = widgets.Label(value="Morbidostat")
        self.label.style.font_weight = "bold"
        self.turbidostat_box = TurbidostatBox()
        self.chemostat_box = self.turbidostat_box.chemostat_box
        self.box = widgets.VBox(
            layout=widgets.Layout(
                border="1px solid black", padding="10px", width="720px"
            ),
            children=[self.turbidostat_box.widget],
        )
        self.widget = widgets.VBox([self.label, self.box])

        c = CultureUniversal()
        parameter_style = self.chemostat_box.parameter_style
        stress_increase_parameters = [
            k
            for k in c.__dict__.keys()
            if k
            in [
                "stress_increase_initial_dilution_number",
                "stress_increase_initial_dose",
                "stress_increase_ramp_factor",
                "stress_increase_delay_dilutions",
                "stress_increase_t_doubling_threshold",
            ]
        ]
        stress_increase_parameters_widgets = [
            widgets.FloatText(
                value=c.__dict__[par],
                description=par,
                style=parameter_style,
                continuous_update=True,
            )
            for par in stress_increase_parameters
        ]

        stress_decrease_parameters = [
            k
            for k in c.__dict__.keys()
            if k in ["no_growth_period_max", "no_growth_t_doubling_threshold"]
        ]
        stress_decrease_parameters_widgets = [
            widgets.FloatText(
                value=c.__dict__[par],
                description=par,
                style=parameter_style,
                continuous_update=True,
            )
            for par in stress_decrease_parameters
        ]
        stress_increase_box = widgets.VBox(
            children=[
                widgets.Label(value="Stress increase"),
                widgets.VBox(
                    stress_increase_parameters_widgets,
                    layout=widgets.Layout(
                        border="1px dashed gray", padding="10px", width="335px"
                    ),
                ),
            ]
        )
        stress_decrease_box = widgets.VBox(
            children=[
                widgets.Label(value="Stress decrease"),
                widgets.VBox(
                    stress_decrease_parameters_widgets,
                    layout=widgets.Layout(
                        border="1px dashed gray", padding="10px", width="335px"
                    ),
                ),
            ]
        )
        self.box.children = self.box.children + (
            widgets.HBox(
                [
                    stress_increase_box,
                    widgets.Output(layout=widgets.Layout(width="6px")),
                    stress_decrease_box,
                ]
            ),
        )

    def highlight(self):
        unhighlight(self.turbidostat_box)
        unhighlight(self.chemostat_box)
        highlight(self)

    def unhighlight(self):
        unhighlight(self)


mb = MorbidostatBox()
mb.widget
