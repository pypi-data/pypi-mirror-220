#
# Automatically generated file, do not edit!
#

"""
    ArducamEvkSDK
"""
from __future__ import annotations
import ArducamEvkSDK
import typing

__all__ = [
    "Camera",
    "CameraConfig",
    "Control",
    "Device",
    "EVENT_EXIT",
    "EVENT_FRAME_END",
    "EVENT_FRAME_START",
    "EVENT_NONE",
    "EventCode",
    "Format",
    "Frame",
    "I2CMode",
    "I2C_MODE_16_16",
    "I2C_MODE_16_32",
    "I2C_MODE_16_8",
    "I2C_MODE_8_16",
    "I2C_MODE_8_8",
    "LOG_CRITICAL",
    "LOG_DEBUG",
    "LOG_ERR",
    "LOG_INFO",
    "LOG_OFF",
    "LOG_TRACE",
    "LOG_WARN",
    "LoggerLevel",
    "MEM_TYPE_DMA",
    "MEM_TYPE_RAM",
    "MemType",
    "Param",
    "USBSpeed",
    "USB_SPEED_FULL",
    "USB_SPEED_HIGH",
    "USB_SPEED_LOW",
    "USB_SPEED_SUPER",
    "USB_SPEED_SUPER_PLUS",
    "USB_SPEED_UNKNOWN",
    "list_devices"
]


class Camera():
    def __init__(self) -> None: ...
    def close(self) -> None: 
        """
        close the camera
        """
    def enable_console_log(self, enable: bool = True) -> None: 
        """
        enable/disable console log
        """
    def has_event_callback(self) -> bool: 
        """
        check if the callback function for event is set
        """
    def has_message_callback(self) -> bool: 
        """
        check if the callback function for message is set
        """
    def has_read_callback(self) -> bool: 
        """
        check if the callback function for reading a frame is set
        """
    def init(self) -> bool: 
        """
        init the camera
        """
    def open(self, param: Param) -> int: 
        """
        open the camera
        """
    def read(self, timeout: int = 2000) -> Frame: 
        """
        read a frame
        """
    def read_board_config(self, command: int, value: int, index: int, buf_size: int) -> object: 
        """
        read sensor register
        """
    def read_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int) -> object: 
        """
        read sensor register
        """
    def read_reg_16_16(self, ship_addr: int, reg_addr: int) -> object: 
        """
        Reads a register value with 16 bit address and 16 bit value.
        """
    def read_reg_16_8(self, ship_addr: int, reg_addr: int) -> object: 
        """
        Reads a register value with 16 bit address and 8 bit value.
        """
    def read_reg_8_16(self, ship_addr: int, reg_addr: int) -> object: 
        """
        Reads a register value with 8 bit address and 16 bit value.
        """
    def read_reg_8_8(self, ship_addr: int, reg_addr: int) -> object: 
        """
        Reads a register value with 8 bit address and 8 bit value.
        """
    def read_sensor_reg(self, reg_addr: int) -> object: 
        """
        read sensor register
        """
    def read_user_data(self, addr: int, len: int) -> object: 
        """
        read sensor register
        """
    def register_control(self, controls: typing.List[Control]) -> bool: 
        """
        register controls
        """
    def send_vr(self, command: int, direction: int, value: int, index: int, buffer: typing.List[int]) -> bool: 
        """
        send vendor request
        """
    def set_control(self, controlId: str, value: int) -> bool: 
        """
        set control value
        """
    def set_event_callback(self, callback: typing.Callable[[EventCode], None]) -> None: 
        """
        set the callback function for event, or None to disable it
        """
    def set_message_callback(self, callback: typing.Callable[[LoggerLevel, str], None]) -> None: 
        """
        set the callback function for message, or None to disable it
        """
    def set_read_callback(self, callback: typing.Callable[[Frame], None]) -> None: 
        """
        set the callback function for reading a frame, or None to disable it
        """
    def set_transfer(self, transfer_size: int, transfer_buffer_size: int) -> None: 
        """
        set transfer size and buffer size
        """
    def start(self) -> None: 
        """
        start the camera
        """
    def stop(self) -> None: 
        """
        stop the camera
        """
    def switch_mode(self, mode_id: int) -> bool: 
        """
        switch the camera mode
        """
    def write_board_config(self, command: int, value: int, index: int, buf: typing.List[int]) -> bool: 
        """
        write sensor register
        """
    def write_reg(self, mode: I2CMode, i2c_addr: int, regAddr: int, value: int) -> bool: 
        """
        write sensor register
        """
    def write_reg_16_16(self, ship_addr: int, reg_addr: int, value: int) -> int: 
        """
        Writes a register value with 16 bit address and 16 bit value.
        """
    def write_reg_16_8(self, ship_addr: int, reg_addr: int, value: int) -> int: 
        """
        Writes a register value with 16 bit address and 8 bit value.
        """
    def write_reg_8_16(self, ship_addr: int, reg_addr: int, value: int) -> int: 
        """
        Writes a register value with 8 bit address and 16 bit value.
        """
    def write_reg_8_8(self, ship_addr: int, reg_addr: int, value: int) -> int: 
        """
        Writes a register value with 8 bit address and 8 bit value.
        """
    def write_sensor_reg(self, reg_addr: int, value: int) -> bool: 
        """
        write sensor register
        """
    def write_user_data(self, addr: int, data: typing.List[int]) -> bool: 
        """
        write sensor register
        """
    @property
    def bandwidth(self) -> int:
        """
        A property of bandwidth (read-only).

        :type: int
        """
    @bandwidth.setter
    def bandwidth(self) -> None:
        """
        A property of bandwidth (read-only).
        """
    @property
    def bin_config(self) -> dict:
        """
        A property of bin_config (read-only).

        :type: dict
        """
    @bin_config.setter
    def bin_config(self) -> None:
        """
        A property of bin_config (read-only).
        """
    @property
    def capture_fps(self) -> int:
        """
        A property of capture_fps (read-only).

        :type: int
        """
    @capture_fps.setter
    def capture_fps(self) -> None:
        """
        A property of capture_fps (read-only).
        """
    @property
    def config(self) -> CameraConfig:
        """
        A property of config.

        :type: CameraConfig
        """
    @config.setter
    def config(self, arg1: CameraConfig) -> None:
        """
        A property of config.
        """
    @property
    def config_type(self) -> str:
        """
        A property of config_type (read-only).

        :type: str
        """
    @config_type.setter
    def config_type(self) -> None:
        """
        A property of config_type (read-only).
        """
    @property
    def log_level(self) -> LoggerLevel:
        """
        A property of log_level.

        :type: LoggerLevel
        """
    @log_level.setter
    def log_level(self, arg1: LoggerLevel) -> None:
        """
        A property of log_level.
        """
    @property
    def usb_type(self) -> str:
        """
        A property of usb_type (read-only).

        :type: str
        """
    @usb_type.setter
    def usb_type(self) -> None:
        """
        A property of usb_type (read-only).
        """
    pass
class CameraConfig():
    def __init__(self) -> None: ...
    @property
    def bit_width(self) -> int:
        """
        A property of bit_width.

        :type: int
        """
    @bit_width.setter
    def bit_width(self, arg0: int) -> None:
        """
        A property of bit_width.
        """
    @property
    def format(self) -> int:
        """
        A property of format.

        :type: int
        """
    @format.setter
    def format(self, arg0: int) -> None:
        """
        A property of format.
        """
    @property
    def height(self) -> int:
        """
        A property of height.

        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        """
        A property of height.
        """
    @property
    def i2c_addr(self) -> int:
        """
        A property of i2c_addr.

        :type: int
        """
    @i2c_addr.setter
    def i2c_addr(self, arg0: int) -> None:
        """
        A property of i2c_addr.
        """
    @property
    def i2c_mode(self) -> int:
        """
        A property of i2c_mode.

        :type: int
        """
    @i2c_mode.setter
    def i2c_mode(self, arg0: int) -> None:
        """
        A property of i2c_mode.
        """
    @property
    def width(self) -> int:
        """
        A property of width.

        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        """
        A property of width.
        """
    pass
class Control():
    def __init__(self) -> None: 
        """
        Creates a new control.
        """
    def __repr__(self) -> str: 
        """
        Returns a string representation of the control.
        """
    def __str__(self) -> str: 
        """
        Returns a string representation of the control.
        """
    @property
    def code(self) -> str:
        """
        A property of code.

        :type: str
        """
    @code.setter
    def code(self, arg0: str) -> None:
        """
        A property of code.
        """
    @property
    def default(self) -> int:
        """
        A property of default.

        :type: int
        """
    @default.setter
    def default(self, arg0: int) -> None:
        """
        A property of default.
        """
    @property
    def flags(self) -> int:
        """
        A property of flags.

        :type: int
        """
    @flags.setter
    def flags(self, arg0: int) -> None:
        """
        A property of flags.
        """
    @property
    def func(self) -> str:
        """
        A property of func (read-only).

        :type: str
        """
    @func.setter
    def func(self) -> None:
        """
        A property of func (read-only).
        """
    @property
    def max(self) -> int:
        """
        A property of max.

        :type: int
        """
    @max.setter
    def max(self, arg0: int) -> None:
        """
        A property of max.
        """
    @property
    def min(self) -> int:
        """
        A property of min.

        :type: int
        """
    @min.setter
    def min(self, arg0: int) -> None:
        """
        A property of min.
        """
    @property
    def name(self) -> str:
        """
        A property of name (read-only).

        :type: str
        """
    @name.setter
    def name(self) -> None:
        """
        A property of name (read-only).
        """
    @property
    def step(self) -> int:
        """
        A property of step.

        :type: int
        """
    @step.setter
    def step(self, arg0: int) -> None:
        """
        A property of step.
        """
    pass
class Device():
    @property
    def id_product(self) -> int:
        """
        A property of id_product (const).

        :type: int
        """
    @property
    def id_vendor(self) -> int:
        """
        A property of id_vendor (const).

        :type: int
        """
    @property
    def in_used(self) -> bool:
        """
        A property of in_used (const).

        :type: bool
        """
    @property
    def serial_number(self) -> typing.List[int]:
        """
        A property of serial_number (const).

        :type: typing.List[int]
        """
    @property
    def speed(self) -> USBSpeed:
        """
        A property of speed (const).

        :type: USBSpeed
        """
    @property
    def usb_type(self) -> int:
        """
        A property of usb_type (const).

        :type: int
        """
    pass
class EventCode():
    """
    Members:

      EVENT_NONE : reserved event code

      EVENT_FRAME_START : frame start event code

      EVENT_FRAME_END : frame end event code

      EVENT_EXIT : exit event code
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    EVENT_EXIT: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_EXIT: 3>
    EVENT_FRAME_END: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_FRAME_END: 2>
    EVENT_FRAME_START: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_FRAME_START: 1>
    EVENT_NONE: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_NONE: 0>
    __members__: dict # value = {'EVENT_NONE': <EventCode.EVENT_NONE: 0>, 'EVENT_FRAME_START': <EventCode.EVENT_FRAME_START: 1>, 'EVENT_FRAME_END': <EventCode.EVENT_FRAME_END: 2>, 'EVENT_EXIT': <EventCode.EVENT_EXIT: 3>}
    pass
class Format():
    def __init__(self) -> None: ...
    @property
    def bit_depth(self) -> int:
        """
        A property of bit_depth.

        :type: int
        """
    @bit_depth.setter
    def bit_depth(self, arg0: int) -> None:
        """
        A property of bit_depth.
        """
    @property
    def format_code(self) -> int:
        """
        A property of format_code.

        :type: int
        """
    @format_code.setter
    def format_code(self, arg0: int) -> None:
        """
        A property of format_code.
        """
    @property
    def height(self) -> int:
        """
        A property of height.

        :type: int
        """
    @height.setter
    def height(self, arg0: int) -> None:
        """
        A property of height.
        """
    @property
    def width(self) -> int:
        """
        A property of width.

        :type: int
        """
    @width.setter
    def width(self, arg0: int) -> None:
        """
        A property of width.
        """
    pass
class Frame():
    def __init__(self) -> None: ...
    @property
    def bad(self) -> bool:
        """
        A property of bad.

        :type: bool
        """
    @bad.setter
    def bad(self, arg0: bool) -> None:
        """
        A property of bad.
        """
    @property
    def data(self) -> numpy.ndarray[numpy.uint8]:
        """
        A property of data.

        :type: numpy.ndarray[numpy.uint8]
        """
    @data.setter
    def data(self, arg0: numpy.ndarray[numpy.uint8]) -> None:
        """
        A property of data.
        """
    @property
    def format(self) -> Format:
        """
        A property of format.

        :type: Format
        """
    @format.setter
    def format(self, arg0: Format) -> None:
        """
        A property of format.
        """
    @property
    def seq(self) -> int:
        """
        A property of seq.

        :type: int
        """
    @seq.setter
    def seq(self, arg0: int) -> None:
        """
        A property of seq.
        """
    pass
class I2CMode():
    """
    Members:

      I2C_MODE_8_8 : 8-bit register address and 8-bit data

      I2C_MODE_8_16 : 8-bit register address and 16-bit data

      I2C_MODE_16_8 : 16-bit register address and 8-bit data

      I2C_MODE_16_16 : 16-bit register address and 16-bit data

      I2C_MODE_16_32 : 16-bit register address and 32-bit data
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    I2C_MODE_16_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_16: 3>
    I2C_MODE_16_32: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_32: 4>
    I2C_MODE_16_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_8: 2>
    I2C_MODE_8_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_16: 1>
    I2C_MODE_8_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_8: 0>
    __members__: dict # value = {'I2C_MODE_8_8': <I2CMode.I2C_MODE_8_8: 0>, 'I2C_MODE_8_16': <I2CMode.I2C_MODE_8_16: 1>, 'I2C_MODE_16_8': <I2CMode.I2C_MODE_16_8: 2>, 'I2C_MODE_16_16': <I2CMode.I2C_MODE_16_16: 3>, 'I2C_MODE_16_32': <I2CMode.I2C_MODE_16_32: 4>}
    pass
class LoggerLevel():
    """
    Members:

      LOG_TRACE : trace log level

      LOG_DEBUG : debug log level

      LOG_INFO : info log level

      LOG_WARN : warn log level

      LOG_ERR : err log level

      LOG_CRITICAL : critical log level

      LOG_OFF : off log level
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    LOG_CRITICAL: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_CRITICAL: 5>
    LOG_DEBUG: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_DEBUG: 1>
    LOG_ERR: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_ERR: 4>
    LOG_INFO: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_INFO: 2>
    LOG_OFF: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_OFF: 6>
    LOG_TRACE: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_TRACE: 0>
    LOG_WARN: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_WARN: 3>
    __members__: dict # value = {'LOG_TRACE': <LoggerLevel.LOG_TRACE: 0>, 'LOG_DEBUG': <LoggerLevel.LOG_DEBUG: 1>, 'LOG_INFO': <LoggerLevel.LOG_INFO: 2>, 'LOG_WARN': <LoggerLevel.LOG_WARN: 3>, 'LOG_ERR': <LoggerLevel.LOG_ERR: 4>, 'LOG_CRITICAL': <LoggerLevel.LOG_CRITICAL: 5>, 'LOG_OFF': <LoggerLevel.LOG_OFF: 6>}
    pass
class MemType():
    """
    Members:

      MEM_TYPE_DMA : DMA

      MEM_TYPE_RAM : RAM
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    MEM_TYPE_DMA: ArducamEvkSDK.MemType # value = <MemType.MEM_TYPE_DMA: 1>
    MEM_TYPE_RAM: ArducamEvkSDK.MemType # value = <MemType.MEM_TYPE_RAM: 2>
    __members__: dict # value = {'MEM_TYPE_DMA': <MemType.MEM_TYPE_DMA: 1>, 'MEM_TYPE_RAM': <MemType.MEM_TYPE_RAM: 2>}
    pass
class Param():
    def __init__(self) -> None: 
        """
        construct a default param
        """
    @property
    def bin_config(self) -> bool:
        """
        A property of bin_config.

        :type: bool
        """
    @bin_config.setter
    def bin_config(self, arg0: bool) -> None:
        """
        A property of bin_config.
        """
    @property
    def config_file_name(self) -> str:
        """
        A property of config_file_name.

        :type: str
        """
    @config_file_name.setter
    def config_file_name(self, arg0: str) -> None:
        """
        A property of config_file_name.
        """
    @property
    def device(self) -> Device:
        """
        A property of device.

        :type: Device
        """
    @device.setter
    def device(self, arg0: Device) -> None:
        """
        A property of device.
        """
    @property
    def mem_type(self) -> MemType:
        """
        A property of mem_type.

        :type: MemType
        """
    @mem_type.setter
    def mem_type(self, arg0: MemType) -> None:
        """
        A property of mem_type.
        """
    pass
class USBSpeed():
    """
    Members:

      USB_SPEED_UNKNOWN : The OS doesn't report or know the device speed.

      USB_SPEED_LOW : The device is operating at low speed (1.5MBit/s).

      USB_SPEED_FULL : The device is operating at full speed (12MBit/s).

      USB_SPEED_HIGH : The device is operating at high speed (480MBit/s).

      USB_SPEED_SUPER : The device is operating at super speed (5000MBit/s).

      USB_SPEED_SUPER_PLUS : The device is operating at super speed plus (10000MBit/s).
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    USB_SPEED_FULL: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_FULL: 2>
    USB_SPEED_HIGH: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_HIGH: 3>
    USB_SPEED_LOW: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_LOW: 1>
    USB_SPEED_SUPER: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_SUPER: 4>
    USB_SPEED_SUPER_PLUS: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_SUPER_PLUS: 5>
    USB_SPEED_UNKNOWN: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_UNKNOWN: 0>
    __members__: dict # value = {'USB_SPEED_UNKNOWN': <USBSpeed.USB_SPEED_UNKNOWN: 0>, 'USB_SPEED_LOW': <USBSpeed.USB_SPEED_LOW: 1>, 'USB_SPEED_FULL': <USBSpeed.USB_SPEED_FULL: 2>, 'USB_SPEED_HIGH': <USBSpeed.USB_SPEED_HIGH: 3>, 'USB_SPEED_SUPER': <USBSpeed.USB_SPEED_SUPER: 4>, 'USB_SPEED_SUPER_PLUS': <USBSpeed.USB_SPEED_SUPER_PLUS: 5>}
    pass
def list_devices() -> typing.List[Device]:
    """
    list all supported devices
    """
EVENT_EXIT: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_EXIT: 3>
EVENT_FRAME_END: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_FRAME_END: 2>
EVENT_FRAME_START: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_FRAME_START: 1>
EVENT_NONE: ArducamEvkSDK.EventCode # value = <EventCode.EVENT_NONE: 0>
I2C_MODE_16_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_16: 3>
I2C_MODE_16_32: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_32: 4>
I2C_MODE_16_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_16_8: 2>
I2C_MODE_8_16: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_16: 1>
I2C_MODE_8_8: ArducamEvkSDK.I2CMode # value = <I2CMode.I2C_MODE_8_8: 0>
LOG_CRITICAL: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_CRITICAL: 5>
LOG_DEBUG: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_DEBUG: 1>
LOG_ERR: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_ERR: 4>
LOG_INFO: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_INFO: 2>
LOG_OFF: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_OFF: 6>
LOG_TRACE: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_TRACE: 0>
LOG_WARN: ArducamEvkSDK.LoggerLevel # value = <LoggerLevel.LOG_WARN: 3>
MEM_TYPE_DMA: ArducamEvkSDK.MemType # value = <MemType.MEM_TYPE_DMA: 1>
MEM_TYPE_RAM: ArducamEvkSDK.MemType # value = <MemType.MEM_TYPE_RAM: 2>
USB_SPEED_FULL: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_FULL: 2>
USB_SPEED_HIGH: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_HIGH: 3>
USB_SPEED_LOW: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_LOW: 1>
USB_SPEED_SUPER: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_SUPER: 4>
USB_SPEED_SUPER_PLUS: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_SUPER_PLUS: 5>
USB_SPEED_UNKNOWN: ArducamEvkSDK.USBSpeed # value = <USBSpeed.USB_SPEED_UNKNOWN: 0>
__version__ = 'dev'
