import asyncio
import contextlib
import dataclasses
import enum
import logging
import sys
from typing import Any, Callable, Coroutine, Dict, Optional, Union

import aiopg

if sys.version_info < (3, 11, 0):
    from async_timeout import timeout
else:
    from asyncio import timeout  # type: ignore


logger = logging.getLogger(__package__)


class ListenPolicy(str, enum.Enum):
    ALL = "ALL"
    LAST = "LAST"

    def __str__(self) -> str:
        return self.value


@dataclasses.dataclass(frozen=True)
class Timeout:
    __slots__ = ("channel",)

    channel: str


@dataclasses.dataclass(frozen=True)
class Notification:
    __slots__ = ("channel", "payload")

    channel: str
    payload: Optional[str]


ConnectFunc = Callable[[], Coroutine[Any, Any, aiopg.Connection]]
NotificationOrTimeout = Union[Notification, Timeout]
NotificationHandler = Callable[[NotificationOrTimeout], Coroutine]

NO_TIMEOUT: float = -1
NO_TIMEOUT_CTX = contextlib.nullcontext()


def connect_func(*args: Any, **kwargs: Any) -> ConnectFunc:
    async def _connect() -> aiopg.Connection:
        return await aiopg.connect(*args, **kwargs)

    return _connect


class NotificationListener:
    __slots__ = ("_connect", "_reconnect_delay")

    def __init__(self, connect: ConnectFunc, reconnect_delay: float = 5) -> None:
        self._reconnect_delay = reconnect_delay
        self._connect = connect

    async def run(
        self,
        handler_per_channel: Dict[str, NotificationHandler],
        *,
        policy: ListenPolicy = ListenPolicy.ALL,
        notification_timeout: float = 30,
    ) -> None:
        queue_per_channel = {channel: _create_notifications_queue() for channel in handler_per_channel.keys()}

        read_notifications_task = asyncio.create_task(
            self._read_notifications(queue_per_channel=queue_per_channel), name=__package__
        )
        process_notifications_tasks = [
            asyncio.create_task(
                self._process_notifications(
                    channel,
                    notifications=queue_per_channel[channel],
                    handler=handler,
                    policy=policy,
                    notification_timeout=notification_timeout,
                ),
                name=f"{__package__}.{channel}",
            )
            for channel, handler in handler_per_channel.items()
        ]
        try:
            await asyncio.gather(read_notifications_task, *process_notifications_tasks)
        finally:
            read_notifications_task.cancel()
            for process_notifications_task in process_notifications_tasks:
                process_notifications_task.cancel()

    @staticmethod
    async def _process_notifications(
        channel: str,
        *,
        notifications: "asyncio.Queue[Notification]",
        handler: NotificationHandler,
        policy: ListenPolicy,
        notification_timeout: float,
    ) -> None:
        while True:
            notification: NotificationOrTimeout

            if notifications.empty():
                if notification_timeout == NO_TIMEOUT:
                    notification = await notifications.get()
                else:
                    try:
                        async with timeout(notification_timeout):
                            notification = await notifications.get()
                    except asyncio.TimeoutError:
                        notification = Timeout(channel)
            else:
                while not notifications.empty():
                    notification = notifications.get_nowait()
                    if policy == ListenPolicy.ALL:
                        break

            # to have independent async context per run
            # to protect from misuse of contextvars
            try:
                await asyncio.create_task(handler(notification), name=f"{__package__}.{channel}")
            except Exception:
                logger.exception("Failed to handle %s", notification)

    async def _read_notifications(self, queue_per_channel: Dict[str, "asyncio.Queue[Notification]"]) -> None:
        failed_connect_attempts = 0
        while True:
            try:
                connection = await self._connect()
                try:
                    async with connection.cursor() as cursor:
                        for channel in queue_per_channel.keys():
                            await cursor.execute(f"LISTEN {channel}")

                    failed_connect_attempts = 0
                    while True:
                        notify = await connection.notifies.get()
                        queue = queue_per_channel.get(notify.channel)
                        if queue is None:
                            logger.warning("Queue is not found for channel %s", notify.channel)
                            continue

                        await queue.put(Notification(notify.channel, notify.payload))
                finally:
                    await asyncio.shield(connection.close())
            except Exception:
                logger.exception("Connection was lost or not established")

                await asyncio.sleep(self._reconnect_delay * failed_connect_attempts)
                failed_connect_attempts += 1


def _create_notifications_queue() -> "asyncio.Queue[Notification]":
    if sys.version_info >= (3, 9, 0):
        return asyncio.Queue[Notification]()
    return asyncio.Queue()
