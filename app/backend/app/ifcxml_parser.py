from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable
from xml.etree import ElementTree as ET


@dataclass
class ParsedIfcEntity:
    ifc_id: str
    name: str


@dataclass
class ParsedIfcModel:
    building_name: str
    spaces: list[ParsedIfcEntity]
    walls: list[ParsedIfcEntity]
    windows: list[ParsedIfcEntity]


class IfcXmlParseError(ValueError):
    pass


def _findall(root: ET.Element, tag_name: str) -> Iterable[ET.Element]:
    return root.findall(f".//{{*}}{tag_name}")


def _parse_entities(root: ET.Element, tag_name: str) -> list[ParsedIfcEntity]:
    entities: list[ParsedIfcEntity] = []
    for element in _findall(root, tag_name):
        ifc_id = element.attrib.get("id") or element.attrib.get("ref")
        name = element.findtext("{*}Name")
        if not ifc_id:
            continue
        entities.append(ParsedIfcEntity(ifc_id=ifc_id, name=name or tag_name))
    return entities


def parse_ifcxml(content: bytes) -> ParsedIfcModel:
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        line, column = error.position
        raise IfcXmlParseError(f"IFC XML parse error at line {line}, column {column}: {error}") from error

    building_name = "Imported Building"
    building = next(iter(_findall(root, "IfcBuilding")), None)
    if building is not None:
        building_name = building.findtext("{*}Name") or building_name

    spaces = _parse_entities(root, "IfcSpace")
    walls = _parse_entities(root, "IfcWallStandardCase")
    windows = _parse_entities(root, "IfcWindow")

    if not spaces and not walls and not windows:
        raise IfcXmlParseError(
            "No supported IFC entities found. Expected at least one of: IfcSpace, IfcWallStandardCase, IfcWindow"
        )

    return ParsedIfcModel(
        building_name=building_name,
        spaces=spaces,
        walls=walls,
        windows=windows,
    )
