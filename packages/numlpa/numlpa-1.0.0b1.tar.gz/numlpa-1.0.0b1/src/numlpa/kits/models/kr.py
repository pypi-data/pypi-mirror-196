# -*- coding: utf-8 -*-

"""Krivoglaz-Ryaboshapka (KR) model.

The model is described in: "M. Krivoglaz, K. Ryaboshapka,
Theory of x-ray scattering by crystals containing dislocations,
screw and edge dislocations 160 randomly distributed throughout
the crystal, Fiz. Metallov. Metalloved 15 (1963) 18-31."
"""

import numpy as np


def guide(transform, harmonic):
    """Return a guide for the model parameters.

    Parameters
    ----------
    transform : dict
        Fourier transform data.

    Returns
    -------
    dict
        Parameter names, min, max and guess values.

    """
    _ = harmonic
    density = transform['distribution']['density']
    distance = 1/np.sqrt(density)
    data = {
        'names': ('density', 'radius'),
        'max': (density*100, distance/10),
        'min': (density/100, distance*1000),
        'guess': (density, distance),
    }
    return data


def model(transform, harmonic, limit=None):
    """Retun the Fourier amplitude function.

    Parameters
    ----------
    transform : dict
        Fourier transform data.
    harmonic : int
        Harmonic.
    limit : int
        Last variable index.

    Returns
    -------
    Callable
        Function that takes parameter values and returns amplitudes.

    """
    var = {}
    var['C'] = transform['diffraction']['contrast']
    var['z_uvw'] = np.array(transform['diffraction']['z_uvw'])
    var['b_uvw'] = np.array(transform['diffraction']['b_uvw'])
    var['g_hkl'] = np.array(transform['diffraction']['g_hkl'])
    var['g'] = harmonic * var['g_hkl']/transform['diffraction']['cell']
    var['b'] = var['b_uvw'] * transform['diffraction']['cell']/2
    var['g_len'] = np.linalg.norm(var['g'])
    var['b_len'] = np.linalg.norm(var['b'])
    var['g_uni'] = var['g_hkl'] / np.linalg.norm(var['g_hkl'])
    var['z_uni'] = var['z_uvw'] / np.linalg.norm(var['z_uvw'])
    var['psi'] = np.abs(np.arccos(var['g_uni'].dot(var['z_uni'])))
    var['L'] = np.array(transform['coefficients']['variable'])
    if limit:
        var['L'] = var['L'][:limit]
    constant1 = np.pi/2 * var['g_len']**2 * var['b_len']**2 * var['C']
    constant2 = var['L'] / np.abs(var['g'].dot(var['b']))
    constant3 = constant1 * var['L']**2

    def amplitude(density, radius):
        if density < 0 or radius < 0:
            return np.inf
        return np.exp(constant3*density*np.log(constant2/radius))

    return amplitude
