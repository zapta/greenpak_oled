# Addressable SPI OLED display

This design demonstrates the techinque of adding device addressing capabilities to a SPI bus. This provides the speed and distance of an SPI bus with the simplicity and extensibility of an I2C bus.

The addressability is achieved using a Renesas's GreenPAK SPLD devices which interprets the first byte of each SPI transaction as a meta control byte and passes the CS signal to the device only if the address encoded in the control byte matches the device's address.

Resources
* PCB schematic: https://github.com/zapta/greenpak_oled/blob/main/kicad/greenpak_oled.pdf
* GreenPAK design schematic: https://github.com/zapta/greenpak_oled/blob/main/greenpak/greenpak_oled.svg
* GreenPAK source and hex files: https://github.com/zapta/greenpak_oled/tree/main/greenpak

<br>

PCB Components side:
<img  src="https://raw.githubusercontent.com/zapta/greenpak_oled/main/www/greenpak_oled.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 80%;" />

PCB OLED display side:
<img  src="https://raw.githubusercontent.com/zapta/greenpak_oled/main/www/greenpak_oled_rear.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 80%;" />


## Protocol

A SPI transaction is a sequence of bytes transfer between a high-to-low and a low-to-high transions of the ``CS`` signal. To tag a transaction with a device address, prepend to it a control byte which include the target devcie address as well as the desired states of the SSD1306 OLED ``RST`` and ``DC`` inputs.

| Bit field    | Funtion     | Description     |
|--------------|-------------|------------|
| Bits [7:5]   |  Reserved   | Set to 0.      |
| Bits [4:4]   |  RST        | The value of the OLED RST input. |
| Bits [3:4]   |  DC         | The value of the OLED D/C input  |
| Bits [2:1]   |  Address    | The target devcie address in the range [0, 7]   |

The address of each device is set by its three solder jumbers, with an open jumper
representing ``0`` and short jumper representing ``1``

## The Demo program

The Python program demo_oled.py demostrates the addressability by continiously writing a different contet to each of the eight possible device addresses. Connecting one or more 
device will display on each a number that identify it's address. The demo uses a USB to SPI adapter, such as a plain Raspberry Pi Pico, that is compatible with the  Python package ``spi-adapter``.

## Timing diagrams
TBD

## Construction
TBD



