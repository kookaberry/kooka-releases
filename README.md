Kookaberry firmware and IDE
===========================

The Kookaberry is a microcontroller board used for teaching computing in
Australian schools.  It runs MicroPython which allows you to easily program
the board in the Python programming language.

Here you can find official releases of the Kookaberry firmware and the
Kookaberry IDE.

For documentation see: <http://docs.micropython.org/en/kookaberry/kookaberry/quickref.html>

Firmware upgrade
----------------

The firmware files are:
- f103.bin -- firmware for the F103
- f091.bin -- firmware for the F091
- nrf5.bin -- firmware for the nRF51

Installation:

1) Make sure the device has the low-level bootloader installed, it is required for
   the following steps to work.

2) Plug the device in USB and it should appear as a mass storage device.
   If the blue LED is blinking once every second then the FEP is in recovery
   mode, otherwise it is in normal mode.  In both cases files can be copied to
   the device for an upgrade.

3) Copy f103.bin, f091.bin, nrf5.bin to the root of the drive.

4) Unplug and re-plug the device from USB.

5) The blue LED should flash for about 30 seconds while it prgrams the F103,
   F091 and nRF51.

6) Once the blue LED stops flashing the device should be ready to use.

Usage
-----

- Hold down "RESET" during power-up (eg plugging into USB) to make the FEP enter
  recovery mode.  In this mode only the filesystem is accessible over USB.
  Everything else is disabled.  This mode is indicated by the blue LED blinking
  once every second.  To get out of this mode unplug the device from USB.

- Press "RESET" when the device is powered on to perform a hard reset of the F091
  and the nRF51822.

- If the supply voltage is very low (less than 2.5V) upon power up then the blue
  LED will pulse slowly and the device will be completely disabled.

- If the supply voltage (VCC) becomes low (less than 2.7V) during operation then
  the blue LED will pulse slowly to indicate this fact.  The device is otherwise
  still fully operational.

- Apps should go in the "/app" directory on the drive.  Libraries should go in the
  "/lib" directory on the drive.

- Hold down "B" during power-up or reset to enter the app menu.
