"""Pruebas básicas para `sinusoidal_signal`.

Comprueba forma, rango y validación de parámetros.
"""

import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))

from scr.func_generic_signals import sinusoidal_signal


def test_sinusoidal_signal_shape_and_range():
    freq = 50
    amp = 1.5
    fs = 1000
    duration = 0.02
    offset = 0.5

    t = np.arange(0.0, duration, 1.0 / fs)
    y = sinusoidal_signal(t, frequency=freq, amplitude=amp, phase=0.0, offset=offset)

    assert y.shape == t.shape
    # Por muestreo no siempre se capta el pico exacto, comprobar límites
    assert np.all(y <= offset + amp + 1e-8)
    assert np.all(y >= offset - amp - 1e-8)


def test_sinusoidal_signal_invalid_parameters():
    t = np.linspace(0, 0.01, 10)
    with pytest.raises(ValueError):
        sinusoidal_signal(t, frequency=0.0, amplitude=1.0)

    with pytest.raises(ValueError):
        sinusoidal_signal(t, frequency=10.0, amplitude=0.0)
