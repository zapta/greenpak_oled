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

## Device SPI address
The device address is set by shorting with solder the neccessary solder jumpers according to this table:

|Address    | A1    | A1    | A0   |
|:--------------:|:-------------:|:------------:|:----:|
| 0   |  -   |  -    |  - |
| 1   |  -   |  -    |  Solder |
| 2   |  -   |   Solder   | -  |
| 3   |  -   |   Solder   | Solder  |
| 4   | Solder    |  -    | -  |
| 5   | Solder    |  -    |  Solder |
| 6   | Solder    |   Soler   | -  |
| 7   | Solder    |   Solder   | Solder  |


## The Demo program

The Python program demo_oled.py demostrates the addressability by continiously writing a different contet to each of the eight possible device addresses. Connecting one or more 
device will display on each a number that identify it's address. The demo uses a USB to SPI adapter, such as a plain Raspberry Pi Pico, that is compatible with the  Python package ``spi-adapter``.

## Timing diagrams
TBD

## Makeing your own

To make your own Addressable SPI OLED display follow these steps:
1. Order the PCB and components.
1. Assemble the components, including the OLED panel which is soldered to the 30 pags strip.
1. Program the GreenPAK device as described below.
1. Set the display address on the SPI bus by soldering the necessary solder jumpers.


## Flashing the GreenPAK

Flashing the GreenPAK IC can be done in-cirucit via the programming pads which provides access to its I2C pins. The Python program flasher.py allows to program it using an USB to I2C adapter such as the Raspberry Pi Pico, which is supported by the Python ``i2c_adapter`` package. 

## FAQ


Q: What SPI mode is used?

A: SPI mode 0 as required by the SSD1306

---

Q: What SPI speeds are supported?

A: We tested it successfuly with 4Mhz SPI clock.

---

Q: Why only 3 address jumpers?

A: We run out of resources in the GreenPAK device. 

---

Q: I want to change the design of the GreenPAK device, what tools do I need?

A: The Go Configure tool is available for free from Renesas and it allows to edit and test GreenPAK designs.  https://www.renesas.com/us/en/software-tool/go-configure-software-hub

---

Q: Why GreenPAK?

A: They are inexpensive, stand alone, flexible, have a small footprint, not requing supporting functionality.

---

Q: What kind of a guarantee do you provide with this design?

A: None whatsoever, the design is provided 'as-is'.

---

Q: This design doesn't uses MISO. Is it possible have MISO reading with addressible SPI?

A: Yes. A MISO signal can be used without having to change the GreenPAK's design.








