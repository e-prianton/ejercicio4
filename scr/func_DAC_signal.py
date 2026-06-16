import numpy as np
import matplotlib.pyplot as plt
from scr.func_generic_signals import trapezoidal_signal



def trapezoidal_dac_samples(frequency, amplitude, fs, duration, 
                            duty_low=0.0, duty_rise=0.25, duty_high=0.5,
                            offset=0.0, bits=12, v_ref=None, clip=True):
    """Genera muestras cuantizadas de una señal trapezoidal para entrada a un DAC.
    
    Parámetros:
    -----------
    frequency : float
        Frecuencia de la señal (Hz).
    amplitude : float
        Amplitud de pico de la señal (V) sobre el offset.
        La señal varía entre `offset` y `offset + amplitude`.
    fs : float
        Frecuencia de muestreo (Hz).
    duration : float
        Duración total de la señal (s).
    duty_low : float, default=0.0
        Fracción del periodo para el nivel bajo (offset constante).
    duty_rise : float, default=0.25
        Fracción del periodo para la subida.
    duty_high : float, default=0.5
        Fracción del periodo para el nivel alto.
    offset : float, default=0.0
        Nivel bajo de voltaje.
    bits : int, default=12
        Resolución del DAC (bits). Valores típicos: 8, 10, 12, 16.
    v_ref : float or None, default=None
        Voltaje de referencia del DAC. Si None, se usa `offset + amplitude`.
    clip : bool, default=True
        Recortar la señal a [0, v_ref] antes de cuantizar.
    
    Retorna:
    --------
    t : ndarray
        Vector de tiempos muestreados (s).
    y : ndarray
        Señal trapezoidal en voltios (valores reales).
    codes : ndarray
        Códigos digitales cuantizados para el DAC (enteros sin signo).
    
    Notas:
    ------
    - Los códigos varían de 0 a 2^bits - 1.
    - La señal se mapea linealmente de [0, v_ref] a [0, 2^bits-1].
    """
    if fs <= 0:
        raise ValueError('fs debe ser > 0')
    if duration <= 0:
        raise ValueError('duration debe ser > 0')
    if bits <= 0 or bits > 32:
        raise ValueError('bits debe estar entre 1 y 32')
    if offset < 0:
        raise ValueError('offset debe ser >= 0')
    
    if v_ref is None:
        v_ref = offset + amplitude
    
    # Generar vector de tiempos
    t = np.arange(0.0, duration, 1.0 / fs)
    
    # Generar señal analógica
    y = trapezoidal_signal(t, frequency, amplitude, duty_low, duty_rise, duty_high, offset)
    
    # Recortar si es necesario
    if clip:
        y = np.clip(y, 0.0, v_ref)
    
    # Señal escalada a códigos digitales: mapear [0, v_ref] -> [0, 2^bits - 1]
    max_code = 2**bits - 1
    codes = np.round((y / v_ref) * max_code)
    
    # Convertir al tipo de dato apropiado
    if bits <= 8:
        codes = np.asarray(codes, dtype=np.uint8)
    elif bits <= 16:
        codes = np.asarray(codes, dtype=np.uint16)
    else:
        codes = np.asarray(codes, dtype=np.uint32)
    
    return t, y, codes


# ============================================================================
# EJEMPLO DE USO Y PRUEBA
# ============================================================================

if __name__ == '__main__':
    # Parámetros de ejemplo
    freq = 50  # Hz
    amp = 3.3  # V (típico para electrónica digital)
    fs = 8000  # Hz (frecuencia de muestreo)
    duration = 0.1 # s (100 ms = 5 periodos a 50 Hz)
    dac_bits = 12  # DAC de 12 bits (4096 niveles)
    
    # Generar muestras con nivel bajo y offset
    t, y_analog, codes = trapezoidal_dac_samples(
        frequency=freq,
        amplitude=2.8,
        fs=fs,
        duration=duration,
        duty_low=0.2,   # 20% del periodo en nivel bajo
        duty_rise=0.2,  # 20% del periodo en subida
        duty_high=0.4,  # 40% del periodo en nivel alto
        offset=0.0,     # nivel bajo de 0.5 V
        bits=dac_bits,
        v_ref=3.3
    )
    amp = 2.8
    offset = 0.0
    
    # Guardar en archivo .npy (entrada para DAC)
    np.save('dac_samples.npy', codes)
    print(f'✓ Muestras DAC guardadas en dac_samples.npy')
    print(f'  - Cantidad de muestras: {len(codes)}')
    print(f'  - Resolución: {dac_bits} bits (rango: 0-{2**dac_bits - 1})')
    print(f'  - Rango de códigos: {codes.min()}-{codes.max()}')
    
    # Visualizar
    plt.figure(figsize=(12, 6))
    
    # Gráfico 1: Señal analógica
    plt.subplot(2, 1, 1)
    plt.plot(t, y_analog, 'b-', linewidth=1.5, label='Señal analógica')
    plt.ylabel('Voltaje (V)')
    plt.title(f'Señal trapezoidal configurable (f={freq} Hz, A={amp} V)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # Gráfico 2: Muestras cuantizadas
    plt.subplot(2, 1, 2)
    codes_scaled = codes / (2**dac_bits - 1) * amp  # Reescalar a voltios
    plt.step(t, codes_scaled, 'r-', where='post', linewidth=1, label='Muestras cuantizadas')
    plt.plot(t, y_analog, 'b-', linewidth=1, alpha=0.5, label='Señal analógica')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Voltaje (V)')
    plt.title(f'Muestras DAC cuantizadas ({dac_bits} bits, fs={fs} Hz)')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    plt.tight_layout()
    plt.savefig('trapezoidal_dac.png', dpi=100)
    print(f'✓ Gráfico guardado en trapezoidal_dac.png')
    
    # Mostrar ventana gráfica si hay servidor X11
    try:
        plt.show()
    except Exception as e:
        print(f'  (No hay servidor gráfico disponible: {e})')
