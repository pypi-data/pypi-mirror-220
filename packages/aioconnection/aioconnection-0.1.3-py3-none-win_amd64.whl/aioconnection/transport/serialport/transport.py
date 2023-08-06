import typing as t
import asyncio

from aioconnection.protocol import Protocol
from aioconnection.utils import ftime
from .core import SerialPort, SerialSettings, SerialError


# TODO alies и запись в библиотеку список сконфигурированных портов приложения
# TODO port property в peer или destination, и в экстра не нужно будет peername и portname
# TODO Информацию из экстра типа socket в driver или interface или lowlevel
class SerialTransport(asyncio.Transport):
    def __init__(self,
                 protocol: Protocol,
                 port: str = '',
                 settings: SerialSettings = None,
                 *,
                 to_open: bool = True,
                 reconnect_timeout: float = 1,
                 loop=None):

        super().__init__()
        self._protocol = protocol
        self._port = port
        self._driver: SerialPort = SerialPort(port=port, settings=settings)
        self._is_active = to_open
        self._reconnect_timeout = max(reconnect_timeout, 0.5)
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._extra = {'serial': self._driver, 'serialname': self._port}
        self._connection_failed_time = 0.0
        self._is_closing = True
        self._recv_task: t.Optional[asyncio.Task] = None
        self._send_task: t.Optional[asyncio.Task] = None
        self._open_task: t.Optional[asyncio.Task] = None
        self._close_task: t.Optional[asyncio.Task] = None

        if port and to_open:
            self.open()

    def set_protocol(self, protocol: Protocol):
        self._protocol = protocol

    def get_protocol(self):
        return self._protocol

    def is_reading(self):
        return self._is_task_running(self._recv_task)

    def pause_reading(self):
        raise NotImplementedError

    def resume_reading(self):
        raise NotImplementedError

    @property
    def settings(self):
        return self._driver.settings

    @settings.setter
    def settings(self, settings: SerialSettings):
        self._driver.settings = settings

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, port: str):
        if port != self._port:
            self._port = port
            self._loop.create_task(self._change_port())

    @staticmethod
    async def _task_done(task):
        if bool(task) and not task.done():
            await task

    @staticmethod
    def _is_task_running(task):
        return bool(task) and not task.done()

    async def _change_port(self):
        is_active = self._is_active
        self._is_active = False
        await self._task_done(self._open_task)
        self._close()
        await self._task_done(self._close_task)
        self._driver.port = self._port
        self._extra['serialname'] = self._port
        if is_active:
            self.open()

    def write(self, data):
        if self._is_closing or self._is_task_running(self._send_task):
            raise RuntimeError()
        self._send_task = self._loop.create_task(self._sending(data))
        self._protocol.pause_writing()

    def open(self):
        self._is_active = True
        self._open()

    def _open(self):
        if not self._is_task_running(self._open_task) and self._is_closing and self._port:
            # TODO make cancelled task stub in __init__ for all tasks
            self._send_task =  self._open_task = self._loop.create_task(self._opening())

    def is_active(self):
        return self._is_active

    def is_closing(self):
        return self._is_closing

    def close(self):
        self._is_active = False
        self._close()

    def _close(self, exc=None):
        if not self._is_closing:
            self._close_task = self._loop.create_task(self._closing())
            self._connection_failed(exc)

    def _connection_failed(self, exc):
        self._is_closing = True
        if exc:
            self._connection_failed_time = ftime()
            if self._is_active:
                self._loop.call_soon(self._open)
        self._loop.call_soon(self._protocol.connection_failed, exc, self)

    async def _opening(self):
        if self._close_task and not self._close_task.done():
            await self._close_task
        while ftime() - self._connection_failed_time < self._reconnect_timeout:
            if not self._is_active:
                return
            await asyncio.sleep(0.2)

        try:
            await self._loop.run_in_executor(None, self._driver.open)
        except SerialError as exc:
            self._connection_failed(exc)
        else:
            self._is_closing = False
            self._loop.call_soon(self._protocol.connection_made, self)
            self._recv_task = self._loop.create_task(self._receiving())

    async def _closing(self):
        if self._open_task and not self._open_task.done():
            await self._open_task
        await asyncio.gather(self._loop.run_in_executor(None, self._driver.close),
                             self._send_task, self._recv_task)

    async def _receiving(self):
        while True:
            try:
                data = await self._driver.recv()
            except SerialError as exc:
                self._close(exc)
                break
            else:
                if not self._is_closing:
                    self._loop.call_soon(self._protocol.data_received, data)

    async def _sending(self, data):
        try:
            await self._driver.send(data)
        except SerialError as exc:
            self._close(exc)
        else:
            if not self._is_closing:
                self._loop.call_soon(self._protocol.resume_writing)
