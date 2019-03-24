import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.caevo.context import Context
    from timeline.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.entities import Entity


class Timex():
    def __init__(self, id: str, text: str, offset: int, length: int,
                 timex_type: str, value: str, temporal_function: bool,
                 document: 'Document') -> None:  # noqa
        self._id = id
        self._text=text
        self._offset=offset
        self._length=length
        self._timex_type=timex_type
        self._value=value
        self._temporal_function=temporal_function
        self._document=document

    def id(self) -> str:
        return self._id

    def text(self) -> str:
        return self._text

    def offset(self) -> int:
        return self._offset

    def length(self) -> int:
        return self._length

    def timex_type(self) -> str:
        return self._timex_type

    def value(self) -> str:
        return self._value

    def temporal_function(self) -> bool:
        return self._temporal_function

    def document(self) -> 'Document':
        return self._document

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document', ns: Dict):
        m_type = el.tag
        id = el.attrib['tid']
        text = el.attrib['text']
        offset = int(el.attrib['offset'])
        length = int(el.attrib['length'])
        timex_type = el.attrib['type']
        value = el.attrib['value']
        temporal_function = bool(el.attrib['temporalFunction'])
        return Timex(
            id=id,
            text=text,
            offset=offset,
            length=length,
            timex_type=timex_type,
            value=value,
            temporal_function=temporal_function,
            document=document,
        )
        