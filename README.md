Kookaberry firmware and IDE
===========================

The Kookaberry is a microcontroller board used for teaching computing in
Australian schools.  It runs MicroPython which allows you to easily program
the board in the Python programming language.

Here you can find official releases of the Kookaberry firmware and the
Kookaberry PC Suite, which includes an IDE, a Teacher's Window and a
Blockly editor.

The latest release packages can be found at: <https://github.com/kookaberry/kooka-releases/releases>

Individual files can be found by browsing this repository, in the following
directories:

- `KookaSuite/` contains executable installation files for Windows and macOS
  versions of the Kookaberry PC Suite.
- `firmware/` contains the firmware that goes on the Kookaberry board.
- `lib/` contains various libraries/modules for use on the Kookaberry board.

For documentation see: <http://docs.micropython.org/en/kookaberry/kookaberry/quickref.html>

Firmware upgrade
----------------

The firmware files are:
- f103.bin -- firmware for the F103
- f091.bin -- firmware for the F091
- nrf5.bin -- firmware for the nRF51
- l476.bin -- firmware for the L476

Installation:

1) Make sure the device has the low-level bootloader installed, it is required for
   the following steps to work.

2) Plug the device in USB and it should appear as a mass storage device.
   If the blue LED is blinking once every second then the FEP is in recovery
   mode, otherwise it is in normal mode.  In both cases files can be copied to
   the device for an upgrade.

3) Copy f103.bin, f091.bin, nrf5.bin to the root of the drive (use l476.bin instead
   of f091.bin on Kookaberry L476 boards).

4) Unplug and re-plug the device from USB.

5) The blue LED should flash for about 30 seconds while it prgrams the F103,
   F091 (or L476) and nRF51.

6) Once the blue LED stops flashing the device should be ready to use.

Usage
-----

- Hold down "RESET" during power-up (eg plugging into USB) to make the FEP enter
  recovery mode.  In this mode only the filesystem is accessible over USB.
  Everything else is disabled.  This mode is indicated by the blue LED blinking
  once every second.  To get out of this mode unplug the device from USB.

- Press "RESET" when the device is powered on to perform a hard reset of the
  F091/L476 and the nRF51822.

- If the supply voltage is very low (less than 2.5V) upon power up then the blue
  LED will pulse slowly and the device will be completely disabled.

- If the supply voltage (VCC) becomes low (less than 2.7V) during operation then
  the blue LED will pulse slowly to indicate this fact.  The device is otherwise
  still fully operational.

- Apps should go in the "/app" directory on the drive.  Libraries should go in the
  "/lib" directory on the drive.

- Hold down "B" during power-up or reset to enter the app menu.
