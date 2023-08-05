import sys
import ctypes
class ChannelSubclass:
	# No subclass
	PHIDCHSUBCLASS_NONE = 1
	# Digital output duty cycle
	PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE = 16
	# Digital output frequency
	PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY = 18
	# Digital output LED driver
	PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER = 17
	# Encoder IO mode settable
	PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE = 96
	# Graphic LCD
	PHIDCHSUBCLASS_LCD_GRAPHIC = 80
	# Text LCD
	PHIDCHSUBCLASS_LCD_TEXT = 81
	# Spatial AHRS/IMU
	PHIDCHSUBCLASS_SPATIAL_AHRS = 112
	# Temperature sensor RTD
	PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD = 32
	# Temperature sensor thermocouple
	PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE = 33
	# Voltage sensor port
	PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT = 48
	# Voltage ratio bridge input
	PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE = 65
	# Voltage ratio sensor port
	PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT = 64

	@classmethod
	def getName(self, val):
		if val == self.PHIDCHSUBCLASS_NONE:
			return "PHIDCHSUBCLASS_NONE"
		if val == self.PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE:
			return "PHIDCHSUBCLASS_DIGITALOUTPUT_DUTY_CYCLE"
		if val == self.PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY:
			return "PHIDCHSUBCLASS_DIGITALOUTPUT_FREQUENCY"
		if val == self.PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER:
			return "PHIDCHSUBCLASS_DIGITALOUTPUT_LED_DRIVER"
		if val == self.PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE:
			return "PHIDCHSUBCLASS_ENCODER_MODE_SETTABLE"
		if val == self.PHIDCHSUBCLASS_LCD_GRAPHIC:
			return "PHIDCHSUBCLASS_LCD_GRAPHIC"
		if val == self.PHIDCHSUBCLASS_LCD_TEXT:
			return "PHIDCHSUBCLASS_LCD_TEXT"
		if val == self.PHIDCHSUBCLASS_SPATIAL_AHRS:
			return "PHIDCHSUBCLASS_SPATIAL_AHRS"
		if val == self.PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD:
			return "PHIDCHSUBCLASS_TEMPERATURESENSOR_RTD"
		if val == self.PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE:
			return "PHIDCHSUBCLASS_TEMPERATURESENSOR_THERMOCOUPLE"
		if val == self.PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT:
			return "PHIDCHSUBCLASS_VOLTAGEINPUT_SENSOR_PORT"
		if val == self.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE:
			return "PHIDCHSUBCLASS_VOLTAGERATIOINPUT_BRIDGE"
		if val == self.PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT:
			return "PHIDCHSUBCLASS_VOLTAGERATIOINPUT_SENSOR_PORT"
		return "<invalid enumeration value>"
