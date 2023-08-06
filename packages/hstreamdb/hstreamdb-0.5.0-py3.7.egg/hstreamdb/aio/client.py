import functools
from typing import Optional, Any, Iterable, Type, Iterator, Dict, List, Tuple
import types
import grpc
import logging
from contextlib import asynccontextmanager
import itertools
from urllib.parse import urlparse

import HStream.Server.HStreamApi_pb2 as ApiPb
import HStream.Server.HStreamApi_pb2_grpc as ApiGrpc
from hstreamdb.aio.producer import BufferedProducer, AppendPayload
from hstreamdb.aio.consumer import Consumer
from hstreamdb.types import (
    RecordId,
    Record,
    record_id_from,
    Stream,
    stream_type_from,
    Subscription,
    subscription_type_from,
    Shard,
    shard_type_from,
    SpecialOffset,
    ShardOffset,
)
from hstreamdb.utils import (
    find_shard_id,
    decode_records,
    encode_records,
    encode_records_from_append_payload,
)

__all__ = ["secure_client", "insecure_client", "HStreamDBClient"]

logger = logging.getLogger(__name__)


def dec_api(f):
    @functools.wraps(f)
    async def wrapper(client, *args, **kargs):
        try:
            return await f(client, *args, **kargs)
        except grpc.aio.AioRpcError as e:
            # The service is currently unavailable, so we choose another
            if e.code() == grpc.StatusCode.UNAVAILABLE:
                await client._switch_channel()
                return await f(client, *args, **kargs)
            else:
                raise e

    return wrapper


class HStreamDBClient:
    _TargetTy = str

    _stub: ApiGrpc.HStreamApiStub
    _channels: Dict[_TargetTy, Optional[grpc.aio.Channel]]

    _current_target: _TargetTy
    # {(stream_name, shard_id)}
    _append_channels: Dict[Tuple[str, int], _TargetTy]
    _subscription_channels: Dict[str, _TargetTy]
    _reader_channels: Dict[str, _TargetTy]
    _shards_info: Dict[str, List[Shard]]

    _cons_target = staticmethod(lambda host, port: f"{host}:{port}")

    def __init__(
        self, host: str = "127.0.0.1", port: int = 6570, credentials=None
    ):
        self._current_target = self._cons_target(host, port)
        self._channels = {}
        self._append_channels = {}
        self._subscription_channels = {}
        self._reader_channels = {}
        self._shards_info = {}
        if credentials:
            _channel = grpc.aio.secure_channel(
                self._current_target, credentials
            )
        else:
            _channel = grpc.aio.insecure_channel(self._current_target)
        self._channels[self._current_target] = _channel
        self._stub = ApiGrpc.HStreamApiStub(_channel)

    async def init_cluster_info(self):
        cluster_info = await self._stub.DescribeCluster(None)
        # TODO: check protocolVersion, serverVersion
        for node in cluster_info.serverNodes:
            target = self._cons_target(node.host, node.port)
            if target not in self._channels:
                self._channels[target] = None

    # -------------------------------------------------------------------------

    @dec_api
    async def create_stream(
        self, name, replication_factor=1, backlog=0, shard_count=1
    ):
        """
        Args:
            name: stream name
            replication_factor: how stream can be replicated across nodes in
                                the cluster
            backlog: how long streams of HStreamDB retain records after being
                     appended, in senconds.
        """
        await self._stub.CreateStream(
            ApiPb.Stream(
                streamName=name,
                replicationFactor=replication_factor,
                backlogDuration=backlog,
                shardCount=shard_count,
            )
        )

    @dec_api
    async def delete_stream(self, name, ignore_non_exist=False, force=False):
        await self._stub.DeleteStream(
            ApiPb.DeleteStreamRequest(
                streamName=name, ignoreNonExist=ignore_non_exist, force=force
            )
        )

    @dec_api
    async def list_streams(self) -> Iterator[Stream]:
        """List all streams"""
        r = await self._stub.ListStreams(ApiPb.ListStreamsRequest())
        return (stream_type_from(s) for s in r.streams)

    async def append(
        self,
        name: str,
        payloads: Iterable[Any],
        key: Optional[str] = None,
        compresstype=None,
        compresslevel=9,
    ) -> Iterator[RecordId]:
        """Append payloads to a stream.

        Args:
            name: stream name
            payloads: a list of string, bytes or dict(json).
            key: Optional stream key.

        Returns:
            Appended RecordIds generator
        """
        shard_id, channel = await self._lookup_append(name, key, None)
        stub = ApiGrpc.HStreamApiStub(channel)
        r = await stub.Append(
            ApiPb.AppendRequest(
                streamName=name,
                shardId=shard_id,
                records=encode_records(
                    payloads,
                    key=key,
                    compresstype=compresstype,
                    compresslevel=compresslevel,
                ),
            )
        )
        return (record_id_from(x) for x in r.recordIds)

    def new_producer(
        self,
        append_callback: Optional[Type[BufferedProducer.AppendCallback]] = None,
        size_trigger=0,  # NOTE: this is the size of uncompressed records
        time_trigger=0,
        workers=1,
        retry_count=0,
        retry_max_delay=60,
        compresstype=None,
        compresslevel=9,
    ):
        return BufferedProducer(
            self._append_with_shard,
            self._find_shard_id,
            append_callback=append_callback,
            size_trigger=size_trigger,
            time_trigger=time_trigger,
            workers=workers,
            retry_count=retry_count,
            retry_max_delay=retry_max_delay,
        )

    @dec_api
    async def list_shards(self, stream_name) -> List[Shard]:
        # FIXME: what if shards_info can be changed?
        shards = self._shards_info.get(stream_name)
        if not shards:
            r = await self._stub.ListShards(
                ApiPb.ListShardsRequest(streamName=stream_name)
            )
            shards = [shard_type_from(s) for s in r.shards]
            self._shards_info[stream_name] = shards

        return shards

    @dec_api
    async def create_subscription(
        self,
        subscription_id: str,
        stream_name: str,
        ack_timeout: int = 600,  # 10min
        max_unacks: int = 10000,
        offset: SpecialOffset = SpecialOffset.LATEST,
    ):
        await self._stub.CreateSubscription(
            ApiPb.Subscription(
                subscriptionId=subscription_id,
                streamName=stream_name,
                ackTimeoutSeconds=ack_timeout,
                maxUnackedRecords=max_unacks,
                offset=offset,
            )
        )

    @dec_api
    async def list_subscriptions(self) -> Iterator[Subscription]:
        r = await self._stub.ListSubscriptions(None)
        return (subscription_type_from(s) for s in r.subscription)

    @dec_api
    async def does_subscription_exist(self, subscription_id: str):
        r = await self._stub.CheckSubscriptionExist(
            ApiPb.CheckSubscriptionExistRequest(subscriptionId=subscription_id)
        )
        return r.exists

    async def delete_subscription(self, subscription_id: str, force=False):
        channel = await self._lookup_subscription(subscription_id)
        stub = ApiGrpc.HStreamApiStub(channel)
        await stub.DeleteSubscription(
            ApiPb.DeleteSubscriptionRequest(
                subscriptionId=subscription_id, force=force
            )
        )

    def new_consumer(self, name: str, subscription_id: str, processing_func):
        async def find_stub():
            channel = await self._lookup_subscription(subscription_id)
            return ApiGrpc.HStreamApiStub(channel)

        return Consumer(
            name,
            subscription_id,
            find_stub,
            processing_func,
        )

    @asynccontextmanager
    async def with_reader(
        self,
        stream_name: str,
        reader_id: str,
        shard_offset: ShardOffset,
        timeout: int,
        shard_id: Optional[int] = None,
        stream_key: Optional[str] = None,
    ):
        await self.create_reader(
            stream_name,
            reader_id,
            shard_offset,
            timeout,
            shard_id=shard_id,
            stream_key=stream_key,
        )
        try:
            obj = types.SimpleNamespace()
            obj.read = lambda max_records: self.read_reader(
                reader_id, max_records
            )
            yield obj
        finally:
            await self.delete_reader(reader_id)

    @dec_api
    async def create_reader(
        self,
        stream_name: str,
        reader_id: str,
        shard_offset: ShardOffset,
        timeout: int,
        shard_id: Optional[int] = None,
        stream_key: Optional[str] = None,
    ):
        """Create a reader.

        If the 'shard_id' is None, then use the shard which the optional
        'stream_key' corresponds.
        """
        if shard_id is None:
            shard_id = await self._find_shard_id(stream_name, key=stream_key)
        return await self._stub.CreateShardReader(
            ApiPb.CreateShardReaderRequest(
                streamName=stream_name,
                shardId=shard_id,
                shardOffset=shard_offset,
                readerId=reader_id,
                timeout=timeout,
            )
        )

    async def read_reader(
        self, reader_id: str, max_records: str
    ) -> Iterator[Record]:
        stub = await self._lookup_reader_stub(reader_id)
        resp = await stub.ReadShard(
            ApiPb.ReadShardRequest(readerId=reader_id, maxRecords=max_records)
        )

        return itertools.chain.from_iterable(
            decode_records(r) for r in resp.receivedRecords
        )

    async def delete_reader(self, reader_id: str) -> None:
        stub = await self._lookup_reader_stub(reader_id)
        await stub.DeleteShardReader(
            ApiPb.DeleteShardReaderRequest(readerId=reader_id)
        )
        return None

    # -------------------------------------------------------------------------

    async def _find_shard_id(self, stream_name, key=None) -> int:
        shards = await self.list_shards(stream_name)
        return find_shard_id(shards, key=key)

    async def _append_with_shard(
        self,
        name: str,
        payloads: List[AppendPayload],
        shard_id: int,
        compresstype=None,
        compresslevel=9,
    ) -> Iterator[RecordId]:
        if not payloads:
            logger.warning("Empty payloads, ignored.")
            return
        shard_id, channel = await self._lookup_append(name, None, shard_id)
        stub = ApiGrpc.HStreamApiStub(channel)
        r = await stub.Append(
            ApiPb.AppendRequest(
                streamName=name,
                shardId=shard_id,
                records=encode_records_from_append_payload(
                    payloads,
                    compresstype=compresstype,
                    compresslevel=compresslevel,
                ),
            )
        )

        return (record_id_from(x) for x in r.recordIds)

    async def _lookup_append(self, name, key, shard_id):
        if shard_id is not None:
            keyid = shard_id
            # NOTE: do not use this 'key', the 'key' param has no means.
            del key
        else:
            keyid = await self._find_shard_id(name, key=key)

        target = self._append_channels.get((name, keyid))
        if not target:
            node = await self._lookup_append_api(keyid)
            target = self._cons_target(node.host, node.port)
            self._append_channels[(name, keyid)] = target

        if not shard_id:
            logger.debug(f"Find target for stream <{name},{key}>: {target}")
        else:
            logger.debug(
                f"Find target for stream <{name}> with shard id <{shard_id}>: {target}"
            )

        return keyid, self._get_channel(target)

    async def _lookup_append_stub(self, name, key, shard_id):
        keyid, channel = self._lookup_append(name, key, shard_id)
        return keyid, ApiGrpc.HStreamApiStub(channel)

    async def _lookup_subscription(self, subscription_id: str):
        target = self._subscription_channels.get(subscription_id)
        if not target:
            node = await self._lookup_subscription_api(subscription_id)
            target = self._cons_target(node.host, node.port)
            self._subscription_channels[subscription_id] = target

        logger.debug(
            f"Find target for subscription <{subscription_id}>: {target}"
        )

        return self._get_channel(target)

    async def _lookup_subscription_stub(self, subscription_id: str):
        channel = self._lookup_subscription(subscription_id)
        return ApiGrpc.HStreamApiStub(channel)

    async def _lookup_reader(self, reader_id: str):
        target = self._reader_channels.get(reader_id)
        if not target:
            node = await self._lookup_reader_api(reader_id)
            target = self._cons_target(node.host, node.port)
            self._reader_channels[reader_id] = target

        logger.debug(f"Find target for reader <{reader_id}>: {target}")

        return self._get_channel(target)

    async def _lookup_reader_stub(self, reader_id: str):
        channel = await self._lookup_reader(reader_id)
        return ApiGrpc.HStreamApiStub(channel)

    @dec_api
    async def _lookup_append_api(self, shard_id):
        r = await self._stub.LookupShard(
            ApiPb.LookupShardRequest(shardId=shard_id)
        )
        # there is no reason that returned value does not equal to requested.
        assert r.shardId == shard_id
        return r.serverNode

    @dec_api
    async def _lookup_subscription_api(self, subscription_id: str):
        r = await self._stub.LookupSubscription(
            ApiPb.LookupSubscriptionRequest(subscriptionId=subscription_id)
        )
        assert r.subscriptionId == subscription_id
        return r.serverNode

    @dec_api
    async def _lookup_reader_api(self, reader_id: str):
        r = await self._stub.LookupShardReader(
            ApiPb.LookupShardReaderRequest(readerId=reader_id)
        )
        assert r.readerId == reader_id
        return r.serverNode

    # -------------------------------------------------------------------------

    async def _switch_channel(self):
        while True:
            logger.warning(
                f"Target {self._current_target} unavailable, switching to another..."
            )
            # remove unavailable target
            self._channels.pop(self._current_target)

            if not self._channels:
                raise RuntimeError("No unavailable targets!")

            # Now, self._channels should not be empty.
            self._current_target = list(self._channels.keys())[0]
            channel = self._get_channel(self._current_target)
            self._stub = ApiGrpc.HStreamApiStub(channel)

            try:
                return await self.init_cluster_info()
            except grpc.aio.AioRpcError as e:
                # The service is currently unavailable, so we choose another
                logger.warning(
                    f"Fetch cluster info from {self._current_target} failed! \n {e}"
                )
                continue

    def _get_channel(self, target):
        channel = self._channels.get(target)
        if channel:
            return channel
        else:
            # new channel
            channel = grpc.aio.insecure_channel(target)
            self._channels[target] = channel
            return channel

    # -------------------------------------------------------------------------

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for target, channel in self._channels.items():
            if channel:
                await channel.close(grace=None)


async def insecure_client(host="127.0.0.1", port=6570, url=None):
    """Creates an insecure client to a cluster.

    Args:
        host: hostname to connect to HStreamDB, defaults to '127.0.0.1'
        port: port to connect to HStreanDB, defaults to 6570
        url: alternative service url to connect to HStreamDB, it should be in
            'hstream://your-host' format. Note that if you provide this url
            then the 'host' and 'port' args will be ignored.

    Returns:
        A :class:`HStreamDBClient`
    """
    if url:
        o = urlparse(url)
        if o.scheme != "hstream":
            raise KeyError(f"Invalid service url scheme {o.scheme}")
        host = o.hostname
        # FIXME: should the default port be the same as secure_client?
        port = o.port or 6570
    client = HStreamDBClient(host=host, port=port)
    await client.init_cluster_info()
    return client


async def secure_client(
    host="127.0.0.1",
    port=6570,
    url=None,
    is_creds_file=False,
    root_certificates=None,
    private_key=None,
    certificate_chain=None,
):
    """Creates a secure client to a cluster.

    Args:
        host: hostname to connect to HStreamDB, defaults to '127.0.0.1'
        port: port to connect to HStreanDB, defaults to 6570
        url: alternative service url to connect to HStreamDB, it should be in
            'hstreams://your-host' format. Note that if you provide this url
            then the 'host' and 'port' args will be ignored.
        is_creds_file: whether the credentials is a filepath or the contents.
        root_certificates: The PEM-encoded root certificates as a byte string,
            or None to retrieve them from a default location chosen by gRPC
            runtime. Note: if 'is_creds_file' is True this is the filepath
            instead of the contents.
        private_key: The PEM-encoded private key as a byte string, or None if no
            private key should be used. Note: if 'is_creds_file' is True this
            is the filepath instead of the contents.
        certificate_chain: The PEM-encoded certificate chain as a byte string
            to use or None if no certificate chain should be used. Note: if
            'is_creds_file' is True this is the filepath instead of the contents.

    Returns:
        A :class:`HStreamDBClient`
    """
    if is_creds_file:
        with open(root_certificates, "rb") as f_cert, open(
            private_key, "rb"
        ) as f_key, open(certificate_chain, "rb") as f_chain:
            root_certificates = f_cert.read()
            private_key = f_key.read()
            certificate_chain = f_chain.read()
    creds = grpc.ssl_channel_credentials(
        root_certificates=root_certificates,
        private_key=private_key,
        certificate_chain=certificate_chain,
    )
    if url:
        o = urlparse(url)
        if o.scheme != "hstreams":
            raise KeyError(f"Invalid service url scheme {o.scheme}")
        host = o.hostname
        port = o.port or 6570
    client = HStreamDBClient(host=host, port=port, credentials=creds)
    await client.init_cluster_info()
    return client
