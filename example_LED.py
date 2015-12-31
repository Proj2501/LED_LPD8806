#!/usr/bin/python
# -*- coding: utf-8 -*-

# Example Python SPI for LPD8806 driven LED strip:
# JGronowski
# 2015-12-30
#
# Code inspired by:
# ----------------
# github path: 
# Adafruit-Raspberry-Pi-Python-Code/Adafruit_LEDpixels/Adafruit_LEDpixels.py
# and the article:
# http://mooresclouddev.markpesce.com/2012/10/18/about-lpd8806-based-rgb-led-strips/
#
# LPD8806 Hardware Examples:
# -----------------
# Digital RGB LED Weatherproof Strip - LPD8806 x 48 LED:
# 	https://www.adafruit.com/products/1948
# Digital RGB LED Weatherproof Strip - LPD8806 32 LED:
#	https://www.adafruit.com/products/306
#
# Usage Notes:
# -----------
# The LPD8806 can be run from a SPI bus using just the SI (data in) and
# SCK (clock) pins. Keep in mind that the LPD8806 cannot share the SPI bus
# with other devices, because of the likelihood of data collisions. True
# SPI devices on the bus will pay attention to the CS (chip select) pin
# signal should not get confused by communication intended for the LED
# strip.  The LPD8806 has no device id and will respond to all data on SI.
# The LPD8806 expects three bytes for each LED on the strip--one byte for
# each color component (RGB) of each LED. The first byte corresponds to
# the brightness of the Green light in the first LED. The second byte is Red,
# and the third byte is Blue.  The first bit (MSB) of each byte indicates
# whether the subsequent 7 bits should be shifted on to the next LPD8806
# or be held for the current LPD8806.  Consiquently, I am using 
# 0x00, 0x00, 0x00 to prep the LED strip for new color data.  Color data
# ranges from 0x80 0x80 0x80 (all colors off for 1 RGB LED) to
# 0xFF 0xFF 0xFF (all colors full on making 1 RGB LED turn white). 
#
# BBB pin connections:
# -------------------
# P9_1  = GND (power supply GND)
# P9_2  = GND
# P9_17 = CS  (a SPI pin not used by LPD8806)
# P9_18 = SI  (the yellow DAT pin)
# P9_21 = SO  (a SPI pin not used by LPD8806)
# P9_22 = SCK (the green CLK pin)
#
# Hardware Setup:
# --------------
# The 5 meter LED strip that I got from Adafruit came with double power and
# ground connections (one set connected to the header and the set is loose).
# Connect the extra power and GND pins from the LED strip to a barrel jack.
# https://www.adafruit.com/products/369
# This will be used to power the LED strip and can be used to power the BBB.
# Using some addtional wires, connect the strip's terminal to the BBB P9 
# header pins as above, and optionally connect the DC5V+ pin to the BBB P9_5
# pin or P9_6 pin which will supply 5V power to the BBB (these are VDD_5V).
# A 5V 10A power supply from Adafruit is used for the 5 meter strip.
# https://www.adafruit.com/products/658
# A 5V 2A power supply might be good enough for just 1 meter.  Be careful
# not to brown out the BBB by turning too many LED's white (all RGB on)
# at the same time if the power supply cannot provide enough current.

# Library Function Descriptions:
# -----------------------------
# writestrip(delay)
# 	Update pixel display with a given delay time between pixel updates where
#	delay is a floating point value in seconds

# clearstrip()
#	Turns all pixels off.

# setpixelcolor(n, g, r, b)
#   Sets the color of the nth pixel to the specified (g)reen, (r)ed, and (b)lue
#   values between 0x80 (off) and (0xFF) full on.
#
# warmstrip(warmth, delay)
#   Makes the pixel colors warmer by the specified factor.
#
# coolstrip(coolfactor, delay)
#   Makes the pixel colors cooler by the specified factor.
#
# greenstrip(lushness, delay)
#	Lushness is the amount of green light to add or subtract from the pixel colors.
#
# brightenstrip(brightness, delay)
#   Makes the whole LED strip brighter by the specified amount.
#
# dimstrip(dimness, delay)
#   Makes the whole LED strip darker by the specified amount.
#

import time # useful for wait delay statements
import LED_LPD8806

# Define LED strip size:
# ---------------------
pixels_per_meter = 48 	# usually 32 or 48
num_meters = 5 		# usually 1 to 5
# (optionally use your own integer value for a partial LED strip)
ledpixels = (pixels_per_meter + 1) * num_meters

# Draw pixels:
# -----------
debug = False
led = LED_LPD8806.LED_LPD8806()
led.setup(ledpixels, debug)
led.clearstrip() # turn off all LEDs
for n in range(ledpixels):
			      # Green, Red,  Blue
	led.setpixelcolor(n, 0xFF, 0x80, 0x80) # set all pixels full green
led.writestrip(0.001) # quickly update pixels with green
time.sleep(0.5) # hold this color for half a second

for n in range(ledpixels):
				# G,R,B
        led.setpixelcolor(n, 0x80, 0xFF, 0x80) # set all pixels full red
led.writestrip(0.01) # sweep the display update with red
time.sleep(0.5)

for n in range(ledpixels):
        led.setpixelcolor(n, 0x80, 0x8F, 0x8F) # set all pixels to purple
led.writestrip(0.0)	 # almost instantly change the display to purple
time.sleep(1.0)

for n in range(ledpixels):
        led.setpixelcolor(n, 0xE6, 0xFA, 0x20) # set all pixels to gold
led.writestrip(0.0)  # update display with gold
time.sleep(1.0)

for n in range(ledpixels):
        led.setpixelcolor(n, 0xF0, 0xF0, 0xF0) # set all pixels to white, but not full on
led.writestrip(0.0)
time.sleep(1.0)

# (remember the human eye has a logarithmic response to changes in light,
#  but a camera typically has a linear response to light)
led.dimstrip(50, 0.0)      # dimmer white light
time.sleep(1.0)
led.warmstrip(30, 0.0) # warmer color light 
time.sleep(1.0)
led.clearstrip()	       # turn everything off

#spi.close() # done with SPI


