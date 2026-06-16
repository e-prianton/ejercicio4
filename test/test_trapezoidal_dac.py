"""Verifica forma y longitud de t, y y codes
Comprueba el rango de códigos para 12 bits
Comprueba los valores de y dentro de [0, v_ref]
Prueba errores para parámetros inválidos
Comprueba los casos de bits <= 8 y bits > 16."""

import os
import sys

import numpy as np
import pytest

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..')))

from scr.trapezoidal_DAC import trapezoidal_dac_samples


def test_trapezoidal_dac_samples_shape_and_range():
    freq = 50
    amp = 2.8
    fs = 8000
    duration = 0.1
    bits = 12
    v_ref = 3.3

    t, y, codes = trapezoidal_dac_samples(
        frequency=freq,
        amplitude=amp,
        fs=fs,
        duration=duration,
        duty_low=0.2,
        duty_rise=0.2,
        duty_high=0.4,
        offset=0.5,
        bits=bits,
        v_ref=v_ref,
    )

    expected_len = int(fs * duration)
    assert t.shape == y.shape == codes.shape
    assert len(t) == expected_len
    assert t[0] == pytest.approx(0.0)
    assert t[-1] == pytest.approx((expected_len - 1) / fs)
    assert codes.dtype == np.uint16
    assert codes.min() >= 0
    assert codes.max() <= 2**bits - 1
    assert np.all(codes == np.round((y / v_ref) * (2**bits - 1)).astype(np.uint16))
    assert np.all(y >= 0.0)
    assert np.all(y <= v_ref + 1e-8)


def test_trapezoidal_dac_samples_invalid_parameters():
    with pytest.raises(ValueError):
        trapezoidal_dac_samples(frequency=50, amplitude=1.0, fs=0, duration=0.1)

    with pytest.raises(ValueError):
        trapezoidal_dac_samples(frequency=50, amplitude=1.0, fs=8000, duration=0.1, bits=0)

    with pytest.raises(ValueError):
        trapezoidal_dac_samples(frequency=50, amplitude=1.0, fs=8000, duration=0.1, offset=-0.1)


def test_trapezoidal_dac_samples_dtype_for_8_bits():
    t, y, codes = trapezoidal_dac_samples(
        frequency=50,
        amplitude=1.0,
        fs=1000,
        duration=0.01,
        bits=8,
        v_ref=1.0,
    )

    assert codes.dtype == np.uint8
    assert codes.min() >= 0
    assert codes.max() <= 255
    assert len(codes) == int(1000 * 0.01)
    assert np.all(y >= 0.0)
    assert np.all(y <= 1.0 + 1e-8)


def test_trapezoidal_dac_samples_dtype_for_20_bits():
    t, y, codes = trapezoidal_dac_samples(
        frequency=10,
        amplitude=1.0,
        fs=1000,
        duration=0.01,
        bits=20,
        v_ref=1.0,
    )

    assert codes.dtype == np.uint32
    assert codes.min() >= 0
    assert codes.max() <= 2**20 - 1
    assert len(codes) == int(1000 * 0.01)
    assert np.all(y >= 0.0)
    assert np.all(y <= 1.0 + 1e-8)
