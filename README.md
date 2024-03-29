# Addressable SPI OLED display

This design demonstrates the technique of adding device addressing capabilities to a SPI bus. This provides the speed and distance of an SPI bus with the simplicity and extensibility of an I2C bus.

The addressability is achieved using a Renesas's GreenPAK SPLD devices which interprets the first byte of each SPI transaction as a meta control byte and passes the CS signal to the device only if the address encoded in the control byte matches the device's address. The supported OLED displays are 1.3" SSD1306 and SH1106. 

> **NOTE**: The SSD1306 and the SH1106 are compatible at the hardware level but require different software drivers.

Resources
* PCB schematic: https://github.com/zapta/greenpak_oled/blob/main/kicad/greenpak_oled.pdf
* GreenPAK design schematic: https://github.com/zapta/greenpak_oled/blob/main/greenpak/greenpak_oled.svg
* GreenPAK source and hex files: https://github.com/zapta/greenpak_oled/tree/main/greenpak
* Interactive BOM: https://htmlpreview.github.io/?https://github.com/zapta/greenpak_oled/blob/main/kicad/bom/ibom.html

<br>

Components side:

<img  src="www/greenpak_oled.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 40%;" />

<br>

Display panel side:

<img  src="www/greenpak_oled_rear.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 40%;" />

<br>

Wiring diagram (for oled_demo.py):

<img  src="www/wiring_diagram.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 100%;" />

## Protocol

A SPI transaction is a sequence of bytes transfer between a high-to-low and a low-to-high transitions of the ``CS`` signal. To tag a transaction with a device address, prepend to it a control byte which include the target device address as well as the desired states of the OLED ``RST`` and ``DC`` inputs.

| Bit field    | Function     | Description     |
|--------------|-------------|------------|
| Bits [7:5]   |  Reserved   | Set to 0.      |
| Bits [4:4]   |  RST        | The value of the OLED RST input. |
| Bits [3:4]   |  DC         | The value of the OLED D/C input  |
| Bits [2:1]   |  Address    | The target device address in the range [0, 7]   |

The address of each device is set by its three solder jumbers, with an open jumper
representing ``0`` and short jumper representing ``1``

## Device SPI address

The device address is set by shorting with solder the necessary solder jumpers according to this table:

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

## oled_demo.py

The Python program demo_oled.py demonstrates the addressability by continuously writing a different content to each of the eight possible device addresses. Connecting one or more 
device will display on each a number that identify it's address. The demo uses a USB to SPI adapter, such as a plain Raspberry Pi Pico, that is compatible with the  Python package ``spi-adapter``.

## Timing diagrams

The screenshot below shows a typical address enabled SPI transaction. The first byte 
is the control byte ``0x12`` contains the signals ``OLED_RST=1``, ``OLED_DC=0``, and is ``ADDRESS=2``, and is matched against the device address, which happens to be 2,  and causes a match. This sets the ``OLED_RST`` and ``OLED_DC`` outputs to their respective values (no change in the case of ``OLED_RST``) and then enables ``OLED_CS`` such that the rest of the bytes are processed by the OLED device.

<br>

<img  src="www/signal_capture1.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 100%;" />

The following diagram zoom on the control byte. Note that the ``OLED_DC`` (and so ``OLED_RST`` when changed) stabilizes on its new level before  ``OLED_CS`` is asserted low.

<br>

<img  src="www/signal_capture2.png"
      style="display: block;margin-left: auto;margin-right: auto;width: 100%;" />


## How it works?

The diagram below shows the main functional blocks of the GreenPAK design. For full details and the latest version, explore the design file ``greenpak_oled.gp6`` file using the Renesas design tool.

1. I2C programming support. Used only for flashing or reflashing the GreenPAK device and is not used in normal operation.
2. Serial to parallel shifter. A shift register that provides the four previous SPI bit values.
3. First byte detector. Generates signal that indicates the time of the 8'th bit of the control byte (the first byte in the SPI transaction)
4. Address matcher. On the last bit of the control byte, tests if the address matches.
5. OLED_CS generator. A latch that generates the the ``OLED_CS`` output signals.
6. Auxiliary signals generators. Latches for the ``OLED_RST`` and ``OLED_DC`` output signals.
  
<br>

<img  src="www/greenpak_oled.svg"
      style="display: block;margin-left: auto;margin-right: auto;width: 100%;" />

## Making your own

To make your own Addressable SPI OLED display follow these steps:

1. Order the PCB and components.
1. Assemble the components, including the OLED panel which is soldered to the 30 pags strip.
1. Program the GreenPAK device as described below.
1. Set the display address on the SPI bus by soldering the necessary solder jumpers.

The Github repository contains an HTML interactive BOM that helps identifying the components and their values.


## Flashing the GreenPAK

Flashing the GreenPAK IC can be done in-circuit via the programming pads which are compatible with the [GreenPAK Pogo Probe](https://github.com/zapta/greenpak_pogo). The provided Python program ``flasher.py`` allows to program it using an USB to I2C adapter such as the Raspberry Pi Pico, or the Sparkfun Pro Micro RP2040. which are supported by the Python ``i2c_adapter`` package. 

## FAQ

Q: What is the operating voltage of the OLED display.

A: 3.3V nominal.

---

Q: What SPI mode is used?

A: SPI mode 0 as required by the SSD1306 and SH1106 controllers.

---

Q: What SPI speeds are supported?

A: We tested it successfully with 4Mhz SPI clock.

---

Q: Why only 3 address jumpers?

A: We run out of resources in the GreenPAK device. 

---

Q: I want to change the design of the GreenPAK device, what tools do I need?

A: The Go Configure tool is available for free from Renesas and it allows to edit and test GreenPAK designs.  https://www.renesas.com/us/en/software-tool/go-configure-software-hub

---

Q: Why GreenPAK?

A: They are inexpensive, stand alone, flexible, have a small footprint, not requiring glue components.

---

Q: What kind of a guarantee do you provide with this design?

A: None whatsoever, the design is provided 'as-is'.

---

Q: This design doesn't uses MISO. Is it possible have MISO reading with addressable SPI?

A: Yes. A MISO signal can be used without having to change the GreenPAK's design.
