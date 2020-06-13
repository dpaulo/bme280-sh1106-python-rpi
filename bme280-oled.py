import os
import time
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280

#Initialise the OLED
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

# Initialise the BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)


def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), 'fonts', name))
    return ImageFont.truetype(font_path, size)

def main():
    myFont = make_font("miscfs_.ttf", 12)
    while True:
            with canvas(device) as draw:
                draw.rectangle(device.bounding_box, outline="white")
                draw.text((6, 2), "Temperature {:05.2f}\nHumidity {:05.2f}\nPressure {:05.2f}".format((bme280.get_temperature()),(bme280.get_humidity()),(bme280.get_pressure())), fill="white", font=myFont)
            time.sleep(1)
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass