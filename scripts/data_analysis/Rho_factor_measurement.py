# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Rho factor output
# Author: slash
# GNU Radio version: 3.10.1.1

from gnuradio import analog
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal







class Rho_factor_measurement(gr.hier_block2):
    def __init__(self, T_cold=200, T_hot=77, samp_rate=32k):
        gr.hier_block2.__init__(
            self, "Rho factor output",
                gr.io_signature.makev(2, 2, [gr.sizeof_float*1, gr.sizeof_float*1]),
                gr.io_signature.makev(2, 2, [gr.sizeof_float*1, gr.sizeof_float*1]),
        )

        ##################################################
        # Parameters
        ##################################################
        self.T_cold = T_cold
        self.T_hot = T_hot
        self.samp_rate = samp_rate

        ##################################################
        # Variables
        ##################################################
        self.gain_saturation = gain_saturation = 1

        ##################################################
        # Blocks
        ##################################################
        self.blocks_sub_xx_0_1 = blocks.sub_ff(1)
        self.blocks_sub_xx_0_0 = blocks.sub_ff(1)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(1/gain_saturation)
        self.blocks_divide_xx_0_1 = blocks.divide_ff(1)
        self.blocks_divide_xx_0_0 = blocks.divide_ff(1)
        self.blocks_divide_xx_0 = blocks.divide_ff(1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-1)
        self.analog_const_source_x_0_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, T_hot)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, T_cold)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.analog_const_source_x_0_0_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.analog_const_source_x_0_0_0, 0), (self.blocks_sub_xx_0_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_divide_xx_0_0, 1))
        self.connect((self.blocks_divide_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_divide_xx_0_0, 0), (self, 0))
        self.connect((self.blocks_divide_xx_0_1, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_divide_xx_0_1, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_sub_xx_0_1, 1))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_divide_xx_0, 0))
        self.connect((self.blocks_sub_xx_0_0, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_sub_xx_0_1, 0), (self.blocks_divide_xx_0_0, 0))
        self.connect((self, 0), (self.blocks_divide_xx_0_1, 0))
        self.connect((self, 0), (self.blocks_sub_xx_0_0, 0))
        self.connect((self, 1), (self.blocks_divide_xx_0_1, 1))
        self.connect((self, 1), (self.blocks_sub_xx_0_0, 1))


    def get_T_cold(self):
        return self.T_cold

    def set_T_cold(self, T_cold):
        self.T_cold = T_cold
        self.analog_const_source_x_0_0.set_offset(self.T_cold)

    def get_T_hot(self):
        return self.T_hot

    def set_T_hot(self, T_hot):
        self.T_hot = T_hot
        self.analog_const_source_x_0_0_0.set_offset(self.T_hot)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_gain_saturation(self):
        return self.gain_saturation

    def set_gain_saturation(self, gain_saturation):
        self.gain_saturation = gain_saturation
        self.blocks_multiply_const_vxx_0.set_k(1/self.gain_saturation)

