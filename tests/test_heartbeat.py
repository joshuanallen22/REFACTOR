from __future__ import annotations

from refactor.telemetry import TelemetryExporter


def test_emit_heartbeat_records_event() -> None:
    exporter = TelemetryExporter(clock=lambda: 123.0)
    event = exporter.emit_heartbeat("retrieval", status="ok", endpoint="primary")

    assert event.subsystem == "retrieval"
    assert event.status == "ok"
    assert event.timestamp == 123.0
    assert event.metadata == {"endpoint": "primary"}


def test_latest_filters_by_subsystem() -> None:
    exporter = TelemetryExporter(clock=lambda: 1.0)
    exporter.emit_heartbeat("retrieval", status="ok")
    exporter.emit_heartbeat("safety", status="degraded")

    latest = exporter.latest("retrieval")
    assert latest is not None
    assert latest.subsystem == "retrieval"
    assert exporter.latest("unknown") is None


def test_export_snapshot_returns_copy() -> None:
    exporter = TelemetryExporter(clock=lambda: 1.0)
    exporter.emit_heartbeat("retrieval")
    snapshot = exporter.export_snapshot()

    snapshot.clear()
    assert exporter.export_snapshot()  # original data remains


def test_aggregate_status_reflects_latest_per_subsystem() -> None:
    exporter = TelemetryExporter(clock=lambda: 1.0)
    exporter.emit_heartbeat("retrieval", status="ok")
    exporter.emit_heartbeat("retrieval", status="degraded")
    exporter.emit_heartbeat("safety", status="ok")

    assert exporter.aggregate_status() == {"retrieval": "degraded", "safety": "ok"}
