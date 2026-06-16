import numpy as np
import matplotlib.pyplot as plt
from scr.func_generic_signals import trapezoidal_signal


def simulate_rc_filter(t, input_signal, rc):
    y = np.zeros_like(input_signal)
    dt = t[1] - t[0]
    for i in range(1, len(t)):
        y[i] = y[i-1] + (dt / rc) * (input_signal[i-1] - y[i-1])
    return y


if __name__ == '__main__':
    fs = 10000
    duration = 0.05
    t = np.linspace(0.0, duration, int(fs * duration), endpoint=False)

    y_in = trapezoidal_signal(
        t,
        frequency=20,
        amplitude=4.0,
        duty_low=0.1,
        duty_rise=0.3,
        duty_high=0.4,
        offset=1.0
    )

    y_out = simulate_rc_filter(t, y_in, rc=0.002)

    plt.figure(figsize=(10, 5))
    plt.plot(t, y_in, label='Entrada trapezoidal', linewidth=1.5)
    plt.plot(t, y_out, label='Salida filtro RC', linewidth=1.5)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Voltaje (V)')
    plt.title('Ejemplo genérico: señal trapezoidal sin DAC')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
