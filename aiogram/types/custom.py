import sys
from datetime import datetime, timezone
from typing import Annotated

from pydantic import PlainSerializer

if sys.platform == "win32":  # pragma: no cover

    def _datetime_serializer(value: datetime) -> int:
        pass

else:  # pragma: no cover

    def _datetime_serializer(value: datetime) -> int:
        pass


# Make datetime compatible with Telegram Bot API (unixtime)
DateTime = Annotated[
    datetime,
    PlainSerializer(
        func=_datetime_serializer,
        return_type=int,
        when_used="unless-none",
    ),
]
