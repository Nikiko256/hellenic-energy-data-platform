"""Parse ENTSO-E actual-load XML into Silver-ready interval records."""

import re
import xml.etree.ElementTree as ET
from datetime import UTC, datetime, timedelta


def parse_load_xml(
    xml_text: str,
    *,
    area_code: str,
    source_request_id: str,
    source_payload_sha256: str,
    ingested_at_utc: datetime,
) -> list[dict[str, object]]:
    """Convert ENTSO-E actual-load XML into one record per source interval."""
    root = ET.fromstring(xml_text)
    source_document_id = _first_descendant_text(root, "mRID")

    if source_document_id is None:
        raise ValueError("Missing required XML element: mRID")

    records: list[dict[str, object]] = []

    for period in _descendants(root, "Period"):
        period_start = _parse_utc(
            _required_path_text(period, "timeInterval", "start")
        )
        period_end = _parse_utc(
            _required_path_text(period, "timeInterval", "end")
        )
        duration_minutes = _parse_duration_minutes(
            _required_child_text(period, "resolution")
        )

        seen_positions: set[int] = set()

        for point in _children(period, "Point"):
            try:
                position = int(_required_child_text(point, "position"))
            except ValueError as error:
                raise ValueError("Invalid ENTSO-E point position.") from error

            if position < 1:
                raise ValueError("ENTSO-E point position must be at least 1.")

            if position in seen_positions:
                raise ValueError(f"Duplicate ENTSO-E point position: {position}")

            seen_positions.add(position)

            try:
                load_mw = float(_required_child_text(point, "quantity"))
            except ValueError as error:
                raise ValueError("Invalid numeric load quantity.") from error

            interval_start = period_start + timedelta(
                minutes=(position - 1) * duration_minutes
            )
            interval_end = interval_start + timedelta(minutes=duration_minutes)

            if interval_end > period_end:
                raise ValueError(
                    f"Point {position} ends after the declared ENTSO-E period."
                )

            records.append(
                {
                    "area_code": area_code,
                    "interval_start_utc": interval_start,
                    "interval_end_utc": interval_end,
                    "duration_minutes": duration_minutes,
                    "load_mw": load_mw,
                    "source_document_id": source_document_id,
                    "source_request_id": source_request_id,
                    "source_payload_sha256": source_payload_sha256,
                    "ingested_at_utc": ingested_at_utc,
                }
            )

    return sorted(records, key=lambda record: record["interval_start_utc"])


def _local_name(tag: str) -> str:
    """Return an XML tag name without its namespace."""
    return tag.split("}")[-1]


def _children(element: ET.Element, name: str) -> list[ET.Element]:
    """Return direct children with a matching local tag name."""
    return [child for child in element if _local_name(child.tag) == name]


def _descendants(element: ET.Element, name: str) -> list[ET.Element]:
    """Return all descendants with a matching local tag name."""
    return [child for child in element.iter() if _local_name(child.tag) == name]


def _first_descendant_text(element: ET.Element, name: str) -> str | None:
    """Return text from the first matching descendant, if present."""
    for child in _descendants(element, name):
        if child.text:
            return child.text.strip()
    return None


def _required_child_text(element: ET.Element, name: str) -> str:
    """Read text from a required direct child XML element."""
    matching_children = _children(element, name)

    if not matching_children or not matching_children[0].text:
        raise ValueError(f"Missing required XML element: {name}")

    return matching_children[0].text.strip()


def _required_path_text(
    element: ET.Element,
    parent_name: str,
    child_name: str,
) -> str:
    """Read text from a required nested XML element."""
    matching_parents = _children(element, parent_name)

    if not matching_parents:
        raise ValueError(f"Missing required XML element: {parent_name}")

    return _required_child_text(matching_parents[0], child_name)


def _parse_utc(value: str) -> datetime:
    """Parse a timezone-aware ENTSO-E timestamp into UTC."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))

    if parsed.tzinfo is None:
        raise ValueError(f"Timestamp must include timezone information: {value}")

    return parsed.astimezone(UTC)


def _parse_duration_minutes(value: str) -> int:
    """Parse ISO durations such as PT60M and PT15M."""
    match = re.fullmatch(r"PT(?:(\d+)H)?(?:(\d+)M)?", value)

    if not match:
        raise ValueError(f"Unsupported ENTSO-E resolution: {value}")

    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    total_minutes = hours * 60 + minutes

    if total_minutes <= 0:
        raise ValueError(f"Resolution must be positive: {value}")

    return total_minutes