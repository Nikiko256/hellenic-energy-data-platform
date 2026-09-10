from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from hellenic_energy.parsing.entsoe_xml import parse_load_xml

FIXTURES = Path(__file__).parents[1] / "fixtures" / "entsoe"

PARSER_METADATA = {
    "area_code": "10YGR-HTSO-----Y",
    "source_request_id": "request-1",
    "source_payload_sha256": "abc123",
    "ingested_at_utc": datetime(2025, 1, 2, tzinfo=UTC),
}


def test_parses_hourly_load_intervals() -> None:
    xml_text = (FIXTURES / "load_hourly.xml").read_text()

    records = parse_load_xml(xml_text, **PARSER_METADATA)

    assert len(records) == 2
    assert records[0]["duration_minutes"] == 60
    assert records[0]["load_mw"] == 5000.0
    assert records[0]["interval_start_utc"].hour == 0
    assert records[1]["interval_start_utc"].hour == 1


def test_parses_15_minute_intervals_with_prefixed_namespace() -> None:
    xml_text = (FIXTURES / "load_15m_prefixed.xml").read_text()

    records = parse_load_xml(xml_text, **PARSER_METADATA)

    assert len(records) == 4
    assert all(record["duration_minutes"] == 15 for record in records)
    assert records[3]["interval_start_utc"].minute == 45
    assert records[3]["load_mw"] == 5300.0


def test_parses_multiple_periods() -> None:
    xml_text = (FIXTURES / "load_multiple_periods.xml").read_text()

    records = parse_load_xml(xml_text, **PARSER_METADATA)

    assert len(records) == 2
    assert records[0]["interval_start_utc"].hour == 0
    assert records[1]["interval_start_utc"].hour == 1


def test_rejects_missing_position() -> None:
    xml_text = (FIXTURES / "load_missing_position.xml").read_text()

    with pytest.raises(ValueError, match="position"):
        parse_load_xml(xml_text, **PARSER_METADATA)


def test_rejects_invalid_numeric_quantity() -> None:
    xml_text = (FIXTURES / "load_invalid_quantity.xml").read_text()

    with pytest.raises(ValueError, match="Invalid numeric load quantity"):
        parse_load_xml(xml_text, **PARSER_METADATA)