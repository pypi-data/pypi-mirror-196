from __future__ import annotations
from weakref import ref
from asyncio import (
    Transport,
    Protocol
)
from asyncio.coroutines import iscoroutine
from hedra.core.engines.types.common.protocols.shared import FlowControlMixin
from hedra.core.engines.types.common.protocols.shared.reader import Reader
from hedra.core.engines.types.common.protocols.shared.writer import Writer


class TCPProtocol(FlowControlMixin, Protocol):
    """Helper class to adapt between Protocol and StreamReader.
    (This is a helper class instead of making StreamReader itself a
    Protocol subclass, because the StreamReader has other potential
    uses, and to prevent the user of the StreamReader to accidentally
    call inappropriate methods of the protocol.)
    """

    __slots__ = (
        '_source_traceback',
        '_reject_connection',
        '_stream_writer',
        '_transport',
        '_client_connected_cb',
        '_over_ssl',
        '_closed',
        '_stream_reader_wr'
    )

    def __init__(self, stream_reader: Reader, client_connected_cb=None, loop=None):
        super().__init__(loop=loop)
        self._source_traceback = None

        if stream_reader is not None:
            self._stream_reader_wr: Reader = ref(stream_reader)
            self._source_traceback = stream_reader._source_traceback
        else:
            self._stream_reader_wr = None
        if client_connected_cb is not None:
            # This is a stream created by the `create_server()` function.
            # Keep a strong reference to the reader until a connection
            # is established.
            self._strong_reader = stream_reader
        self._reject_connection = False
        self._stream_writer: Writer = None
        self._transport: Transport = None
        self._client_connected_cb = client_connected_cb
        self._over_ssl = False
        self._closed = self._loop.create_future()

    @property
    def _stream_reader(self) -> Reader:
        if self._stream_reader_wr is None:
            return None
        return self._stream_reader_wr()

    def _replace_writer(self, writer: Writer):
        transport = writer.transport
        self._stream_writer = writer
        self._transport = transport
        self._over_ssl = transport.get_extra_info('sslcontext') is not None

    def connection_made(self, transport: Transport):
        if self._reject_connection:
            context = {
                'message': ('An open stream was garbage collected prior to '
                            'establishing network connection; '
                            'call "stream.close()" explicitly.')
            }
            if self._source_traceback:
                context['source_traceback'] = self._source_traceback
            self._loop.call_exception_handler(context)
            transport.abort()
            return
        self._transport = transport
        reader: Reader = self._stream_reader
        if reader is not None:
            reader.set_transport(transport)
        self._over_ssl = transport.get_extra_info('sslcontext') is not None
        if self._client_connected_cb is not None:
            self._stream_writer = Reader(transport, self,
                                               reader,
                                               self._loop)
            res = self._client_connected_cb(reader,
                                            self._stream_writer)
            if iscoroutine(res):
                self._loop.create_task(res)
            self._strong_reader = None

    def connection_lost(self, exc):
        reader: Reader = self._stream_reader
        if reader is not None:
            if exc is None:
                reader.feed_eof()
            else:
                reader.set_exception(exc)
        if not self._closed.done():
            if exc is None:
                self._closed.set_result(None)
            else:
                self._closed.set_exception(exc)
        super().connection_lost(exc)
        self._stream_reader_wr = None
        self._stream_writer = None
        self._transport = None

    def data_received(self, data):
        reader = self._stream_reader
        if reader is not None:
            reader.feed_data(data)

    def eof_received(self):
        reader: Reader = self._stream_reader
        if reader is not None:
            reader.feed_eof()
        if self._over_ssl:
            # Prevent a warning in SSLProtocol.eof_received:
            # "returning true from eof_received()
            # has no effect when using ssl"
            return False
        return True

    def _get_close_waiter(self, stream):
        return self._closed

    def __del__(self):
        # Prevent reports about unhandled exceptions.
        # Better than self._closed._log_traceback = False hack
        try:
            closed = self._closed
        except AttributeError:
            pass  # failed constructor
        else:
            if closed.done() and not closed.cancelled():
                closed.exception()

