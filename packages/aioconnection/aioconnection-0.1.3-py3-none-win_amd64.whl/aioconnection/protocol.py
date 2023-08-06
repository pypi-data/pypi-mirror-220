import asyncio
import datetime
import typing as t
from enum import IntEnum, auto
from collections import deque
from dataclasses import dataclass

from notool import Publisher, publisher, enum_str

from aioconnection.utils import ftime


@enum_str
class Ttype(IntEnum):
    UNKNOWN = 1
    TCP = auto()
    SERIAL = auto()

    @classmethod
    def _member2str_map(cls):
        return {cls.UNKNOWN: 'Unknown', cls.TCP: 'TCP', cls.SERIAL: 'Serial'}


# TODO add alias
@dataclass
class TransportInfo:
    type: Ttype
    source: tuple[str, int] = None
    dest: t.Union[tuple[str, int], str] = None
    exception: t.Any = None

    @classmethod
    def make(cls, transport, exc=None):
        dest = source = None
        type_ = Ttype.UNKNOWN
        if source := transport.get_extra_info('serialname'):
            type_ = Ttype.SERIAL
        elif source := transport.get_extra_info('sockname'):
            type_ = Ttype.TCP
            dest = transport.get_extra_info('peername')
        return cls(type_, source, dest, exc)

    def __str__(self):
        source = f'{self.source}' if self.source else ''
        dest = ''
        exc = f', {self.exception}' if self.exception else ''
        if self.type is Ttype.TCP:
            source = f'source {self.source[0]}:{self.source[1]}' if self.source else ''
            dest = f', dest {self.dest[0]}:{self.dest[1]}' if self.dest else ''
        return f'{self.type} ({source}{dest}){exc}'


# TODO event with partial not parsed data
@enum_str
class Etype(IntEnum):
    CONNECTED = 1
    CONNECT_FAILED = auto()
    SEND = auto()
    RECV = auto()
    REPLY_EXPIRED = auto()
    IDLE = auto()

    @classmethod
    def _member2str_map(cls):
        return {cls.CONNECTED: 'Connected', cls.CONNECT_FAILED: 'Connect Failed',
                cls.SEND: 'Send', cls.RECV: 'Receive', cls.REPLY_EXPIRED: 'Reply Timeout',
                cls.IDLE: 'Idle'}


# TODO metadata like auth user
@dataclass
class Event:
    time: t.Union[float, datetime.datetime]
    type: Etype
    bytes: bytes
    data: t.Union[TransportInfo, t.Any] = None

    @property
    def write_id(self):
        return getattr(self, '_id', 0)

    @write_id.setter
    def write_id(self, value):
        setattr(self, '_id', value)

    def reply_accepted(self):
        if _reply_accepted := getattr(self, '_reply_accepted', None):
            _reply_accepted()


class _TailSentinel:
    def __bool__(self):
        return False


TAIL_SENTINEL = _TailSentinel()


class Parser:
    def process(self, *data: t.Any, event_type: Etype = Etype.RECV) \
            -> t.Generator[tuple[t.Union[bytes, bytearray], t.Any], None, None]:
        for data_ in data:
            yield from self._process(data_, event_type)

    def _process(self, data: t.Any, event_type: Etype) -> tuple[t.Union[bytes, bytearray], t.Any]:
        yield b'', None


class StrParser(Parser):
    def __init__(self, codec: str = 'charmap'):
        self.codec = codec

    def _process(self, data: t.Any, event_type: Etype):
        raw, parsed = b'', None
        try:
            if isinstance(data, bytes):
                raw = data
                parsed = data.decode(self.codec)
            elif isinstance(data, str):
                parsed = data
                raw = data.encode(self.codec)
            else:
                raise TypeError(f'Accepted data type must be in {str, bytes}')
        except ValueError:
            ...
        yield raw, parsed


class RawParser(Parser):
    def _process(self, data: t.Any, event_type: Etype):
        if isinstance(data, bytes):
            return data, None
        else:
            raise TypeError(f'Accepted data type must be {bytes}')


# TODO debug set in logger level
# TODO parser, timeouts cls or self attrs??
# TODO _in_buffer to bytearray + limit maximum length by cutting head (do it in Parser)?
class Protocol(asyncio.Protocol, Publisher):
    DEBUG = False
    parser_factory = StrParser
    event_factory = Event

    def __init__(self, *,
                 event_factory: t.Callable = None,
                 event_ftime: t.Callable = None,
                 parser=None,
                 reply_timeout: float = 0.0,
                 idle_timeout: float = 0.0,
                 log_size: int = 0,
                 loop=None,
                 subscribers: t.Union[t.Callable, t.Iterable[t.Callable]] = None,
                 init_callback: t.Callable = None,
                 **kwargs):
        Publisher.__init__(self)
        if subscribers:
            self.subscribe(subscribers)

        self.event_factory = event_factory or self.event_factory
        self.event_ftime = event_ftime or datetime.datetime.now
        self.parser = parser or self.parser_factory()
        self.log: t.Optional[deque[Event]] = deque(maxlen=log_size) if log_size else None
        self.transport: t.Optional[asyncio.Transport] = None
        self.transport_info: t.Optional[TransportInfo] = None
        self.reply_timeout = reply_timeout
        # TODO write id to class
        self._write_id = 0
        self._next_write_id = 0
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._in_buffer: bytes = b''
        self._out_buffer: deque[tuple[list, float]] = deque()
        self._allowed_to_write = False
        self._reply_awaiting = False
        # TODO maybe create cancelled task and handle
        self._reply_handle: t.Optional[asyncio.Handle] = None
        self._recv_last_time = 0.0
        self._idle_timeout = idle_timeout
        self._ping_task: t.Optional[asyncio.Task] = None
        self.__post_init__(**kwargs)
        if init_callback:
            init_callback(self)

    def __post_init__(self, **kwargs):
        ...

    @property
    def idle_timeout(self):
        return self._idle_timeout

    @idle_timeout.setter
    def idle_timeout(self, timeout):
        self._idle_timeout = timeout
        if self._ping_task and not self._ping_task.done():
            self._ping_task.cancel()
        if timeout:
            self._ping_task = self._loop.create_task(self._pinging())

    async def _pinging(self):
        while True:
            await asyncio.sleep(self._idle_timeout)
            time_diff = ftime() - self._recv_last_time
            if time_diff >= self._idle_timeout and not (self._out_buffer or self._reply_handle):
                self._register_event(Etype.IDLE)

    def connection_made(self, transport: asyncio.Transport):
        self.transport = transport
        if self._idle_timeout:
            self._ping_task = self._loop.create_task(self._pinging())
        self._allowed_to_write = True
        self._write()
        self.transport_info = TransportInfo.make(transport)
        if self.transport_info.type == Ttype.TCP:
            transport.set_write_buffer_limits(0, 0)
        self._register_event(Etype.CONNECTED, data=self.transport_info)

    def connection_failed(self, exc=None, transport: asyncio.Transport = None):
        self.transport = transport or self.transport
        self._allowed_to_write = False
        self._ping_task and self._ping_task.cancel()
        self._reply_expired(False)
        self.transport_info = TransportInfo.make(self.transport, exc)
        self._register_event(Etype.CONNECT_FAILED, data=self.transport_info)

    def connection_lost(self, exc):
        self.connection_failed(exc)

    def data_received(self, data_raw: bytes, force: bool = False):
        if self._allowed_to_write or force:
            self._recv_last_time = ftime()
            time_ = self.event_ftime()
            event_type = Etype.RECV
            data_raw = self._in_buffer + data_raw if self._in_buffer else data_raw
            bytes_data = list(self.parser.process(data_raw))
            self._in_buffer = b''
            is_reply = bool(self._reply_handle)
            for bytes_, data in bytes_data:
                if data is TAIL_SENTINEL:
                    self._in_buffer = bytes_
                    continue
                self._register_event(event_type, bytes_, data, time_,
                                     set_id=is_reply, set_reply=is_reply)
        else:
            self._loop.call_soon(self.data_received, data_raw, True)

    def _reply_expired(self, accepted=True):
        if self._reply_handle:
            self._reply_handle.cancel()
            self._reply_handle = None
            if not accepted:
                self._register_event(Etype.REPLY_EXPIRED, set_id=True)
            self._write()

    def resume_writing(self):
        self._data_drained()

    def pause_writing(self):
        self._allowed_to_write = False

    def write(self, *data: t.Union[bytes, str, object], reply_timeout: t.Optional[float] = 0.0):
        bytes_data = list(self.parser.process(*data, event_type=Etype.SEND))
        reply_timeout = 0.0 if reply_timeout is None else self.reply_timeout + reply_timeout
        self._out_buffer.append((bytes_data, reply_timeout))
        self._write()
        self._next_write_id += 1
        return self._next_write_id

    def _write(self):
        if self._allowed_to_write and self._out_buffer and not self._reply_handle:
            bytes_data = self._out_buffer[0][0]
            try:
                self.transport.write(b''.join(bytes_ for bytes_, data in bytes_data))
            except RuntimeError:
                pass

    def _data_drained(self):
        time_ = self.event_ftime()
        self._allowed_to_write = True
        bytes_data, reply_timeout = self._out_buffer.popleft()
        if reply_timeout:
            self._reply_handle = self._loop.call_later(reply_timeout, self._reply_expired, False)
        else:
            self._write()
        self._write_id += 1
        for bytes_, data in bytes_data:
            self._register_event(Etype.SEND, bytes_, data, time_, set_id=True)

    def _register_event(self, type_, bytes_=b'', data=None, time_=None, *,
                        set_id=False, set_reply=False):
        event = self.event_factory(time_ or self.event_ftime(), type_, bytes_, data)
        if set_id:
            event.write_id = self._write_id
        if set_reply:
            setattr(event, '_reply_accepted', self._reply_expired)
        if self.DEBUG:
            print(event)
        if self.log is not None and type_ not in (Etype.IDLE, Etype.REPLY_EXPIRED):
            self.log.append(event)

        # self._loop.call_soon(self.event_handler, event)
        self.event_handler(event)
        self.publish(event, loop=self._loop)

    def event_handler(self, event: Event):
        ...


if __name__ == '__main__':
    ...
