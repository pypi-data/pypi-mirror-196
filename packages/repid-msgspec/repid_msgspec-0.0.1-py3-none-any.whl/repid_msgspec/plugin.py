import sys
from copy import deepcopy
from datetime import datetime, timedelta
from typing import Any, ClassVar, Type, Union
from uuid import uuid4

from msgspec import Meta, Struct, field, json
from repid.data import PrioritiesT
from repid.data.protocols import (
    DelayPropertiesT,
    ResultPropertiesT,
    RetriesPropertiesT,
)
from repid.utils import VALID_ID, VALID_NAME

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

try:
    from croniter import croniter

    CRON_SUPPORT = True
except ImportError:  # pragma: no cover
    CRON_SUPPORT = False


def enc_hook(obj: Any) -> Any:
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    raise TypeError(f"Objects of type {type(obj)} are not supported")


def dec_hook(type: Type, obj: Any) -> Any:  # noqa: A002
    if type is timedelta:
        return timedelta(seconds=obj)
    raise TypeError(f"Objects of type {type} are not supported")


class RoutingKey(Struct, array_like=True, omit_defaults=True, frozen=True):
    topic: Annotated[str, Meta(pattern=str(VALID_NAME))]
    queue: Annotated[str, Meta(pattern=str(VALID_NAME))] = "default"
    priority: Annotated[int, Meta(ge=1)] = PrioritiesT.MEDIUM.value
    id_: Annotated[str, Meta(pattern=str(VALID_ID))] = field(default_factory=lambda: uuid4().hex)


class ArgsBucket(Struct, array_like=True, omit_defaults=True, frozen=True):
    data: str

    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Union[timedelta, None] = None

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "ArgsBucket":
        return args_bucket_decoder.decode(data.encode())

    @property
    def is_overdue(self) -> bool:
        if self.ttl is None:
            return False
        return datetime.now(tz=self.timestamp.tzinfo) > self.timestamp + self.ttl


class ResultBucket(Struct, array_like=True, omit_defaults=True, frozen=True):
    data: str

    # perf_counter_ns
    started_when: int
    finished_when: int

    success: bool = True
    exception: Union[str, None] = None

    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Union[timedelta, None] = None

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "ResultBucket":
        return result_bucket_decoder.decode(data.encode())

    @property
    def is_overdue(self) -> bool:
        if self.ttl is None:
            return False
        return datetime.now(tz=self.timestamp.tzinfo) > self.timestamp + self.ttl


class RetriesProperties(Struct, array_like=True, omit_defaults=True, frozen=True):
    max_amount: int = 0
    already_tried: int = 0

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "RetriesProperties":
        return retries_decoder.decode(data.encode())


class ResultProperties(Struct, array_like=True, omit_defaults=True, frozen=True):
    id_: str = field(default_factory=lambda: uuid4().hex)
    ttl: Union[timedelta, None] = None

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "ResultProperties":
        return result_decoder.decode(data.encode())


class DelayProperties(Struct, array_like=True, omit_defaults=True, frozen=True):
    delay_until: Union[datetime, None] = None
    defer_by: Union[timedelta, None] = None
    cron: Union[str, None] = None
    next_execution_time: Union[datetime, None] = None

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "DelayProperties":
        return delay_decoder.decode(data.encode())


class Parameters(Struct, array_like=True, omit_defaults=True, frozen=True):
    RETRIES_CLASS: ClassVar[Type[RetriesPropertiesT]] = RetriesProperties
    RESULT_CLASS: ClassVar[Type[ResultPropertiesT]] = ResultProperties
    DELAY_CLASS: ClassVar[Type[DelayPropertiesT]] = DelayProperties

    execution_timeout: timedelta = field(default_factory=lambda: timedelta(minutes=10))
    result: Union[ResultProperties, None] = None
    retries: RetriesProperties = field(default_factory=RetriesProperties)
    delay: DelayProperties = field(default_factory=DelayProperties)
    timestamp: datetime = field(default_factory=datetime.now)
    ttl: Union[timedelta, None] = None

    def encode(self) -> str:
        return encoder.encode(self).decode("cp1252")

    @classmethod
    def decode(cls, data: str) -> "Parameters":
        return parameters_decoder.decode(data.encode())

    @property
    def is_overdue(self) -> bool:
        if self.ttl is None:
            return False
        return datetime.now(tz=self.timestamp.tzinfo) > self.timestamp + self.ttl

    @property
    def compute_next_execution_time(self) -> Union[datetime, None]:
        now = datetime.now()
        if self.delay.delay_until is not None and self.delay.delay_until > now:
            return self.delay.delay_until
        if self.delay.defer_by is not None:
            defer_by_times = (now - self.timestamp) // self.delay.defer_by + 1
            time_offset = self.delay.defer_by * defer_by_times
            return self.timestamp + time_offset
        if self.delay.cron is not None:
            if not CRON_SUPPORT:
                raise ImportError("Croniter is not installed.")  # pragma: no cover
            return croniter(self.delay.cron, now).get_next(ret_type=datetime)  # type: ignore[no-any-return]
        return None

    def _prepare_reschedule(self) -> "Parameters":
        copy = deepcopy(self)
        object.__setattr__(copy.retries, "already_tried", 0)
        object.__setattr__(copy.delay, "next_execution_time", self.compute_next_execution_time)
        object.__setattr__(copy, "timestamp", datetime.now())
        return copy

    def _prepare_retry(self, next_retry: timedelta) -> "Parameters":
        copy = deepcopy(self)
        object.__setattr__(copy.retries, "already_tried", copy.retries.already_tried + 1)
        object.__setattr__(
            copy.delay,
            "next_execution_time",
            datetime.now() + next_retry,
        )
        return copy


encoder = json.Encoder(enc_hook=enc_hook)
args_bucket_decoder = json.Decoder(ArgsBucket, dec_hook=dec_hook)
result_bucket_decoder = json.Decoder(ResultBucket, dec_hook=dec_hook)
retries_decoder = json.Decoder(RetriesProperties, dec_hook=dec_hook)
result_decoder = json.Decoder(ResultProperties, dec_hook=dec_hook)
delay_decoder = json.Decoder(DelayProperties, dec_hook=dec_hook)
parameters_decoder = json.Decoder(Parameters, dec_hook=dec_hook)
