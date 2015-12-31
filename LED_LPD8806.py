#!/usr/bin/python
# -*- coding: utf-8 -*-

# Python SPI for LPD8806 driven LED strip:
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

from Adafruit_BBIO.SPI import SPI
#import Adafruit_BBIO.GPIO as GPIO

import time # useful for wait delay statements
global pixels

class LED_LPD8806(object):
  # Constructor
  def __init__(self):
	self.spi = SPI(0,0) #/dev/spidev1.0  (be sure to run Python with su if 'no permission'
	self.spi.msh=10000000 #SPI clock set to 10MHz
	self.spi.bpw = 8 # bits per word
	self.spi.threewire = False # not half-duplex
	self.spi.lsbfirst = False # we want MSB first
	self.spi.mode = 0 # options are modes 0 through 3
	self.spi.cshigh = False # we want chip select to be active low
	self.spi.open(0,0) # make it so
	time.sleep(0.05)

  def setup(self, led_pixels, debug=False):
	if (debug):
		print "Initializing LED strip"
	global pixels
	pixels = [[0x80 for x in range(3)] for y in range(led_pixels)]
	for i in range(led_pixels):
	        pixels[i]=[0x00, 0x00, 0x00]

  # Define LED functions:
  # --------------------

  # Update pixel display with a given delay time between pixel updates:
  def writestrip(self, delay):
	if (delay < 0):
		delay = 0
	for i in range(len(pixels)):
		self.spi.writebytes([0x00, 0x00, 0x00]) #prepare write
	for i in range(len(pixels)):
		self.spi.writebytes(pixels[i]) #write colors to pixels
		time.sleep(delay)

  # Turn off all LEDs:
  def clearstrip(self):
	global pixels
	for i in range(len(pixels)):
		self.spi.writebytes([0x00, 0x00, 0x00]) #prepare write
	for i in range(len(pixels)):
		pixels[i] = [0x80, 0x80, 0x80]
	self.writestrip(0)


  # Set an individual pixel to a specific color (to display later):
  def setpixelcolor(self, n, g, r, b):
	global pixels
	if (n >= len(pixels)):
		return
	if (n < 0):
		return
	if (g > 0xFF):
		g = 0xFF
	if (g < 0x80):
		g = 0x80
	if (r > 0xFF):
		r = 0xFF
	if (r < 0x80):
		r = 0x80
	if (b > 0xFF):
		b = 0xFF
	if (b < 0x80):
		b = 0x80
	pixels[n] = [g, r, b]

  # Update display with warmer colors (more red light) by a specified amount with a delay between pixels
  def warmstrip(self, warmth, delay):
	global pixels
	if (delay < 0):
		delay = 0
	for n in range(len(pixels)):
                if((pixels[n][1] + warmth) < 0x80):
                        pixels[n][1] = 0x80
                elif((pixels[n][2] + warmth) > 0xFF):
                        pixels[n][1] = 0xFF
                else:
			pixels[n][1] = pixels[n][1]+warmth
	self.writestrip(delay)

  # Update display with cooler colors (more blue) by a specified amount with a delay between each pixel
  def coolstrip(self, coolfactor, delay):
	global pixels
	if (delay < 0):
		delay = 0
	for n in range(len(pixels)):
                if((pixels[n][2] + coolfactor) < 0x80):
                        pixels[n][2] = 0x80
                elif((pixels[n][2] + coolfactor) > 0xFF):
                        pixels[n][2] = 0xFF
                else:
                        pixels[n][2] = pixels[n][2]+coolfactor

	self.writestrip(delay)

  # Update display with greener colors by a specified amount with a set delay between each pixel
  def greenstrip(self, lushness, delay):
	global pixels
	if (delay < 0):
		delay = 0
	for n in range(len(pixels)):
                if((pixels[n][0] + lushness) < 0x80):
                        pixels[n][0] = 0x80
                else:
                        pixels[n][0] = pixels[n][0]+lushness
	self.writestrip(delay)

  # Update display with brighter (whiter) light by specified amount with a set delay between pixel updates
  def brightenstrip(self, brightness, delay):
	global pixels
	if (delay < 0):
		delay = 0
        for n in range(len(pixels)):
                if((pixels[n][0] + brightness) < 0x80):
                        pixels[n][0] = 0x80
		elif((pixels[n][0] + brightness) > 0xFF):
			pixels[n][0] = 0xFF
                else:
                        pixels[n][0] = pixels[n][0]+brightness
                if((pixels[n][1] + brightness) < 0x80):
                        pixels[n][1] = 0x80
                elif((pixels[n][1] + brightness) > 0xFF):
                        pixels[n][1] = 0xFF
                else:
                        pixels[n][1] = pixels[n][1]+brightness
                if((pixels[n][2] + brightness) < 0x80):
                        pixels[n][2] = 0x80
                elif((pixels[n][2] + brightness) > 0xFF):
                        pixels[n][2] = 0xFF
                else:
                        pixels[n][2] = pixels[n][2]+brightness
	self.writestrip(delay)

  # Darken display (less light) by specified amount with a set delay between pixel updates
  def dimstrip(self, dimness, delay):
	global pixels
	if (delay < 0):
		delay = 0
	for n in range(len(pixels)):
		if((pixels[n][0] - dimness) < 0x80):
			pixels[n][0] = 0x80
                elif((pixels[n][0] - dimness) > 0xFF):
                        pixels[n][0] = 0xFF
		else:
			pixels[n][0] = pixels[n][0]-dimness
		if((pixels[n][1] - dimness) < 0x80):
			pixels[n][1] = 0x80
		elif((pixels[n][1] - dimness) > 0xFF):
			pixels[n][1] = 0xFF
		else:
			pixels[n][1] = pixels[n][1]-dimness
		if((pixels[n][2] - dimness) < 0x80):
			pixels[n][2] = 0x80
		elif((pixels[n][2] - dimness) > 0xFF):
			pixels[n][2] = 0xFF
		else:
			pixels[n][2] = pixels[n][2]-dimness
	self.writestrip(delay)



#spi.close() # done

