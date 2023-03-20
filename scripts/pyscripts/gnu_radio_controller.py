#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Radiometer control script
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import datetime
import numpy as np



from gnuradio import qtgui

class gnu_radio_controller(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Radiometer control script", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radiometer control script")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "gnu_radio_controller")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.vec_len = vec_len = 4096
        self.std_dev_power = std_dev_power = 0.000025
        self.samp_rate = samp_rate = 10E6
        self.rho = rho = 1
        self.record_data = record_data = 0
        self.noise_sys = noise_sys = 1
        self.noise_cmb = noise_cmb = 1
        self.noise_atm_zenith = noise_atm_zenith = 1
        self.local_oscillator = local_oscillator = 1.0E9
        self.intermediate_rate = intermediate_rate = 1000
        self.ingest_data = ingest_data = 0
        self.file_write_rate = file_write_rate = 10
        self.file_path = file_path = '/home/slash/Desktop/Phys 258/Phys_258_Final_Project/Amateur_measurement_of_the_CMB/data/no_file'
        self.center_frequency = center_frequency = 1450E6
        self.calibrate = calibrate = 0
        self.average_power = average_power = 3
        self.T_sys = T_sys = 1
        self.T_other = T_other = 1
        self.T_atm = T_atm = 1
        self.IntegrationTimeShort = IntegrationTimeShort = 0.8
        self.IntegrationTimeLong = IntegrationTimeLong = 8
        self.IntegrationTime = IntegrationTime = 8

        ##################################################
        # Blocks
        ##################################################
        self._rho_tool_bar = Qt.QToolBar(self)
        self._rho_tool_bar.addWidget(Qt.QLabel("Rho" + ": "))
        self._rho_line_edit = Qt.QLineEdit(str(self.rho))
        self._rho_tool_bar.addWidget(self._rho_line_edit)
        self._rho_line_edit.returnPressed.connect(
            lambda: self.set_rho(eng_notation.str_to_num(str(self._rho_line_edit.text()))))
        self.top_layout.addWidget(self._rho_tool_bar)
        self._noise_sys_range = Range(0, 10, 0.2, 1, 200)
        self._noise_sys_win = RangeWidget(self._noise_sys_range, self.set_noise_sys, "System       ", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_sys_win, 1, 0, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_cmb_range = Range(0, 10, 0.2, 1, 200)
        self._noise_cmb_win = RangeWidget(self._noise_cmb_range, self.set_noise_cmb, "CMB            ", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_cmb_win, 0, 0, 1, 2)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._noise_atm_zenith_range = Range(0, 10, 0.2, 1, 200)
        self._noise_atm_zenith_win = RangeWidget(self._noise_atm_zenith_range, self.set_noise_atm_zenith, "Atm Zenith", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._noise_atm_zenith_win, 2, 0, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._ingest_data_options = [0, 1]
        # Create the labels list
        self._ingest_data_labels = ['Stop', 'Start']
        # Create the combo box
        # Create the radio buttons
        self._ingest_data_group_box = Qt.QGroupBox("Ingest data ?" + ": ")
        self._ingest_data_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._ingest_data_button_group = variable_chooser_button_group()
        self._ingest_data_group_box.setLayout(self._ingest_data_box)
        for i, _label in enumerate(self._ingest_data_labels):
            radio_button = Qt.QRadioButton(_label)
            self._ingest_data_box.addWidget(radio_button)
            self._ingest_data_button_group.addButton(radio_button, i)
        self._ingest_data_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ingest_data_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._ingest_data_options.index(i)))
        self._ingest_data_callback(self.ingest_data)
        self._ingest_data_button_group.buttonClicked[int].connect(
            lambda i: self.set_ingest_data(self._ingest_data_options[i]))
        self.top_grid_layout.addWidget(self._ingest_data_group_box, 6, 1, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._file_path_tool_bar = Qt.QToolBar(self)
        self._file_path_tool_bar.addWidget(Qt.QLabel("T athmosphere" + ": "))
        self._file_path_line_edit = Qt.QLineEdit(str(self.file_path))
        self._file_path_tool_bar.addWidget(self._file_path_line_edit)
        self._file_path_line_edit.returnPressed.connect(
            lambda: self.set_file_path(str(str(self._file_path_line_edit.text()))))
        self.top_layout.addWidget(self._file_path_tool_bar)
        # Create the options list
        self._calibrate_options = [0, 1, 2, 3]
        # Create the labels list
        self._calibrate_labels = ['No rho', 'Rho calibration', 'Atm calibration', 'Atm calibration+']
        # Create the combo box
        # Create the radio buttons
        self._calibrate_group_box = Qt.QGroupBox("Calibration" + ": ")
        self._calibrate_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._calibrate_button_group = variable_chooser_button_group()
        self._calibrate_group_box.setLayout(self._calibrate_box)
        for i, _label in enumerate(self._calibrate_labels):
            radio_button = Qt.QRadioButton(_label)
            self._calibrate_box.addWidget(radio_button)
            self._calibrate_button_group.addButton(radio_button, i)
        self._calibrate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._calibrate_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._calibrate_options.index(i)))
        self._calibrate_callback(self.calibrate)
        self._calibrate_button_group.buttonClicked[int].connect(
            lambda i: self.set_calibrate(self._calibrate_options[i]))
        self.top_layout.addWidget(self._calibrate_group_box)
        self._T_sys_tool_bar = Qt.QToolBar(self)
        self._T_sys_tool_bar.addWidget(Qt.QLabel("T system" + ": "))
        self._T_sys_line_edit = Qt.QLineEdit(str(self.T_sys))
        self._T_sys_tool_bar.addWidget(self._T_sys_line_edit)
        self._T_sys_line_edit.returnPressed.connect(
            lambda: self.set_T_sys(eng_notation.str_to_num(str(self._T_sys_line_edit.text()))))
        self.top_layout.addWidget(self._T_sys_tool_bar)
        self._T_other_tool_bar = Qt.QToolBar(self)
        self._T_other_tool_bar.addWidget(Qt.QLabel("T other" + ": "))
        self._T_other_line_edit = Qt.QLineEdit(str(self.T_other))
        self._T_other_tool_bar.addWidget(self._T_other_line_edit)
        self._T_other_line_edit.returnPressed.connect(
            lambda: self.set_T_other(eng_notation.str_to_num(str(self._T_other_line_edit.text()))))
        self.top_layout.addWidget(self._T_other_tool_bar)
        self._T_atm_tool_bar = Qt.QToolBar(self)
        self._T_atm_tool_bar.addWidget(Qt.QLabel("T athmosphere" + ": "))
        self._T_atm_line_edit = Qt.QLineEdit(str(self.T_atm))
        self._T_atm_tool_bar.addWidget(self._T_atm_line_edit)
        self._T_atm_line_edit.returnPressed.connect(
            lambda: self.set_T_atm(eng_notation.str_to_num(str(self._T_atm_line_edit.text()))))
        self.top_layout.addWidget(self._T_atm_tool_bar)
        self._IntegrationTime_range = Range(0, 10, 0.2, 8, 200)
        self._IntegrationTime_win = RangeWidget(self._IntegrationTime_range, self.set_IntegrationTime, "Integration Time", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._IntegrationTime_win, 6, 0, 1, 1)
        for r in range(6, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(1/samp_rate*IntegrationTime, 1)
        # Create the options list
        self._record_data_options = [0, 1]
        # Create the labels list
        self._record_data_labels = ['Stop', 'Start']
        # Create the combo box
        # Create the radio buttons
        self._record_data_group_box = Qt.QGroupBox("Record data ?" + ": ")
        self._record_data_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._record_data_button_group = variable_chooser_button_group()
        self._record_data_group_box.setLayout(self._record_data_box)
        for i, _label in enumerate(self._record_data_labels):
            radio_button = Qt.QRadioButton(_label)
            self._record_data_box.addWidget(radio_button)
            self._record_data_button_group.addButton(radio_button, i)
        self._record_data_callback = lambda i: Qt.QMetaObject.invokeMethod(self._record_data_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._record_data_options.index(i)))
        self._record_data_callback(self.record_data)
        self._record_data_button_group.buttonClicked[int].connect(
            lambda i: self.set_record_data(self._record_data_options[i]))
        self.top_layout.addWidget(self._record_data_group_box)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_frequency, #fc
            samp_rate, #bw
            'Waterfall', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 0, 2, 2)
        for r in range(3, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            1024, #size
            intermediate_rate, #samp_rate
            'Radiometer Time Sink', #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.1)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 20)

        self.qtgui_time_sink_x_0.set_y_label('Power', 'dB*')

        self.qtgui_time_sink_x_0.enable_tags(False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win, 5, 0, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_histogram_sink_x_0_0 = qtgui.histogram_sink_f(
            1,
            1000,
            average_power-std_dev_power*4,
            average_power+std_dev_power*4,
            'Histogram',
            1,
            None # parent
        )

        self.qtgui_histogram_sink_x_0_0.set_update_time(0.10)
        self.qtgui_histogram_sink_x_0_0.enable_autoscale(True)
        self.qtgui_histogram_sink_x_0_0.enable_accumulate(True)
        self.qtgui_histogram_sink_x_0_0.enable_grid(True)
        self.qtgui_histogram_sink_x_0_0.enable_axis_labels(True)


        labels = ['Bin counts', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        styles = [4, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers= [0, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]
        alphas = [0.8, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_histogram_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_histogram_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_histogram_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_histogram_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_histogram_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_histogram_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_histogram_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_histogram_sink_x_0_0_win = sip.wrapinstance(self.qtgui_histogram_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_histogram_sink_x_0_0_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.num_sink_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.num_sink_1.set_update_time(0.10)
        self.num_sink_1.set_title('Power undecimated')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.num_sink_1.set_min(i, -1)
            self.num_sink_1.set_max(i, 1)
            self.num_sink_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.num_sink_1.set_label(i, "Data {0}".format(i))
            else:
                self.num_sink_1.set_label(i, labels[i])
            self.num_sink_1.set_unit(i, units[i])
            self.num_sink_1.set_factor(i, factor[i])

        self.num_sink_1.enable_autoscale(False)
        self._num_sink_1_win = sip.wrapinstance(self.num_sink_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._num_sink_1_win, 7, 0, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.moving_average = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1,
            None # parent
        )
        self.moving_average.set_update_time(0.10)
        self.moving_average.set_title('Moving Average')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.moving_average.set_min(i, -1)
            self.moving_average.set_max(i, 1)
            self.moving_average.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.moving_average.set_label(i, "Data {0}".format(i))
            else:
                self.moving_average.set_label(i, labels[i])
            self.moving_average.set_unit(i, units[i])
            self.moving_average.set_factor(i, factor[i])

        self.moving_average.enable_autoscale(False)
        self._moving_average_win = sip.wrapinstance(self.moving_average.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._moving_average_win, 7, 1, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_sub_xx_0_1 = blocks.sub_ff(1)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_selector_0_1 = blocks.selector(gr.sizeof_float*1,0,ingest_data)
        self.blocks_selector_0_1.set_enabled(True)
        self.blocks_selector_0_0 = blocks.selector(gr.sizeof_float*1,calibrate,0)
        self.blocks_selector_0_0.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_float*1,0,ingest_data)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(rho)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, 0.001, 4000, 1)
        self.blocks_keep_one_in_n_0_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(intermediate_rate/file_write_rate))
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_float*1, int(samp_rate/intermediate_rate))
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_float*1, file_path, True)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.blocks_complex_to_mag_squared_1 = blocks.complex_to_mag_squared(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0_0_0 = analog.noise_source_c(analog.GR_UNIFORM, noise_atm_zenith, 0)
        self.analog_noise_source_x_0_0 = analog.noise_source_c(analog.GR_UNIFORM, noise_sys, 0)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_UNIFORM, noise_cmb, 0)
        self.analog_const_source_x_1_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, T_other)
        self.analog_const_source_x_1_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, T_atm)
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, T_sys)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_sub_xx_0_0, 1))
        self.connect((self.analog_const_source_x_1_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.analog_const_source_x_1_0_0, 0), (self.blocks_sub_xx_0_1, 1))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_noise_source_x_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.analog_noise_source_x_0_0_0, 0), (self.blocks_add_xx_0, 2))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_1, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.num_sink_1, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.blocks_selector_0_1, 0))
        self.connect((self.blocks_keep_one_in_n_0_0, 0), (self.qtgui_histogram_sink_x_0_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_mag_squared_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_selector_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_selector_0_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.blocks_keep_one_in_n_0_0, 0))
        self.connect((self.blocks_selector_0_0, 0), (self.moving_average, 0))
        self.connect((self.blocks_selector_0_1, 1), (self.blocks_file_sink_0, 0))
        self.connect((self.blocks_selector_0_1, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_selector_0_0, 2))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_sub_xx_0_1, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_selector_0_0, 1))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_sub_xx_0_1, 0), (self.blocks_selector_0_0, 3))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gnu_radio_controller")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vec_len(self):
        return self.vec_len

    def set_vec_len(self, vec_len):
        self.vec_len = vec_len

    def get_std_dev_power(self):
        return self.std_dev_power

    def set_std_dev_power(self, std_dev_power):
        self.std_dev_power = std_dev_power
        self.qtgui_histogram_sink_x_0_0.set_x_axis(self.average_power-self.std_dev_power*4, self.average_power+self.std_dev_power*4)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_keep_one_in_n_0.set_n(int(self.samp_rate/self.intermediate_rate))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)
        self.single_pole_iir_filter_xx_0.set_taps(1/self.samp_rate*self.IntegrationTime)

    def get_rho(self):
        return self.rho

    def set_rho(self, rho):
        self.rho = rho
        Qt.QMetaObject.invokeMethod(self._rho_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.rho)))
        self.blocks_multiply_const_vxx_1.set_k(self.rho)

    def get_record_data(self):
        return self.record_data

    def set_record_data(self, record_data):
        self.record_data = record_data
        self._record_data_callback(self.record_data)

    def get_noise_sys(self):
        return self.noise_sys

    def set_noise_sys(self, noise_sys):
        self.noise_sys = noise_sys
        self.analog_noise_source_x_0_0.set_amplitude(self.noise_sys)

    def get_noise_cmb(self):
        return self.noise_cmb

    def set_noise_cmb(self, noise_cmb):
        self.noise_cmb = noise_cmb
        self.analog_noise_source_x_0.set_amplitude(self.noise_cmb)

    def get_noise_atm_zenith(self):
        return self.noise_atm_zenith

    def set_noise_atm_zenith(self, noise_atm_zenith):
        self.noise_atm_zenith = noise_atm_zenith
        self.analog_noise_source_x_0_0_0.set_amplitude(self.noise_atm_zenith)

    def get_local_oscillator(self):
        return self.local_oscillator

    def set_local_oscillator(self, local_oscillator):
        self.local_oscillator = local_oscillator

    def get_intermediate_rate(self):
        return self.intermediate_rate

    def set_intermediate_rate(self, intermediate_rate):
        self.intermediate_rate = intermediate_rate
        self.blocks_keep_one_in_n_0.set_n(int(self.samp_rate/self.intermediate_rate))
        self.blocks_keep_one_in_n_0_0.set_n(int(self.intermediate_rate/self.file_write_rate))
        self.qtgui_time_sink_x_0.set_samp_rate(self.intermediate_rate)

    def get_ingest_data(self):
        return self.ingest_data

    def set_ingest_data(self, ingest_data):
        self.ingest_data = ingest_data
        self._ingest_data_callback(self.ingest_data)
        self.blocks_selector_0.set_output_index(self.ingest_data)
        self.blocks_selector_0_1.set_output_index(self.ingest_data)

    def get_file_write_rate(self):
        return self.file_write_rate

    def set_file_write_rate(self, file_write_rate):
        self.file_write_rate = file_write_rate
        self.blocks_keep_one_in_n_0_0.set_n(int(self.intermediate_rate/self.file_write_rate))

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path
        Qt.QMetaObject.invokeMethod(self._file_path_line_edit, "setText", Qt.Q_ARG("QString", str(self.file_path)))
        self.blocks_file_sink_0.open(self.file_path)

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)

    def get_calibrate(self):
        return self.calibrate

    def set_calibrate(self, calibrate):
        self.calibrate = calibrate
        self._calibrate_callback(self.calibrate)
        self.blocks_selector_0_0.set_input_index(self.calibrate)

    def get_average_power(self):
        return self.average_power

    def set_average_power(self, average_power):
        self.average_power = average_power
        self.qtgui_histogram_sink_x_0_0.set_x_axis(self.average_power-self.std_dev_power*4, self.average_power+self.std_dev_power*4)

    def get_T_sys(self):
        return self.T_sys

    def set_T_sys(self, T_sys):
        self.T_sys = T_sys
        Qt.QMetaObject.invokeMethod(self._T_sys_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.T_sys)))
        self.analog_const_source_x_1.set_offset(self.T_sys)

    def get_T_other(self):
        return self.T_other

    def set_T_other(self, T_other):
        self.T_other = T_other
        Qt.QMetaObject.invokeMethod(self._T_other_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.T_other)))
        self.analog_const_source_x_1_0_0.set_offset(self.T_other)

    def get_T_atm(self):
        return self.T_atm

    def set_T_atm(self, T_atm):
        self.T_atm = T_atm
        Qt.QMetaObject.invokeMethod(self._T_atm_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.T_atm)))
        self.analog_const_source_x_1_0.set_offset(self.T_atm)

    def get_IntegrationTimeShort(self):
        return self.IntegrationTimeShort

    def set_IntegrationTimeShort(self, IntegrationTimeShort):
        self.IntegrationTimeShort = IntegrationTimeShort

    def get_IntegrationTimeLong(self):
        return self.IntegrationTimeLong

    def set_IntegrationTimeLong(self, IntegrationTimeLong):
        self.IntegrationTimeLong = IntegrationTimeLong

    def get_IntegrationTime(self):
        return self.IntegrationTime

    def set_IntegrationTime(self, IntegrationTime):
        self.IntegrationTime = IntegrationTime
        self.single_pole_iir_filter_xx_0.set_taps(1/self.samp_rate*self.IntegrationTime)




def main(top_block_cls=gnu_radio_controller, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
