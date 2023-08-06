import asyncio
import platform
import ctypes
import typing as t
import copy
import re
from enum import Enum
from dataclasses import dataclass, field

from serial import win32

from aioconnection.utils import ftime


if platform.platform().startswith('Windows-1'):
    import winreg

    def _ports_list():
        ports = []
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DEVICEMAP\SERIALCOMM')
        for i in range(256):
            try:
                ports.append(winreg.EnumValue(key, i)[1])
            except WindowsError:
                break
        return ports

else:
    import serial.tools.list_ports

    def _ports_list():
        return [port.name for port in serial.tools.list_ports.comports()]


def _default_sort_key(str_):
    numbers = re.findall(r'\d+', str_)
    return int(numbers[-1] if numbers else 0)


def serialports_list(sort_key=_default_sort_key):
    ports = _ports_list()
    return sorted(ports, key=_default_sort_key) if sort_key else ports


class SerialError(IOError):
    ...


class OperationError(SerialError):
    def __init__(self, port, operation, description):
        super().__init__(f'{operation} failed ({port}): {description}')


class Timeout(SerialError):
    def __init__(self, port):
        super().__init__(f'Timeout while operation occurred ({port})')


class SettingsError(SerialError, ValueError):
    def __init__(self):
        super().__init__(f'Invalid port setting values')


class ByteSize(Enum):
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8


class Parity(Enum):
    NONE = 0
    ODD = 1
    EVEN = 2
    MARK = 3
    SPACE = 4


class StopBits(Enum):
    ONE = 0
    ONE5 = 1
    TWO = 2


@dataclass
class SerialSettings:
    baudrate: int = 9600
    bytesize: ByteSize = ByteSize.EIGHT
    parity: Parity = Parity.NONE
    stopbits: StopBits = StopBits.ONE
    silence: int = 4
    is_silence_in_bytes: bool = True

    _driver: 'SerialPort' = field(init=False, default=None, repr=False)
    _silence_timeout: float = field(init=False, default=None, repr=False)
    _total_bytesize: int = field(init=False, default=None, repr=False)

    def __post_init__(self):
        self._total_bytesize = 1 + self.bytesize.value + min(self.parity.value, 1)\
                               + min(self.stopbits.value + 1, 2)

        self._silence_timeout = max(self.silence if not self.is_silence_in_bytes else
                                    self.silence * self._total_bytesize / self.baudrate,
                                    0.001)
        if self._driver:
            self._driver.configure()

    @property
    def total_bytesize(self):
        return self._total_bytesize

    @property
    def silence_timeout(self):
        return self._silence_timeout

    def configure(self, **kwargs):
        self_dict = self.__dict__
        for key, value in kwargs.items():
            if self_dict.get(key) and not str.startswith(key, '_'):
                self_dict[key] = value
        self.__post_init__()
        return self

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if not str.startswith(key, '_') and self._total_bytesize:
            self.__post_init__()


# TODO polling interval для времени слипов вместо silence, ?балансер времени от кол-ва портов
class SerialPort:
    QUEUE_SIZE = 4096

    def __init__(self, port: str = '', settings: SerialSettings = None):
        self._port = port
        self._settings = settings or SerialSettings()
        self._handle: t.Optional[win32.HANDLE] = None
        self._overlapped_recv = win32.OVERLAPPED()
        self._overlapped_send = win32.OVERLAPPED()
        self._on_overlapped_recv = 0
        self._on_overlapped_send = 0
        self._in_buffer = ctypes.create_string_buffer(self.QUEUE_SIZE)
        self._send_last_time: float = 0.0

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port: str):
        if port != self._port:
            if self._handle is not None:
                raise SerialError('Can\'t change port, while it\'s open')
            self._port = port

    @property
    def settings(self):
        return self._settings

    @settings.setter
    def settings(self, settings: SerialSettings):
        if settings != self._settings:
            self._settings = copy.copy(settings)
            self._settings._driver = self
            self.configure()

    def is_closing(self):
        return True if self._handle is None else False

    def open(self):
        if self._handle is not None:
            return
        handle = win32.CreateFile('\\\\.\\' + self._port, win32.GENERIC_READ | win32.GENERIC_WRITE,
                                  0, None, win32.OPEN_EXISTING,
                                  win32.FILE_ATTRIBUTE_NORMAL | win32.FILE_FLAG_OVERLAPPED, 0)
        if handle == win32.INVALID_HANDLE_VALUE:
            raise OperationError(self._port, 'CreateFile', ctypes.WinError())

        self._handle = handle
        win32.SetupComm(self._handle, self.QUEUE_SIZE, self.QUEUE_SIZE)
        win32.PurgeComm(self._handle, win32.PURGE_TXCLEAR | win32.PURGE_TXABORT |
                        win32.PURGE_RXCLEAR | win32.PURGE_RXABORT)
        self._on_overlapped_recv = 0
        self._on_overlapped_send = 0
        self._overlapped_recv.hEvent = win32.CreateEvent(None, 0, 0, None)
        self._overlapped_send.hEvent = win32.CreateEvent(None, 0, 0, None)
        self._configure()
        return self

    def configure(self):
        if self._handle is not None:
            self._configure()

    def _configure(self):
        write_timeout_multiplier = self._settings.total_bytesize * 1000 // self.settings.baudrate + 1
        timeouts = win32.COMMTIMEOUTS(ReadIntervalTimeout=int(self._settings.silence_timeout * 1000),
                                      WriteTotalTimeoutMultiplier=write_timeout_multiplier,
                                      WriteTotalTimeoutConstant=100)

        dcb = win32.DCB(DCBlength=28,
                        BaudRate=self.settings.baudrate,
                        fBinary=1,
                        ByteSize=self._settings.bytesize.value,
                        StopBits=self._settings.stopbits.value,
                        fParity=min(self._settings.parity.value, 1),
                        Parity=self._settings.parity.value)

        if not (win32.SetCommTimeouts(self._handle, timeouts) and win32.SetCommState(self._handle, dcb)):
            raise OperationError(self._port, 'SetCommTimeouts | SetCommStat', ctypes.WinError())

    def close(self):
        if self._handle is not None:
            handle = self._handle
            self._handle = None
            win32.CloseHandle(self._overlapped_recv.hEvent)
            win32.CloseHandle(self._overlapped_send.hEvent)
            win32.CloseHandle(handle)

    async def send(self, data, drain=True):
        if not data:
            return 0
        if self._on_overlapped_send:
            await self._drain()
        send_resume_time = self._send_last_time + self.settings.silence_timeout
        while ftime() < send_resume_time:
            await self._sleep(self.settings.silence_timeout)

        self._read_write_file(data)
        self._on_overlapped_send = len(data)
        return await self._drain() if drain else 0

    async def _drain(self):
        len_data = self._on_overlapped_send
        timeout = None
        while win32.WaitForSingleObject(self._overlapped_send.hEvent, 0) != 0:
            timeout = len_data / self.settings.baudrate if timeout is None\
                else self.settings.silence_timeout
            await self._sleep(timeout)
        self._send_last_time = ftime()
        self._on_overlapped_send = 0
        n = self._get_overlapped_result(self._overlapped_send)
        if n != len_data:
            raise Timeout(self._port)
        return n

    async def recv(self, timeout: float = None):
        if not self._on_overlapped_recv:
            self._read_write_file()

        self._on_overlapped_recv = 1
        recv_stop_time = ftime() + timeout if timeout is not None else float('inf')
        # if the buffer overflows WaitForSingleObject will return with 0
        while self._handle and win32.WaitForSingleObject(self._overlapped_recv.hEvent, 0) != 0:
            if ftime() >= recv_stop_time:
                return b''
            await self._sleep(2 * self.settings.silence_timeout)
        self._on_overlapped_recv = 0

        n = self._get_overlapped_result(self._overlapped_recv)
        if n == 0:
            raise Timeout(self._port)
        return self._in_buffer.raw[:n]

    async def _sleep(self, timeout):
        if self._handle is None:
            raise Timeout(self._port)
        await asyncio.sleep(timeout)

    def _read_write_file(self, data=None):
        if data is not None:
            success = win32.WriteFile(self._handle, data, len(data), None, self._overlapped_send)
        else:
            success = win32.ReadFile(self._handle, self._in_buffer, self.QUEUE_SIZE, None, self._overlapped_recv)
        if not (success or win32.GetLastError() in (win32.ERROR_SUCCESS, win32.ERROR_IO_PENDING)):
            raise OperationError(self._port, 'ReadFile' if data is None else 'WriteFile', ctypes.WinError())

    def _get_overlapped_result(self, overlapped):
        n = win32.DWORD()
        if not win32.GetOverlappedResult(self._handle, overlapped, ctypes.byref(n), False):
            raise OperationError(self._port, 'GetOverlappedResult', ctypes.WinError())
        return n.value

    def __repr__(self):
        return f'{self.__class__.__name__}(id={id(self)}), {self._port}, {self.settings},'
