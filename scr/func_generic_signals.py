""" Fichero con todas las funciones de señales de entrada genéricas """
import numpy as np

def trapezoidal_signal(t, frequency, amplitude, duty_low=0.0, duty_rise=0.25, duty_high=0.5, offset=0.0):
    """Genera una señal trapezoidal configurable.
    
    Esta función produce la forma de onda analógica en voltios y puede
    usarse para cualquier aplicación: simulación, análisis, prueba de
    filtros, entrada a un DAC, etc.
    
    Parámetros:
    -----------
    t : array-like
        Vector de tiempos (s).
    frequency : float
        Frecuencia de la señal (Hz).
    amplitude : float
        Amplitud de pico de la señal (V) sobre el offset.
        La señal varía entre `offset` y `offset + amplitude`.
    duty_low : float, default=0.0
        Fracción del periodo dedicada al nivel bajo (offset constante).
    duty_rise : float, default=0.25
        Fracción del periodo dedicada a la subida.
    duty_high : float, default=0.5
        Fracción del periodo dedicada al nivel alto.
        La bajada ocupa el resto: 1 - duty_low - duty_rise - duty_high.
    offset : float, default=0.0
        Valor de voltaje del nivel bajo.
    
    Retorna:
    --------
    ndarray
        Señal trapezoidal (mismo tamaño que `t`).
    
    Notas:
    ------
    - duty_low + duty_rise + duty_high debe ser < 1.
    - La forma es configurable ajustando duty_low, duty_rise y duty_high.
    - offset desplaza la señal hacia arriba.
    - Esta función genera la onda analógica.
    """
    t = np.asarray(t, dtype=float)
    if frequency <= 0:
        raise ValueError('frequency debe ser > 0')
    if amplitude <= 0:
        raise ValueError('amplitude debe ser > 0')
    if duty_low < 0 or duty_rise <= 0 or duty_high <= 0:
        raise ValueError('duty_low debe ser >= 0; duty_rise y duty_high deben ser > 0')
    if duty_low + duty_rise + duty_high >= 1.0:
        raise ValueError('duty_low + duty_rise + duty_high debe ser < 1')
    if offset < 0:
        raise ValueError('offset debe ser >= 0')
    
    period = 1.0 / frequency
    t_mod = np.mod(t, period)
    y = np.zeros_like(t, dtype=float)
    
    t_low_end = duty_low * period
    t_rise_end = t_low_end + duty_rise * period
    t_high_end = t_rise_end + duty_high * period
    t_fall_duration = period - t_high_end
    
    # Nivel bajo
    mask_low = t_mod < t_low_end
    y[mask_low] = offset
    
    # Tramo de subida
    mask_rise = (t_mod >= t_low_end) & (t_mod < t_rise_end)
    if np.any(mask_rise):
        y[mask_rise] = offset + amplitude * ((t_mod[mask_rise] - t_low_end) / (t_rise_end - t_low_end))
    
    # Tramo alto
    mask_high = (t_mod >= t_rise_end) & (t_mod < t_high_end)
    y[mask_high] = offset + amplitude
    
    # Tramo de bajada
    mask_fall = t_mod >= t_high_end
    if np.any(mask_fall):
        t_fall = t_mod[mask_fall] - t_high_end
        y[mask_fall] = offset + amplitude * (1.0 - t_fall / t_fall_duration)
    
    return y


def square_signal(t, frequency, amplitude, duty=0.5, phase=0.0, offset=0.0):
    """Genera una señal cuadrada configurable.

    La señal alterna entre `offset` y `offset + amplitude` según el ciclo de trabajo
    y la fase inicial.

    Parámetros:
    -----------
    t : array-like
        Vector de tiempos (s).
    frequency : float
        Frecuencia de la señal (Hz).
    amplitude : float
        Amplitud de pico de la señal (V).
    duty : float, default=0.5
        Fracción del periodo en nivel alto.
    phase : float, default=0.0
        Fase inicial en radianes.
    offset : float, default=0.0
        Desplazamiento DC en voltios.

    Retorna:
    --------
    ndarray
        Señal cuadrada (mismo tamaño que `t`).

    Notas:
    ------
    - `frequency` y `amplitude` deben ser > 0.
    - `duty` debe estar en el rango (0, 1).
    - `offset` desplaza la señal hacia arriba.
    """
    t = np.asarray(t, dtype=float)
    if frequency <= 0:
        raise ValueError('frequency debe ser > 0')
    if amplitude <= 0:
        raise ValueError('amplitude debe ser > 0')
    if duty <= 0 or duty >= 1:
        raise ValueError('duty debe estar entre 0 y 1 (excluyendo los extremos)')
    if not np.isfinite(phase):
        raise ValueError('phase debe ser un número finito')
    if offset < 0:
        raise ValueError('offset debe ser >= 0')

    period = 1.0 / frequency
    t_mod = np.mod(t + phase / (2.0 * np.pi * frequency), period)
    y = np.where(t_mod < duty * period, offset + amplitude, offset)
    return y


def sinusoidal_signal(t, frequency, amplitude, phase=0.0, offset=0.0):
    """Genera una señal sinusoidal configurable.

    La señal se define como: y(t) = offset + amplitude * sin(2*pi*frequency*t + phase)

    Parámetros:
    -----------
    t : array-like
        Vector de tiempos (s).
    frequency : float
        Frecuencia de la señal (Hz).
    amplitude : float
        Amplitud de pico de la señal (V).
    phase : float, default=0.0
        Fase inicial en radianes.
    offset : float, default=0.0
        Desplazamiento DC en voltios.

    Retorna:
    --------
    ndarray
        Señal sinusoidal (mismo tamaño que `t`).

    Notas:
    ------
    - `frequency` y `amplitude` deben ser > 0.
    - `offset` puede desplazar la señal en DC.
    - La función devuelve la forma de onda analógica adecuada como entrada
      para simulaciones o para muestreo/quantización posterior.
    """
    t = np.asarray(t, dtype=float)
    if frequency <= 0:
        raise ValueError('frequency debe ser > 0')
    if amplitude <= 0:
        raise ValueError('amplitude debe ser > 0')
    if not np.isfinite(phase):
        raise ValueError('phase debe ser un número finito')

    y = offset + amplitude * np.sin(2.0 * np.pi * frequency * t + float(phase))
    return y


