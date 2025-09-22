"""Lightweight telemetry heartbeat exporter used during Phase 0.

The exporter provides an in-memory sink that other modules can depend on while CI and
observability pipelines are being established. It supports thread-safe emission of heartbeat
events and exposes helpers to query the latest status for a subsystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from time import time
from typing import Callable, Dict, List, Mapping, Optional


@dataclass(frozen=True)
class HeartbeatEvent:
    """Represents a single heartbeat sample."""

    subsystem: str
    status: str
    timestamp: float
    metadata: Mapping[str, str] = field(default_factory=dict)


class TelemetryExporter:
    """Collects and forwards heartbeat events."""

    def __init__(
        self,
        sink: Optional[Callable[[HeartbeatEvent], None]] = None,
        *,
        clock: Callable[[], float] = time,
    ) -> None:
        self._sink = sink
        self._clock = clock
        self._events: List[HeartbeatEvent] = []
        self._lock = Lock()

    def emit_heartbeat(self, subsystem: str, status: str = "ok", **metadata: str) -> HeartbeatEvent:
        """Record a heartbeat for ``subsystem``.

        Args:
            subsystem: Name of the emitting subsystem.
            status: Optional status string, ``"ok"`` by default.
            **metadata: Additional key/value metadata to associate with the heartbeat.

        Returns:
            The :class:`HeartbeatEvent` that was emitted.
        """

        event = HeartbeatEvent(
            subsystem=subsystem,
            status=status,
            timestamp=float(self._clock()),
            metadata=dict(metadata),
        )

        with self._lock:
            self._events.append(event)

        if self._sink is not None:
            self._sink(event)

        return event

    def latest(self, subsystem: Optional[str] = None) -> Optional[HeartbeatEvent]:
        """Return the most recent heartbeat.

        Args:
            subsystem: Optional subsystem filter. If provided, only heartbeats matching the
                subsystem are considered.
        """

        with self._lock:
            if subsystem is None:
                return self._events[-1] if self._events else None

            for event in reversed(self._events):
                if event.subsystem == subsystem:
                    return event

        return None

    def export_snapshot(self) -> List[HeartbeatEvent]:
        """Return a copy of all recorded heartbeats."""

        with self._lock:
            return list(self._events)

    def aggregate_status(self) -> Dict[str, str]:
        """Compute the latest status per subsystem."""

        aggregate: Dict[str, str] = {}
        with self._lock:
            for event in self._events:
                aggregate[event.subsystem] = event.status
        return aggregate
