#!python

# A demo that writes to all 8 possible OLED addresses on a single SPI bus.

import time
import datetime

# import sys
# sys.path.insert(0, '../src/')

from spi_adapter import SpiAdapter, AuxPinMode
from luma.oled.device import ssd1306, sh1106
from luma.core.render import canvas
from PIL import ImageFont, ImageColor



# Customize for your system.
my_port = "COM18"
speed = 4000000


class MyLumaSerial:
    """Implementation of the luma.core.interface.serial interface using an SPI Adapter.
    See luma.core.interface.serial.spi for an example.
    """

    def __init__(self, spi:SpiAdapter, addr: int):
        """Open the SPI Adapter and initialize this Luma serial instance."""
        assert isinstance(spi, SpiAdapter)
        assert isinstance(addr, int)
        assert 0 <= addr <= 7
        self.__spi = spi
        self.__addr = addr
        # Reset the OLED.
        self.__send(bytearray(), dc=0, rst=0)
        time.sleep(0.001)
        self.__send(bytearray(), dc=0, rst=1)

    def __send(self, data: bytearray, dc: int, rst: int = 1) -> None:
        """Send data to self.__addr, with given dc and rst output values."""
        assert isinstance(data, bytearray)
        assert len(data) <= 256
        assert isinstance(dc, int)
        assert 0 <= dc <= 1
        assert isinstance(rst, int)
        assert 0 <= rst <= 1
        rst_mask = 0b10000 if rst else 0
        dc_mask = 0b01000 if dc else 0
        control_byte = rst_mask | dc_mask | self.__addr
        payload = bytearray()
        payload.append(control_byte)
        payload.extend(data)
        resp = self.__spi.send(payload, cs=0, mode=0, speed=speed, read=False)
        assert resp is not None

    def command(self, *cmd) -> None:
        """Send to the SPI display a command with given bytes."""
        data = bytearray()
        self.__send(bytearray(list(cmd)), dc=0)


    def data(self, data):
        """Send to the SPI display data with given bytes."""
        i = 0
        n = len(data)
        while i < n:
            # Limit each write to 256 bytes, including the control byte,
            # per the limitations of the underlying SPI driver.
            chunk_size = min(255, n - i)
            payload = bytearray(data[i : i + chunk_size])
            self.__send(payload, dc=1)
            i += chunk_size

# Maps OLED address to a Luma drvice.
luma_devices = {}

spi = SpiAdapter(port = my_port)
for device_addr in range(8):
  luma_serial = MyLumaSerial(spi, device_addr)
  #luma_device = ssd1306(luma_serial, width=128, height=64, rotate=0)
  luma_device = sh1106(luma_serial, width=128, height=64, rotate=0)
  # luma_device.persist = True  # Do not clear display on exit
  luma_devices[device_addr] = luma_device


font = ImageFont.truetype("./fonts/FreePixel.ttf", 16)
white = ImageColor.getcolor("white", "1")
black = ImageColor.getcolor("black", "1")

while True:
    time_str = "{0:%H:%M:%S}".format(datetime.datetime.now())
    print(f"Drawing {time_str}", flush=True)
    for device_addr, luma_device in luma_devices.items():
      with canvas(luma_device) as draw:
          draw.rectangle(luma_device.bounding_box, outline=white, fill=black)
          draw.text((43, 14), f"OLED {device_addr}", fill=white, font=font)
          draw.text((33, 40), f"{time_str}", fill=white, font=font)
          # Uncomment to save screenshot.
          # draw._image.save("oled_demo_screenshot.png")
    time.sleep(1.0)
