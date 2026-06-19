"""Pruebas básicas para `square_signal`.

Comprueba forma, ciclo de trabajo y validación de parámetros.
"""

import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))

from scr.func_generic_signals import square_signal


def test_square_signal_shape_and_duty():
    freq = 10
    amp = 2.0
    fs = 1000
    duration = 0.1
    offset = 0.2
    duty = 0.25

    t = np.arange(0.0, duration, 1.0 / fs)
    y = square_signal(t, frequency=freq, amplitude=amp, duty=duty, phase=0.0, offset=offset)

    assert y.shape == t.shape
    assert np.all((y == offset) | (y == offset + amp))
    high_fraction = np.mean(y == offset + amp)
    assert high_fraction == pytest.approx(duty, rel=1e-2)
    assert np.all(y >= offset)
    assert np.all(y <= offset + amp)


def test_square_signal_invalid_parameters():
    t = np.linspace(0, 0.01, 10)
    with pytest.raises(ValueError):
        square_signal(t, frequency=0.0, amplitude=1.0)

    with pytest.raises(ValueError):
        square_signal(t, frequency=10.0, amplitude=0.0)

    with pytest.raises(ValueError):
        square_signal(t, frequency=10.0, amplitude=1.0, duty=0.0)

    with pytest.raises(ValueError):
        square_signal(t, frequency=10.0, amplitude=1.0, duty=1.0)
