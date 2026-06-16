import time
import spidev
from scr.func_DAC_signal import trapezoidal_dac_samples

# Genera códigos para un DAC real
t, y, codes = trapezoidal_dac_samples(
    frequency=50,
    amplitude=2.8,
    fs=8000,
    duration=0.02,
    duty_low=0.2,
    duty_rise=0.2,
    duty_high=0.4,
    offset=0.5,
    bits=12,
    v_ref=3.3
)

# Abrir SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000

dt = 1.0 / 8000
for code in codes:
    high = (code >> 8) & 0x0F
    low = code & 0xFF
    spi.xfer2([high | 0x30, low])  # depende del DAC usado
    time.sleep(dt)

spi.close()