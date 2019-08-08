# MicroPython driver for the AS726X spectral sensor

from micropython import const
import time, struct

_SENSORTYPE_AS7262 = const(0x3e)
_SENSORTYPE_AS7263 = const(0x3f)

_AS726x_DEVICE_TYPE = const(0x00)
_AS726x_HW_VERSION = const(0x01)
_AS726x_CONTROL_SETUP = const(0x04)
_AS726x_INT_T = const(0x05)
_AS726x_DEVICE_TEMP = const(0x06)
_AS726x_LED_CONTROL = const(0x07)

_AS72XX_SLAVE_STATUS_REG = const(0x00)
_AS72XX_SLAVE_WRITE_REG = const(0x01)
_AS72XX_SLAVE_READ_REG = const(0x02)

_AS72XX_SLAVE_TX_VALID = const(0x02)
_AS72XX_SLAVE_RX_VALID = const(0x01)

# Delay between checking for virtual register changes
POLLING_DELAY_MS = 5

class AS726X:
    def __init__(self, i2c, addr=0x49, mode=3, gain=3, integration_time=50):
        self._i2c = i2c
        self.addr = addr
        self.buf1 = bytearray(1)
        self.init_device(mode, gain, integration_time)

    def read_u8(self, reg):
        self._i2c.readfrom_mem_into(self.addr, reg, self.buf1)
        return self.buf1[0]

    def write_8(self, reg, val):
        self.buf1[0] = val
        return self._i2c.writeto_mem(self.addr, reg, self.buf1)

    # Read a virtual register from the AS726x
    def virt_read(self, reg):
        # Do a prelim check of the read register
    	if self.read_u8(_AS72XX_SLAVE_STATUS_REG) & _AS72XX_SLAVE_RX_VALID:
    	   self.read_u8(_AS72XX_SLAVE_READ_REG) # Read the byte but do nothing with it

        # Wait for WRITE register to be empty
        while self.read_u8(_AS72XX_SLAVE_STATUS_REG) & _AS72XX_SLAVE_TX_VALID:
            time.sleep_ms(POLLING_DELAY_MS)

        # Send the virtual register address (bit 7 clear to indicate a read)
        self.write_8(_AS72XX_SLAVE_WRITE_REG, reg)

        # Wait for READ flag to be set
        while not self.read_u8(_AS72XX_SLAVE_STATUS_REG) & _AS72XX_SLAVE_RX_VALID:
            time.sleep_ms(POLLING_DELAY_MS)

        return self.read_u8(_AS72XX_SLAVE_READ_REG)

    # Write to a virtual register in the AS726x
    def virt_write(self, reg, value):
        # Wait for WRITE register to be empty
        while self.read_u8(_AS72XX_SLAVE_STATUS_REG) & _AS72XX_SLAVE_TX_VALID:
            time.sleep_ms(POLLING_DELAY_MS)

        # Send the virtual register address (bit 7 set to indicate a write)
        self.write_8(_AS72XX_SLAVE_WRITE_REG, 0x80 | reg)

        # Wait for WRITE register to be empty
        while self.read_u8(_AS72XX_SLAVE_STATUS_REG) & _AS72XX_SLAVE_TX_VALID:
            time.sleep_ms(POLLING_DELAY_MS)

        # Send the data to complete the operation
        self.write_8(_AS72XX_SLAVE_WRITE_REG, value)

    def virt_modify(self, addr, and_, or_):
    	self.virt_write(addr, self.virt_read(addr) & and_ | or_)

    def init_device(self, mode, gain, integration_time):
        self._sens_ver = self.virt_read(_AS726x_HW_VERSION)
        if self._sens_ver != _SENSORTYPE_AS7262 and self._sens_ver != _SENSORTYPE_AS7263:
            raise ValueError("wrong sensor version 0x%02x" % self._sens_ver)
        self.set_bulb_current(0)
        self.set_bulb(False)
        self.set_indicator_current(0)
        self.set_indicator(False)
        self.set_integration_time(integration_time)
        self.set_gain(gain)
        self.set_measurement_mode(mode)

    #Sets the measurement mode
    #Mode 0: Continuous reading of VBGY (7262) / STUV (7263)
    #Mode 1: Continuous reading of GYOR (7262) / RTUX (7263)
    #Mode 2: Continuous reading of all channels (power-on default)
    #Mode 3: One-shot reading of all channels
    def set_measurement_mode(self, mode):
        self.virt_modify(_AS726x_CONTROL_SETUP, 0b11110011, mode << 2)

    #Sets the gain value
    #Gain 0: 1x (power-on default)
    #Gain 1: 3.7x
    #Gain 2: 16x
    #Gain 3: 64x
    def set_gain(self, gain):
        self.virt_modify(_AS726x_CONTROL_SETUP, 0b11001111, gain << 4)

    #Sets the integration value
    #Give this function a byte from 0 to 255.
    #Time will be 2.8ms * [integration value]
    def set_integration_time(self, integration_time):
        self.virt_write(_AS726x_INT_T, integration_time)

    #Set the current limit of bulb/LED.
    #Current 0: 12.5mA
    #Current 1: 25mA
    #Current 2: 50mA
    #Current 3: 100mA
    def set_bulb_current(self, current):
        self.virt_modify(_AS726x_LED_CONTROL, 0b11001111, current << 4)

    def set_bulb(self, on):
        self.virt_modify(_AS726x_LED_CONTROL, ~(1 << 3), on << 3)

    def set_indicator(self, on):
        self.virt_modify(_AS726x_LED_CONTROL, ~(1 << 0), on << 0)

    # Set the current limit of onboard LED. Default is max 8mA = 0b11
    def set_indicator_current(self, current):
    	self.virt_modify(_AS726x_LED_CONTROL, 0b11111001, current << 1)

    def clear_data_available(self):
    	self.virt_modify(_AS726x_CONTROL_SETUP, ~(1 << 1), 0)

    def data_available(self):
        return self.virt_read(_AS726x_CONTROL_SETUP) & (1 << 1)

    def get_calibrated_value(self, cal_address):
        b_arr = bytearray(4)
        b_arr[0] = self.virt_read(cal_address + 0);
        b_arr[1] = self.virt_read(cal_address + 1);
        b_arr[2] = self.virt_read(cal_address + 2);
        b_arr[3] = self.virt_read(cal_address + 3);
        return struct.unpack('>f', b_arr)[0]

    def get_calibrated_values(self):
        return [self.get_calibrated_value(i) for i in range(0x14, 0x2c, 4)]

    def take_measurements(self):
        self.clear_data_available()
        self.set_measurement_mode(3);
        while not self.data_available():
            time.sleep_ms(POLLING_DELAY_MS)
        # Readings can now be accessed via get_calibrated_value[s]

    def take_measurements_with_bulb(self):
        self.set_bulb(True)
        self.take_measurements()
        self.set_bulb(False)

    #Returns the temperature in C
    #Pretty inaccurate: +/-8.5C
    def get_temperature(self):
        return self.virt_read(_AS726x_DEVICE_TEMP)

    def soft_reset(self):
    	self.virt_modify(_AS726x_CONTROL_SETUP, 0xff, 1 << 7)
        time.sleep_ms(800)

    def get_sensor_type(self):
        if self._sens_ver == _SENSORTYPE_AS7262:
            return "AS7262"
        elif self._sens_ver == _SENSORTYPE_AS7263:
            return "AS7263"
        else:
            return "unknown"

    def get_wavelengths(self):
        if self._sens_ver == _SENSORTYPE_AS7262:
            return [450, 500, 550, 570, 600, 650]
        else:
            return [610, 680, 730, 760, 810, 860]
