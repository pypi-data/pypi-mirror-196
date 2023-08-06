import glob
import os

import ipywidgets as widgets
from IPython.display import clear_output, display
from ipywidgets import HBox, Layout, VBox

from replifactory.device.base_device import BaseDevice
from replifactory.util.experiment import Experiment
from replifactory.GUI.device_control_widgets import DeviceControl
from replifactory.GUI.device_tab import get_ftdi_addresses

# class ExperimentWidget:
#     def __init__(self, status_bar):
#         self.status_bar = status_bar
#         print("output made")
#         with self.status_bar.output:
#             self.status_bar.main_gui.experiment = Experiment("NewExperiment")
#         # if self.status_bar.main_gui.experiment is not None:
#         #     with self.status_bar.output:
#         #         self.status_bar.main_gui.experiment.status()
# box_layout = Layout(display='flex',
#                     flex_flow='column',
#                     align_items='stretch',
#                     border='solid 1px gray', )


class SetupMenu:
    layout_width = "350px"

    # config_paths = glob.glob("../**/device_config.yaml", recursive=True)
    # config_paths = [os.path.relpath(os.path.join(p, "..")) for p in config_paths]
    # experiment_directories = glob.glob("../**/main_run.log", recursive=True)
    # experiment_directories = [os.path.relpath(os.path.join(p, "..")) for p in experiment_directories]

    def __init__(self, main_gui):
        self.main_gui = main_gui
        style = {"description_width": "70px", "align": "left"}
        self.refresh_button = widgets.Button(
            icon="fa-sync-alt",
            tooltip="Refresh lists",
            button_style="info",
            layout=Layout(width="35px"),
        )
        self.refresh_button.on_click(self.handle_refresh_button)
        dropdown_layout = Layout(width="200px")

        self.experiment_directory_dropdown = widgets.Dropdown(
            options=[],
            description="directory",
            style=style,
            layout=dropdown_layout,
            index=None,
        )
        self.device_address_dropdown = widgets.Dropdown(
            description="Device",
            options=get_ftdi_addresses(),
            style=style,
            layout=dropdown_layout,
            tooltip="device address",
        )

        self.experiment_new_button = widgets.Button(
            tooltip="new experiment", icon="fa-folder-plus", layout=Layout(width="35px")
        )
        self.experiment_new_button.on_click(self.handle_new_experiment)
        self.experiment_directory_dropdown.observe(
            self.handle_experiment_folder_choice, names="value"
        )

        self.device_link_button = widgets.Button(
            tooltip="link device", icon="fa-link", layout=Layout(width="35px")
        )
        # self.reset_connection_button = widgets.Button(tooltip="reset connections", button_style="warning",
        #                                               icon="fa-retweet")
        # self.reset_connection_button.on_click(self.handle_connection_reset_button)
        self.device_valid = widgets.Button(
            description="",
            icon="fa-times",
            disabled=True,
            value=False,
            button_style="danger",
            layout=Layout(width="35px"),
            tooltip="device not connected",
        )
        self.experiment_valid = widgets.Button(
            description="",
            icon="fa-times",
            disabled=True,
            value=False,
            button_style="danger",
            layout=self.device_valid.layout,
            tooltip="no experiment selected",
        )

        self.device_link_button.on_click(self.handle_connect_button)

        self.device_check_button = widgets.Button(
            description="TEST", icon="fa-clipboard-check"
        )
        self.experiment_run_button = widgets.Button(
            description="RUN", icon="fa-play", disabled=True
        )
        self.experiment_stop_button = widgets.Button(
            description="STOP", icon="fa-stop", disabled=True
        )

        self.device_check_button.on_click(self.handle_check_button)
        self.experiment_run_button.on_click(self.handle_run_button)
        self.experiment_stop_button.on_click(self.handle_stop_button)

        self.input = None

        self.head = widgets.Accordion(
            titles=("Setup",),
            children=[widgets.Output()],
            layout=Layout(width=self.layout_width),
            selected_index=0,
        )

        self.clear_output_button = widgets.Button(
            description="clear output", icon="fa-eraser"
        )
        self.clear_output_button.on_click(self.handle_clear_output_button)
        self.output = widgets.Output()
        self.output.layout.width = "340px"
        self.output.layout.height = "500px"

        self.widget = VBox([self.head, self.clear_output_button, self.output])

        self.update_experiment_directories()
        self.update()

    def check_device_valid(self):
        if self.main_gui.device is None:
            self.change_device_valid(False)
            return
        if self.main_gui.device.is_connected():
            self.change_device_valid(True)
        else:
            self.change_device_valid(False)

    def update_buttons(self):
        self.check_experiment_valid()
        self.check_device_valid()

    def update(self):
        self.update_buttons()
        widget_list = [
            self.refresh_button,
            HBox(
                [
                    self.experiment_valid,
                    self.experiment_directory_dropdown,
                    self.experiment_new_button,
                ]
            ),
            # self.reset_connection_button,
            HBox(
                [
                    self.device_valid,
                    self.device_address_dropdown,
                    self.device_link_button,
                ]
            ),
            # self.fit_calibration_button,
            self.device_check_button,
            HBox([self.experiment_run_button, self.experiment_stop_button]),
        ]
        self.head.children = [VBox(widget_list)]

    # def ask_question(self, question):
    #     input_label = widgets.Label("How can i help you? ")
    #     input_text = widgets.Text()

    def handle_refresh_button(self, button):
        with self.output:
            self.disable_all()
            # if self.main_gui.device:
            #     if not self.main_gui.device.is_connected():
            #         self.reset_connection_button.click()
            self.update_ftdi_addresses()
            self.update_experiment_directories()
            self.enable_all()
            self.update()

    def handle_connect_button(self, button):
        self.disable_all()
        self.device_link_button.disabled = True
        icon0 = self.device_link_button.icon
        self.device_link_button.icon = "fa-spinner"
        try:
            self.connect_device_to_gui()
            if self.main_gui.device.is_connected():
                self.change_device_valid(True)
                self.enable_all()
                return
        except Exception:
            pass
        finally:
            self.device_link_button.icon = icon0
        self.change_device_valid(False)
        self.enable_all()

    def change_experiment_valid(self, ok=True):
        if ok:
            self.experiment_valid.button_style = "success"
            self.experiment_valid.icon = "fa-check"
            self.experiment_valid.tooltip = "experiment selected"
        else:
            self.experiment_valid.button_style = "danger"
            self.experiment_valid.icon = "fa-times"
            self.experiment_valid.tooltip = "no experiment selected"

    def change_device_valid(self, ok=True):
        if ok:
            self.device_valid.icon = "fa-check"
            self.device_valid.button_style = "success"
            self.device_valid.tooltip = "device connected"
        else:
            self.device_valid.icon = "fa-times"
            self.device_valid.button_style = "danger"
            self.device_valid.tooltip = "device not connected"

    # def handle_connection_reset_button(self, button):
    #     self.connect_button.disabled=True
    #     if self.main_gui.device:
    #         self.main_gui.device.disconnect_all()
    #
    #     # self.control_widget = DeviceControl(None).widget
    #     # self.update_ftdi_addresses()
    #     self.reset_connection_button.icon = "fa-retweet"
    #     self.connect_button.disabled = False
    #     self.connect_button.button_style = ""
    #     self.connect_button.icon = "fa-link"

    def connect_device_to_gui(self):
        self.disable_all()
        if self.main_gui.device:
            self.main_gui.device.disconnect_all()
        self.main_gui.device_tab.control_widget = DeviceControl(
            None, self.main_gui
        ).widget
        with self.output:
            clear_output()
            # self.update()

            if self.main_gui.device is not None:
                self.main_gui.device.connect(
                    ftdi_address=self.device_address_dropdown.value
                )
            else:
                self.main_gui.device = BaseDevice(
                    ftdi_address=self.device_address_dropdown.value
                )
                self.main_gui.device.connect()
            # if self.config_path.value is not None:
            #     self.main_gui.device.load_calibration(config_path=self.config_path.value)
            self.main_gui.device_tab.control_widget = DeviceControl(
                self.main_gui.device, self.main_gui
            ).widget
            self.main_gui.device_tab.update()
        self.enable_all()
        self.main_gui.update()

    def handle_clear_output_button(self, b):
        with self.output:
            clear_output()

    def update_experiment_directories(self):
        experiment_directories = glob.glob("../**/main_run.log", recursive=True)
        experiment_directories = [
            os.path.relpath(os.path.join(p, "..")) for p in experiment_directories
        ]
        experiment_directories = [os.path.relpath(p) for p in experiment_directories]
        self.disable_all()
        self.experiment_directory_dropdown.unobserve_all()
        self.experiment_directory_dropdown = widgets.Dropdown(
            options=experiment_directories,
            description="Experiment",
            style=self.device_address_dropdown.style,
            layout=self.device_address_dropdown.layout,
            index=None,
        )
        self.experiment_directory_dropdown.options = experiment_directories
        if hasattr(self.main_gui, "experiment"):
            if self.main_gui.experiment:
                if self.main_gui.experiment.directory:
                    self.experiment_directory_dropdown.index = (
                        self.experiment_directory_dropdown.options.index(
                            os.path.relpath(self.main_gui.experiment.directory)
                        )
                    )
        self.experiment_directory_dropdown.observe(
            self.handle_experiment_folder_choice, names="value"
        )
        self.enable_all()

    def disable_all(self):
        self.device_check_button.disabled = True
        self.experiment_directory_dropdown.disabled = True
        self.experiment_new_button.disabled = True
        self.device_address_dropdown.disabled = True
        self.device_link_button.disabled = True
        # self.reset_connection_button.disabled = True

    def enable_all(self):
        self.device_check_button.disabled = False
        self.experiment_directory_dropdown.disabled = False
        self.experiment_new_button.disabled = False
        self.device_address_dropdown.disabled = False
        self.device_link_button.disabled = False
        # self.reset_connection_button.disabled = False

    def update_ftdi_addresses(self):
        self.device_address_dropdown.options = get_ftdi_addresses()

    def handle_check_button(self, b):
        with self.output:
            clear_output()
            assert not self.main_gui.experiment.is_running()
            self.main_gui.experiment.device.run_self_test()
            self.experiment_run_button.disabled = False

    def handle_run_button(self, b):
        with self.output:
            clear_output()
            self.main_gui.experiment.run()
            self.experiment_run_button.disabled = True
            self.experiment_stop_button.disabled = False
            # self.update()

    def handle_stop_button(self, b):
        with self.output:
            clear_output()
            self.main_gui.experiment.stop()
            self.experiment_stop_button.disabled = True
            self.experiment_run_button.disabled = False
            # self.update()

    # def update(self):
    #     # self.update_experiment_directories()
    #     # self.update_ftdi_addresses()
    #     widget_list = [self.refresh_button,
    #                    HBox([self.experiment_directory_dropdown, self.new_experiment_button]),
    #                    HBox([self.ftdi_address, self.connect_button, self.reset_connection_button]),
    #                    # self.fit_calibration_button,
    #                    self.check_button, HBox([self.run_button, self.stop_button])]
    #     self.head.children = [VBox(widget_list)]
    #
    #     # self.main_gui.reload_setup_menu_widget()

    def handle_new_experiment(self, b):
        # if self.main_gui.device is None:
        #     with self.output:
        #         print("PLEASE CONNECT DEVICE TO CREATE NEW EXPERIMENT!")
        # else:

        with self.output:
            clear_output()
            self.q = widgets.Text(
                description="new directory:",
                style={"description_width": "initial"},
                continuous_update=False,
            )
            b = widgets.Button(description="create directory")
            display(VBox([self.q, b]))
            b.on_click(self.make_new_exp_folder)

    def make_new_exp_folder(self, change):
        directory = self.q.value
        with self.output:
            print("Creating new experiment")
            self.main_gui.experiment = Experiment(directory)
            self.main_gui.experiment.device.make_all_blank_cultures()
            self.main_gui.experiment_program_tab.update()
            # self.reset_connection_button.click()
        self.update_experiment_directories()

    def handle_experiment_folder_choice(self, change):
        self.disable_all()
        directory = change.new
        with self.output:
            clear_output()
            self.main_gui.experiment = Experiment(directory)
        self.main_gui.experiment_program_tab.update()
        self.refresh_button.click()
        self.check_experiment_valid()

    def check_experiment_valid(self):
        if not self.main_gui.experiment:
            self.change_experiment_valid(ok=False)
            return
        if self.main_gui.experiment.directory:
            self.change_experiment_valid(ok=True)


class InputWidget:
    def __init__(self, q):
        self.name = q
        self.input = widgets.FloatText(
            description=q, style={"description_width": "initial"}
        )
        self.submit = widgets.Button(description="submit")
        self.widget = HBox([self.input, self.submit])


class UserInputFloat:
    def __init__(self, setup_menu, question, action=None):
        self.setup_menu = setup_menu
        self.question = question
        self.action = action
        with self.setup_menu.output:
            clear_output()
            q = widgets.FloatText(description=question, continuous_update=False)
            display(q)
        q.observe(self.on_answer, names="value")

    def on_answer(self, change):
        with self.setup_menu.output:
            clear_output()
            print(self.question, "\nuser input:", change.new)
            if self.action is callable:
                self.action(change.new)


class UserInputText:
    def __init__(self, setup_menu, question, action=None):
        self.setup_menu = setup_menu
        self.question = question
        self.action = action
        with self.setup_menu.output:
            clear_output()
            q = widgets.Text(description=question, continuous_update=False)
            display(q)
        q.observe(self.on_answer, names="value")

    def on_answer(self, change):
        with self.setup_menu.output:
            clear_output()
            print(self.question, "\nuser input:", change.new)
            if self.action is callable:
                print("calling")
                self.action(change.new)


class UserInputConfirm:
    def __init__(self, setup_menu, question, action=None):
        self.setup_menu = setup_menu
        self.question = question
        self.action = action
        with self.setup_menu.output:
            clear_output()
            y = widgets.Button(description="Yes", button_style="success")
            n = widgets.Button(description="No", button_style="danger")
            q = HBox([y, n])
            display(q)
        y.on_click(self.on_yes)
        n.on_click(self.on_no)

    def on_yes(self, button):
        with self.setup_menu.output:
            clear_output()
            print("yass")

    def on_no(self, button):
        with self.setup_menu.output:
            clear_output()
            print("nope")
