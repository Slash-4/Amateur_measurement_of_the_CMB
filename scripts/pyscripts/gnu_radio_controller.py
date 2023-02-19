#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
import math
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation



from gnuradio import qtgui

class gnu_radio_controller(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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
        self.variable_qtgui_chooser_0 = variable_qtgui_chooser_0 = 0
        self.samp_rate = samp_rate = 32000
        self.center_frequency = center_frequency = 11E9
        self.bandwidth_view = bandwidth_view = 11E9
        self.bandwidth = bandwidth = 2E9
        self.Local_oscillator = Local_oscillator = 1.0E9

        ##################################################
        # Blocks
        ##################################################
        # Create the options list
        self._variable_qtgui_chooser_0_options = [0, 1, 2]
        # Create the labels list
        self._variable_qtgui_chooser_0_labels = ['0', '1', '2']
        # Create the combo box
        self._variable_qtgui_chooser_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_chooser_0_tool_bar.addWidget(Qt.QLabel("'variable_qtgui_chooser_0'" + ": "))
        self._variable_qtgui_chooser_0_combo_box = Qt.QComboBox()
        self._variable_qtgui_chooser_0_tool_bar.addWidget(self._variable_qtgui_chooser_0_combo_box)
        for _label in self._variable_qtgui_chooser_0_labels: self._variable_qtgui_chooser_0_combo_box.addItem(_label)
        self._variable_qtgui_chooser_0_callback = lambda i: Qt.QMetaObject.invokeMethod(self._variable_qtgui_chooser_0_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._variable_qtgui_chooser_0_options.index(i)))
        self._variable_qtgui_chooser_0_callback(self.variable_qtgui_chooser_0)
        self._variable_qtgui_chooser_0_combo_box.currentIndexChanged.connect(
            lambda i: self.set_variable_qtgui_chooser_0(self._variable_qtgui_chooser_0_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._variable_qtgui_chooser_0_tool_bar)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_cc(1.0, 1)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            1024, #fftsize
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_frequency, #fc
            bandwidth, #bw
            "", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_win)
        self.blocks_keep_one_in_n_0 = blocks.keep_one_in_n(gr.sizeof_gr_complex*1, 4)
        self.blocks_freqshift_cc_0 = blocks.rotator_cc(2.0*math.pi*Local_oscillator/samp_rate)
        self.analog_sig_source_x_0_0_0 = analog.sig_source_c(samp_rate, analog.GR_SQR_WAVE, 1000, 1, 0, 0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_sig_source_x_0_0_0, 0), (self.single_pole_iir_filter_xx_0, 0))
        self.connect((self.blocks_freqshift_cc_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_keep_one_in_n_0, 0), (self.blocks_freqshift_cc_0, 0))
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_keep_one_in_n_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "gnu_radio_controller")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_variable_qtgui_chooser_0(self):
        return self.variable_qtgui_chooser_0

    def set_variable_qtgui_chooser_0(self, variable_qtgui_chooser_0):
        self.variable_qtgui_chooser_0 = variable_qtgui_chooser_0
        self._variable_qtgui_chooser_0_callback(self.variable_qtgui_chooser_0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0_0.set_sampling_freq(self.samp_rate)
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.Local_oscillator/self.samp_rate)

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.qtgui_sink_x_0.set_frequency_range(self.center_frequency, self.bandwidth)

    def get_bandwidth_view(self):
        return self.bandwidth_view

    def set_bandwidth_view(self, bandwidth_view):
        self.bandwidth_view = bandwidth_view

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.qtgui_sink_x_0.set_frequency_range(self.center_frequency, self.bandwidth)

    def get_Local_oscillator(self):
        return self.Local_oscillator

    def set_Local_oscillator(self, Local_oscillator):
        self.Local_oscillator = Local_oscillator
        self.blocks_freqshift_cc_0.set_phase_inc(2.0*math.pi*self.Local_oscillator/self.samp_rate)




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
