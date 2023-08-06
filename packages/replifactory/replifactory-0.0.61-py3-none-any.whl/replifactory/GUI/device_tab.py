import inspect

import ipywidgets as widgets
import pyftdi.ftdi
from IPython.display import clear_output
from pyftdi.usbtools import UsbTools

from replifactory.culture.morbidostat import MorbidostatCulture
from replifactory.culture.turbidostat import TurbidostatCulture
from replifactory.device.base_device import BaseDevice
from replifactory.GUI.calibration_widgets import CalibrationTab
from replifactory.GUI.device_control_widgets import DeviceControl
from replifactory.GUI.hardware_testing_widgets import HardwareTestGUI

import logging


class DeviceTab:
    def __init__(self, main_gui):
        self.title = "Device"
        # config_paths = glob.glob("../**/device_config.yaml", recursive=True)
        # self.config_paths = [os.path.relpath(p) for p in config_paths]
        # self.experiment_directories = [os.path.relpath(os.path.join(p, "..")) for p in self.main_gui.status_bar.]

        self.main_gui = main_gui
        self.setup_menu = main_gui.setup_menu
        # self.device_class = widgets.Dropdown(description="*CLASS", options=get_device_classes())
        self.ftdi_address = widgets.Dropdown(
            description="*ADDRESS", options=get_ftdi_addresses()
        )
        # self.config_path = widgets.Dropdown(description="CALIBRATION", options=self.config_paths, index=None)
        self.connect_button = widgets.Button(description="link device", icon="fa-link")
        self.reset_connection_button = widgets.Button(
            description="reset connections", button_style="danger", icon="fa-retweet"
        )
        self.reset_connection_button.on_click(self.handle_connection_reset_button)
        self.connect_button.on_click(self.handle_connect_button)
        self.control_widget = DeviceControl(None, self.main_gui)
        self.calibration_tab = None
        self.testing_tab = None
        self.widget = None
        self.update()

    def update(self):
        self.widget = widgets.Tab()
        self.control_widget = DeviceControl(self.main_gui.device, self.main_gui)
        self.calibration_tab = CalibrationTab(main_gui=self.main_gui)
        self.testing_tab = HardwareTestGUI(main_gui=self.main_gui)
        self.widget.children = [
            self.control_widget.widget,
            self.calibration_tab.widget,
            self.testing_tab.widget,
        ]
        self.widget.set_title(0, "Control")
        self.widget.set_title(1, "Calibration")
        self.widget.set_title(2, "Testing")

        # self.widget = VBox([#self.device_class,
        #                     # self.ftdi_address,
        #                     # self.config_path,
        #                     # HBox([self.connect_button, self.reset_connection_button]),
        #                     self.control_widget])

    def update_selection_options(self):
        """
        Update the selection options for the device class and FTDI address
        :return:
        """
        # config_paths = glob.glob("../**/device_config.yaml", recursive=True)
        # self.config_paths = [os.path.relpath(p) for p in config_paths]
        # self.experiment_directories = [os.path.relpath(os.path.join(p, "..")) for p in self.config_paths]
        # self.device_class = widgets.Dropdown(description="*CLASS", options=get_device_classes())
        self.ftdi_address = widgets.Dropdown(
            description="*ADDRESS", options=get_ftdi_addresses()
        )
        # self.config_path = widgets.Dropdown(description="CALIBRATION", options=self.config_paths, index=None)
        self.update()
        self.main_gui.update()

    def handle_connect_button(self, button):
        button.disabled = True
        button.description = "connecting..."
        try:
            self.connect_device()
        finally:
            button.disabled = False
            # button.description_tooltip = "link device"

    def handle_connection_reset_button(self, button):
        try:
            self.main_gui.device.spi.terminate()
        except Exception:
            pass
        try:
            self.main_gui.device.i2c.terminate()
        except Exception:
            pass

        UsbTools.release_all_devices()
        UsbTools.flush_cache()
        # self.control_widget = DeviceControl(None).widget
        self.update_selection_options()

    def connect_device(self):
        self.control_widget = DeviceControl(None, self.main_gui).widget
        with self.setup_menu.output:
            clear_output()
            self.update()

            if self.main_gui.device is not None:
                self.main_gui.device.connect(ftdi_address=self.ftdi_address.value)
            else:
                self.main_gui.device = BaseDevice(ftdi_address=self.ftdi_address.value)
                self.main_gui.device.connect()
            # if self.config_path.value is not None:
            #     self.main_gui.device.load_calibration(config_path=self.config_path.value)
            self.control_widget = DeviceControl(
                self.main_gui.device, self.main_gui
            ).widget
            self.update()
        self.main_gui.update()

    # def connect_experiment_device(self):
    #     with self.status_bar.output:
    #         clear_output()
    #         self.widget = DeviceControl(self.main_gui.device).widget
    #     self.main_gui.update()


# def get_device_classes():
#     ks = list(globals().keys())
#     device_classes = [BaseDevice, MorbidostatDevice]
#     for k in ks:
#         try:
#             if BaseDevice in inspect.getmro(globals()[k]):
#                 device_classes += [globals()[k]]
#         except:
#             pass
#     culture_classes = list(set(device_classes))
#     return culture_classes


def get_culture_classes():
    ks = list(globals().keys())
    culture_classes = [TurbidostatCulture, MorbidostatCulture]
    for k in ks:
        try:
            if TurbidostatCulture in inspect.getmro(globals()[k]):
                culture_classes += [globals()[k]]
        except Exception:
            pass
    culture_classes = list(set(culture_classes))
    return culture_classes


def get_ftdi_addresses():
    try:
        available_devices = [d[0] for d in pyftdi.ftdi.Ftdi.list_devices()]
    except Exception:
        logging.warning("Could not list FTDI devices. Resetting USB connections.")
        UsbTools.release_all_devices()
        UsbTools.flush_cache()
        available_devices = [d[0] for d in pyftdi.ftdi.Ftdi.list_devices()]

    ftdi_addresses = []
    for value in available_devices:
        bus = value.bus
        # address = value.address
        # ftdi_addresses += ["ftdi://ftdi:2232h:%d:%d" % (bus, address)]
        ftdi_addresses += ["ftdi://ftdi:2232h:%d" % (bus)]
    return ftdi_addresses
