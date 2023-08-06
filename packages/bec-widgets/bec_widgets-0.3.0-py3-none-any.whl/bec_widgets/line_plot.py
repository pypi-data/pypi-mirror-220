import os
import warnings
from typing import Any

import numpy as np
import pyqtgraph as pg
from bec_lib import BECClient
from pyqtgraph import mkBrush, mkColor, mkPen
from pyqtgraph.Qt import QtCore, QtWidgets, uic
from pyqtgraph.Qt.QtCore import pyqtSignal


class BasicPlot(QtWidgets.QWidget):
    update_signal = pyqtSignal()

    def __init__(self, name="", y_value_list=["gauss_bpm"]) -> None:
        """
        Basic plot widget for displaying scan data.

        Args:
            name (str, optional): Name of the plot. Defaults to "".
            y_value_list (list, optional): List of signals to be plotted. Defaults to ["gauss_bpm"].
        """

        super(BasicPlot, self).__init__()
        # Set style for pyqtgraph plots
        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        current_path = os.path.dirname(__file__)
        uic.loadUi(os.path.join(current_path, "line_plot.ui"), self)

        self._idle_time = 100
        self.title = ""
        self.label_bottom = ""
        self.label_left = ""

        self.scan_motors = []
        self.y_value_list = y_value_list
        self.plotter_data_x = []
        self.plotter_data_y = []
        self.curves = []
        self.pens = []
        self.brushs = []

        self.plotter_scan_id = None

        # TODO to be moved to utils function
        plotstyles = {
            "symbol": "o",
            "symbolSize": 10,
        }
        color_list = ["#384c6b", "#e28a2b", "#5E3023", "#e41a1c", "#984e83", "#4daf4a"]
        color_list = BasicPlot.golden_angle_color(colormap="CET-R2", num=len(self.y_value_list))

        # setup plots
        self.plot = self.plot_window.getPlotItem()
        for ii in range(len(self.y_value_list)):
            pen = mkPen(color=color_list[ii], width=2, style=QtCore.Qt.DashLine)
            brush = mkBrush(color=color_list[ii])
            curve = pg.PlotDataItem(**plotstyles, symbolBrush=brush, pen=pen, skipFiniteCheck=True)
            self.plot.addItem(curve)
            self.curves.append(curve)
            self.pens.append(pen)
            self.brushs.append(brush)

        self.crosshair_v = pg.InfiniteLine(angle=90, movable=False)
        self.plot.addItem(self.crosshair_v, ignoreBounds=True)

        # Add textItems
        self.add_text_items()

        # Manage signals
        self.proxy = pg.SignalProxy(
            self.plot.scene().sigMouseMoved, rateLimit=60, slot=self.mouse_moved
        )
        self.proxy_update = pg.SignalProxy(self.update_signal, rateLimit=25, slot=self.update)

    def add_text_items(self):
        """Add text items to the plot"""

        self.mouse_box_data.setText("Mouse cursor")
        # TODO Via StyleSheet, one may set the color of the full QLabel
        # self.mouse_box_data.setStyleSheet(f"QLabel {{color : rgba{self.pens[0].color().getRgb()}}}")

    def mouse_moved(self, event: tuple) -> None:
        """
        Update the mouse box with the current mouse position and the corresponding data.

        Args:
            event (tuple):  Mouse event containing the position of the mouse cursor.
                            The position is stored in first entry as horizontal, vertical pixel.
        """
        pos = event[0]
        if not self.plot.sceneBoundingRect().contains(pos):
            return
        mousePoint = self.plot.vb.mapSceneToView(pos)
        self.crosshair_v.setPos(mousePoint.x())
        if not self.plotter_data_x:
            return
        self.mouse_box_data.setText("Mouse cursor")

        for ii, y_value in enumerate(self.y_value_list):
            closest_point = self.closest_x_y_value(
                mousePoint.x(), self.plotter_data_x, self.plotter_data_y[ii]
            )
            # TODO fix text wobble in plot, see plot when it crosses 0
            x_data = f"{closest_point[0]:.{self.precision}f}"
            y_data = f"{closest_point[1]:.{self.precision}f}"
            string_cap = 10
            self.mouse_box_data.setText(
                "".join(
                    [
                        self.mouse_box_data.text(),
                        "\n",
                        # TODO fix different fonts for mouse cursor!
                        # f"<p'FONT COLOR=red';>",  # rgba{self.pens[ii].color().getRgb()
                        f"{y_value}",
                        "\n",
                        f"X_data:   {x_data:>{string_cap}}",
                        "\n",
                        f"Y_data: {y_data:>{string_cap}}",
                    ]
                )
            )

    def closest_x_y_value(self, input_value, list_x, list_y) -> tuple:
        """
        Find the closest x and y value to the input value.

        Args:
            input_value (float): Input value
            list_x (list): List of x values
            list_y (list): List of y values

        Returns:
            tuple: Closest x and y value
        """
        arr = np.asarray(list_x)
        i = (np.abs(arr - input_value)).argmin()
        return list_x[i], list_y[i]

    def update(self):
        """Update the plot with the new data."""
        if len(self.plotter_data_x) <= 1:
            return
        self.plot.setLabel("bottom", self.label_bottom)
        self.plot.setLabel("left", self.label_left)
        for ii in range(len(self.y_value_list)):
            self.curves[ii].setData(self.plotter_data_x, self.plotter_data_y[ii])

    def __call__(self, data: dict, metadata: dict, **kwds: Any) -> None:
        """Update function that is called during the scan callback. To avoid
        too many renderings, the GUI is only processing events every <_idle_time> ms.

        Args:
            data (dict): Dictionary containing a new scan segment
            metadata (dict): Scan metadata

        """
        if metadata["scanID"] != self.plotter_scan_id:
            self.plotter_scan_id = metadata["scanID"]
            self._reset_plot_data()

        self.title = f"Scan {metadata['scan_number']}"

        self.scan_motors = scan_motors = metadata.get("scan_report_devices")
        client = BECClient()
        remove_y_value_index = [
            index
            for index, y_value in enumerate(self.y_value_list)
            if y_value not in client.device_manager.devices
        ]
        if remove_y_value_index:
            for ii in sorted(remove_y_value_index, reverse=True):
                # TODO Use bec warning message??? to be discussed with Klaus
                warnings.warn(
                    f"Warning: no matching signal for {self.y_value_list[ii]} found in list of devices. Removing from plot."
                )
                self.y_value_list.pop(ii)
        self.precision = client.device_manager.devices[scan_motors[0]]._info["describe"][
            scan_motors[0]
        ]["precision"]
        # TODO after update of bec_lib, this will be new way to access data
        # self.precision = client.device_manager.devices[scan_motors[0]].precision
        x = data["data"][scan_motors[0]][scan_motors[0]]["value"]
        self.plotter_data_x.append(x)
        for ii, y_value in enumerate(self.y_value_list):
            y = data["data"][y_value][y_value]["value"]
            self.plotter_data_y[ii].append(y)
        self.label_bottom = scan_motors[0]
        self.label_left = f"{', '.join(self.y_value_list)}"

        if len(self.plotter_data_x) <= 1:
            return
        self.update_signal.emit()

    def _reset_plot_data(self):
        """Reset the plot data."""
        self.plotter_data_x = []
        self.plotter_data_y = []
        for ii in range(len(self.y_value_list)):
            self.curves[ii].setData([], [])
            self.plotter_data_y.append([])
        self.mouse_box_data.setText("Mouse cursor")  # Crashes the Thread

    @staticmethod
    def golden_ratio(num: int) -> list:
        """Calculate the golden ratio for a given number of angles.

        Args:
            num (int): Number of angles
        """
        phi = 2 * np.pi * ((1 + np.sqrt(5)) / 2)
        angles = []
        for ii in range(num):
            x = np.cos(ii * phi)
            y = np.sin(ii * phi)
            angle = np.arctan2(y, x)
            angles.append(angle)
        return angles

    @staticmethod
    def golden_angle_color(colormap: str, num: int) -> list:
        """
        Extract num colors for from the specified colormap following golden angle distribution.

        Args:
            colormap (str): Name of the colormap
            num (int): Number of requested colors

        Returns:
            list: List of colors with length <num>

        Raises:
            ValueError: If the number of requested colors is greater than the number of colors in the colormap.
        """

        cmap = pg.colormap.get(colormap)
        cmap_colors = cmap.color
        if num > len(cmap_colors):
            raise ValueError(
                f"Number of colors requested ({num}) is greater than the number of colors in the colormap ({len(cmap_colors)})"
            )
        angles = BasicPlot.golden_ratio(len(cmap_colors))
        color_selection = np.round(np.interp(angles, (-np.pi, np.pi), (0, len(cmap_colors))))
        colors = [
            mkColor(tuple((cmap_colors[int(ii)] * 255).astype(int))) for ii in color_selection[:num]
        ]
        return colors


if __name__ == "__main__":
    import argparse

    from bec_widgets import ctrl_c

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--signals",
        help="specify recorded signals",
        nargs="+",
        default=["gauss_bpm", "bpm4i", "bpm5i", "bpm6i", "xert"],
    )
    value = parser.parse_args()
    print(f"Plotting signals for: {', '.join(value.signals)}")
    client = BECClient()
    client.start()
    app = QtWidgets.QApplication([])
    ctrl_c.setup(app)
    plot = BasicPlot(y_value_list=value.signals)
    plot.show()
    client.callbacks.register("scan_segment", plot, sync=False)
    app.exec_()
