import abc
import asyncio
from typing import (
    Optional,
    Any,
    Callable,
    Awaitable,
    Iterator,
    Type,
    List,
    Dict,
    Sized,
    Tuple,
    Union,
)
import logging

import HStream.Server.HStreamApi_pb2 as ApiPb

from hstreamdb.types import RecordId
from hstreamdb.utils import encode_payload

__all__ = [
    "PayloadsFull",
    "PayloadTooBig",
    "AppendPayload",
    "PayloadGroup",
    "BufferedProducer",
]

logger = logging.getLogger(__name__)


class Timer:
    def __init__(self, delay, coro):
        self._delay = delay
        self._coro = coro
        self._continue: asyncio.Event = asyncio.Event()
        self._enable: bool = True
        self._task: asyncio.Task = asyncio.create_task(self._loop())

    def start(self):
        self._continue.set()

    def stop(self):
        self._continue.clear()
        self._task.cancel()

    def exit(self):
        self._enable = False

    async def _loop(self):
        while True:
            if not self._enable:
                break
            try:
                await self._continue.wait()
                await asyncio.sleep(self._delay)
                await asyncio.shield(self._coro())
            except asyncio.CancelledError:
                # do nothing
                logger.debug("Timer: receive CancelledError")


class PayloadsFull(Exception):
    pass


class PayloadTooBig(Exception):
    pass


class Payload(abc.ABC, Sized):
    @abc.abstractmethod
    def __len__(self):
        ...


class PayloadGroup:
    def __init__(self, queue, key, maxsize=0, maxtime=0):
        self._payloads: List[Payload] = []
        self._size: int = 0
        self._flushing_payloads: List[Payload] = []
        self._flushing_size: int = 0
        self._flush_done: asyncio.Event = asyncio.Event()

        self._key: Any = key
        self._notify_queue: asyncio.Queue = queue
        self._lock: asyncio.Lock = asyncio.Lock()
        self._maxsize: int = maxsize
        self._timer: Optional[Timer] = (
            Timer(maxtime, self.flush) if maxtime > 0 else None
        )

    async def append(self, payload: Payload):
        if not self._payloads and self._timer:
            # The first payload comes, set timer
            self._timer.start()

        payload_size = len(payload)

        if self._maxsize > 0 and payload_size > self._maxsize:
            raise PayloadTooBig

        # reach maxsize
        if self._upper(payload_size):
            await self.flush()

        await self._append_nowait(payload)

    async def flush(self):
        if self._flushing_payloads:
            # block until last flushing done
            logger.debug("waiting last flush done...")
            await self._flush_done.wait()

        if self._timer:
            self._timer.stop()

        # no current flushing, trigger it
        self._flush_nowait()

    def pop(self):
        return self._flushing_payloads, self._flushing_size

    async def post_flush(self):
        self._flushing_payloads = []
        self._flushing_size = 0
        self._flush_done.set()

    def exit(self):
        if self._timer:
            self._timer.exit()

    def _flush_nowait(self):
        self._flushing_payloads = self._payloads
        self._flushing_size = self._size
        self._payloads = []
        self._size = 0
        self._flush_done.clear()
        self._notify_queue.put_nowait(self._key)

    async def _append_nowait(self, payload: Payload):
        """Put a payload into the payloads without blocking.

        If no free bytes is immediately available, raise PayloadsFull.
        """
        payload_size = len(payload)
        if self._upper(payload_size):
            raise PayloadsFull

        # FIXME: does this lock really needed?
        async with self._lock:
            self._payloads.append(payload)
            self._size += payload_size

    def _upper(self, size):
        """Return True if there are not exceed maxsize bytes.

        Note: if the Payloads was initialized with maxsize=0 (the default),
        then _upper() is never True.
        """
        if self._maxsize <= 0:
            return False
        else:
            return (self._size + size) > self._maxsize


# -----------------------------------------------------------------------------


class AppendPayload(Payload):
    _payload_bin: bytes
    _payload_type: ApiPb.HStreamRecordHeader.Flag

    def __init__(
        self,
        payload: Union[bytes, str, Dict[Any, Any]],
        key: Optional[str] = None,
    ):
        self.payload: Union[bytes, str, Dict[Any, Any]] = payload
        self._payload_bin, self._payload_type = encode_payload(self.payload)
        self.key: Optional[str] = key

    def __len__(self):
        return len(self._payload_bin)


class BufferedProducer:
    StreamKeyId = int
    GroupKeyTy = Tuple[str, StreamKeyId]  # (stream_name, shard_id)

    class AppendCallback(abc.ABC):
        @abc.abstractmethod
        def on_success(
            self,
            stream_name: str,
            payloads: List[AppendPayload],
            stream_keyid: int,
        ):
            ...

        @abc.abstractmethod
        def on_fail(
            self,
            stream_name: str,
            payloads: List[AppendPayload],
            stream_keyid: int,
            e: Exception,
        ):
            ...

    def __init__(
        self,
        flush_coro: Callable[
            [str, List[AppendPayload], int, Optional[str], int],
            Awaitable[Iterator[RecordId]],
        ],
        find_stream_key_id_coro: Callable[
            [str, Optional[str]], Awaitable[StreamKeyId]
        ],
        append_callback: Optional[Type[AppendCallback]] = None,
        size_trigger=0,
        time_trigger=0,
        workers=1,
        retry_count=0,
        retry_max_delay=60,  # seconds
        compresstype=None,
        compresslevel=9,
    ):
        if workers < 1:
            raise ValueError("workers must be no less than 1")
        self._group: Dict[BufferedProducer.GroupKeyTy, PayloadGroup] = {}
        self._size_trigger = size_trigger
        self._time_trigger = time_trigger
        self._retry_count = retry_count
        self._retry_max_delay = retry_max_delay
        self._flush_coro = flush_coro
        self._compresstype = compresstype
        self._compresslevel = compresslevel
        self._find_stream_key_id_coro = find_stream_key_id_coro
        self._append_callback = append_callback
        self._queues = [asyncio.Queue() for _ in range(workers)]
        self._workers = [
            asyncio.create_task(self._loop_queue(self._queues[i]))
            for i in range(workers)
        ]

    async def append(
        self,
        stream_name: str,
        payload: Union[bytes, str, Dict[Any, Any]],
        key: Optional[str] = None,
    ):
        group_key = await self._fetch_group_key(stream_name, key)
        bpayload = AppendPayload(payload, key=key)

        payloads: PayloadGroup
        if group_key not in self._group:
            payloads = PayloadGroup(
                self._find_queue(group_key),
                group_key,
                maxsize=self._size_trigger,
                maxtime=self._time_trigger,
            )
            self._group[group_key] = payloads
        else:
            payloads = self._group[group_key]

        await payloads.append(bpayload)

    async def flush(self, stream_name: str, shard_id: int):
        group_key = self._cons_group_key(stream_name, shard_id)
        await self._flush(group_key)

    async def flush_by_key(self, stream_name: str, key: Optional[str] = None):
        group_key = await self._fetch_group_key(stream_name, key)
        await self._flush(group_key)

    async def flushall(self):
        for _, payloads in self._group.items():
            await payloads.flush()

    async def close(self):
        for _, pg in self._group.items():
            pg.exit()

        await self.flushall()

        for q in self._queues:
            await q.put(None)

    async def wait(self):
        try:
            await asyncio.gather(
                *[pg._timer._task for _, pg in self._group.items() if pg._timer]
            )
        except asyncio.CancelledError:
            pass
        await asyncio.gather(*self._workers)

    async def wait_and_close(self):
        await self.close()
        await self.wait()

    # -------------------------------------------------------------------------

    async def _flush(self, group_key):
        payloads = self._group.get(group_key)
        if not payloads:
            raise ValueError("No such payloads!")
        await payloads.flush()

    async def _loop_queue(self, queue):
        while True:
            group_key = await queue.get()
            if group_key is None:
                break

            payload_group = self._group[group_key]
            stream_name, stream_keyid = self._uncons_group_key(group_key)

            await self._flusing_worker(stream_name, payload_group, stream_keyid)
            queue.task_done()

    async def _flusing_worker(self, stream_name, payload_group, stream_keyid):
        payloads, _size = payload_group.pop()
        logger.debug(
            f"Flushing stream <{stream_name},{stream_keyid}> "
            f"with {len(payloads)} batches..."
        )
        retries = 0
        while True:
            try:
                await self._flush_coro(
                    stream_name,
                    payloads,
                    stream_keyid,
                    compresstype=self._compresstype,
                    compresslevel=self._compresslevel,
                )
                await payload_group.post_flush()
            except Exception as e:  # TODO: should be a specific append exception
                if self._retry_count < 0 or retries < self._retry_count:
                    logger.debug(
                        f"Retrying {retries} with max deley {self._retry_max_delay}s..."
                    )
                    await asyncio.sleep(
                        min(2**retries, self._retry_max_delay)
                        if self._retry_max_delay >= 0
                        else 2**retries
                    )
                    retries += 1
                    continue
                else:
                    if self._append_callback:
                        return self._append_callback.on_fail(
                            stream_name, payloads, stream_keyid, e
                        )
                    else:
                        raise e
            break

        if self._append_callback:
            return self._append_callback.on_success(
                stream_name, payloads, stream_keyid
            )

    def _find_queue(self, group_key):
        return self._queues[abs(hash(group_key)) % len(self._queues)]

    async def _fetch_group_key(self, name, key):
        shard_id = await self._find_stream_key_id_coro(name, key)
        return self._cons_group_key(name, shard_id)

    @staticmethod
    def _cons_group_key(name, shard_id):
        return (name, shard_id)

    @staticmethod
    def _uncons_group_key(group_key):
        return (group_key[0], group_key[1])
