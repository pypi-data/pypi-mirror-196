# -*- coding: utf-8 -*-

"""CPU diffractometer.

This subpackage implements the features to simulate X-ray diffraction
and to compute the Fourier transform of the diffracted intensity.
This implementation uses the Monte Carlo method, parallelized on CPU.
"""

from . import diffraction, parser


setup = parser.setup
diffract = diffraction.diffract
