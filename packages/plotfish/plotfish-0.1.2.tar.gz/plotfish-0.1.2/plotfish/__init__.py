__version__ = "0.1.0"

from decimal import Decimal
from datetime import datetime, timezone
import time
from typing import Union, Optional
import os
import logging
import socketio

NumberLike = Union[int, float, Decimal]
TimestampLike = Union[int, float, datetime]

api_key = os.environ.get("PLOTFISH_API_KEY")
riverbed_url = os.environ.get("RIVERBED_URL")

logger = logging.getLogger(__name__)


class PlotfishError(RuntimeError):
    """For Plotfish SDK related exceptions"""


socket = socketio.Client(logger=logger)


def plot(
    label: str,
    value: Optional[NumberLike] = None,
    change: Optional[NumberLike] = None,
    timestamp: Optional[TimestampLike] = None,
) -> None:
    if not socket.connected:
        if api_key is None:
            raise PlotfishError("api_key cannot be null.")

        if riverbed_url is None:
            raise PlotfishError("riverbed_url cannot be null.")

        socket.connect(url=riverbed_url, auth={"apiKey": api_key})

    if change is not None and value is not None:
        raise PlotfishError(
            f"Cannot pass both `value` ({value}) and `change` ({change})!"
        )

    if change is None and value is None:
        raise PlotfishError(f"One of `change` or `value` must be non-null!")

    if isinstance(timestamp, datetime):
        timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
    elif isinstance(timestamp, int):
        timestamp = float(timestamp)
    elif timestamp is None:
        timestamp = time.time()

    socket.emit("recordDatapoints", (label, [[timestamp, value, None]]))
