import ipywidgets as widgets
from ipywidgets import HBox, Layout

from replifactory.GUI.camera_widgets import CameraTab
from replifactory.GUI.device_tab import DeviceTab
from replifactory.GUI.experiment_program_tab import ExperimentProgramTab
from replifactory.GUI.graph_tab import ExperimentPlotTab
from replifactory.GUI.setup_menu import SetupMenu
from replifactory.GUI.status_tab import StatusTab

# from replifactory.GUI.calibration_widgets import CalibrationTab
# from IPython.display import display


# def open_gui():
#     global _main_gui
#     if "_main_gui" in globals().keys():
#         display(_main_gui.widget)
#     else:
#         gui = MainGuiBuilder()
#         display(gui.widget)
#     rf.gui = _main_gui


class ExperimentTab:
    title = "Experiment"

    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.widget = widgets.Tab()
        self.program_tab = self.main_gui.experiment_program_tab
        self.status_tab = self.main_gui.experiment_status_tab
        self.plot_tab = self.main_gui.experiment_plot_tab
        self.widget.children = [
            self.program_tab.widget,
            self.status_tab.widget,
            self.plot_tab.widget,
        ]
        self.widget.set_title(0, "Program")
        self.widget.set_title(1, "Status")
        self.widget.set_title(2, "Plot")

    def update(self):
        self.widget.children = [
            self.program_tab.widget,
            self.status_tab.widget,
            self.plot_tab.widget,
        ]


class MainGuiBuilder:
    def __init__(self):
        global _main_gui
        if "_main_gui" in globals().keys():
            q = input("initialize new GUI?[y/n]")
            if q == "y":
                _main_gui = self
            else:
                raise RuntimeError("Existing GUI was NOT overwritten by new GUI")
        self._device = None
        self._experiment = None
        # self.calibration_tab = CalibrationTab(main_gui=self)
        self.setup_menu = SetupMenu(main_gui=self)

        self.device_tab = DeviceTab(main_gui=self)

        self.experiment_program_tab = ExperimentProgramTab(main_gui=self)
        self.experiment_status_tab = StatusTab(main_gui=self)
        self.experiment_plot_tab = ExperimentPlotTab(main_gui=self)
        self.experiment_tab = ExperimentTab(main_gui=self)

        self.camera_tab = CameraTab()

        self.tab_list = [self.experiment_tab, self.device_tab, self.camera_tab]
        self.tabs = widgets.Tab()

        self.widget = HBox([self.setup_menu.widget, self.tabs])
        self.update()
        _main_gui = self

        width = "800px"
        height = "1000px"
        # self.experiment_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap", display="flex",align_content="flex-start")
        # self.device_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap row", display="flex",align_content="flex-start")
        # # self.calibration_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap row", display="flex", align_content="flex-start")
        # self.experiment_status_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap row", display="flex", align_content="flex-start")
        # self.experiment_plot_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap", display="flex", align_content="flex-start")
        # self.camera_tab.widget.layout = Layout(height=height, width=width, flex_flow="wrap", display="flex", align_content="flex-start")
        for tab in self.tab_list:
            tab.widget.layout = Layout(
                height=height,
                width=width,
                flex_flow="wrap",
                display="flex",
                align_content="flex-start",
            )
        self.update()

    def update(self):
        # self.setup_menu.update()
        # self.reload_setup_menu_widget()
        if hasattr(self, "tabs"):
            self.experiment_tab.update()
            self.tabs.children = [tab.widget for tab in self.tab_list]

            for i in range(len(self.tab_list)):
                self.tabs.set_title(i, self.tab_list[i].title)
            for c in self.tabs.children:
                c.layout = widgets.Layout(width="800px")
            if hasattr(self, "setup_menu"):
                self.widget.children = (self.setup_menu.widget, self.tabs)

    # def reload_setup_menu_widget(self):
    #     if hasattr(self, "setup_menu"):
    #         self.widget.children = (self.setup_menu.widget, self.tabs)
    #     # self.widget = HBox([self.status_bar.widget, self.tabs])

    @property
    def device(self):
        if self.experiment is None:
            return self._device
        else:
            return self.experiment.device

    @device.setter
    def device(self, device):
        if self.experiment is not None:
            if device is not None:
                # if device.directory is None:
                #     device.directory = self.experiment.directory

                self.experiment.device = device
        self._device = device
        # if device is not None:
        #     self.calibration_tab.update()

    @property
    def experiment(self):
        return self._experiment

    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment
        if self._device is not None:
            self.experiment.device = self._device
            print("New device associated with experiment, but not initialized")
        # if self.experiment.device is not None:
        # # self.device = self.experiment.device
        # # if self.device.__class__ in self.device_tab.device_class.options:
        # #     self.device_tab.device_class.index = self.device_tab.device_class.options.index(self.device.__class__)
        # # else:
        # #     print("Experiment config device class unknown.")
        # # if self.device.ftdi_address in self.device_tab.ftdi_address.options:
        # #     self.device_tab.ftdi_address.index = self.device_tab.ftdi_address.options.index(self.device.ftdi_address)
        # # else:
        # #     print("Experiment config FTDI address does not match connected devices.")
        # # config_paths = [p for p in self.status_bar.config_path.options if
        # #                 os.path.realpath(p).startswith(os.path.realpath(self.device.directory))]
        # # if len(self.status_bar.config_paths) > 0:
        # #     self.device_tab.config_path.index = self.device_tab.config_path.options.index(config_paths[0])
        # # else:
        # #     print("Experiment config device directory unknown.")
        #
        # else:
