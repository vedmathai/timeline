import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.fabric.context import Context
    from timeline.src.datamodel.fabric.document import Document
    from timeline.src.datamodel.caevo.entities import Entity
    from timeline.src.datamodel.caevo.timex import Timex as CTimex
    from timeline.src.datamodel.ecb_plus.markable import Markable
    from timeline.src.datamodel.fabric.tlink import TLink


class Timex():
    def __init__(self, id: str, text: str, tokens: List['Token'], m_type: str,
                 length: int, timex_type: str, value: str, 
                 entities: List['Entity'], temporal_function: bool,
                 document: 'Document') -> None:
        self._id = id
        self._text = text
        self._tokens = tokens
        self._m_type = m_type
        self._length = length
        self._timex_type = timex_type
        self._entities = entities
        self._value = value
        self._temporal_function = temporal_function
        self._tlinks: Dict[str, 'TLink'] = {}
        self._document = document

    def id(self) -> str:
        return self._id

    def text(self) -> str:
        return self._text

    def tokens(self) -> List['Token']:
        return self._tokens

    def m_type(self) -> str:
        return self._m_type

    def length(self) -> int:
        return self._length

    def timex_type(self) -> str:
        return self._timex_type
    
    def entities(self) -> List['Entity']:
        return self._entities

    def value(self) -> str:
        return self._value

    def add_tlink(self, tlink: 'TLink') -> None:
        self._tlinks[tlink.id()] = tlink

    def tlinks(self) -> Dict[str, 'TLink']:
        return self._tlinks

    def temporal_function(self) -> bool:
        return self._temporal_function

    def document(self) -> 'Document':
        return self._document

    @staticmethod
    def from_caevo_ecb_plus(document: 'Document', context: 'Context',
                            ecb_markable: 'Markable', caevo_timex: 'CTimex'):
        if ecb_markable is None:
            return
        id = ecb_markable.id()
        text = caevo_timex.text()
        m_type = ecb_markable.m_type()
        tokens = ecb_markable.tokens()
        length = caevo_timex.length()
        timex_type = caevo_timex.timex_type()
        value = caevo_timex.value()
        temporal_function = caevo_timex.temporal_function()
        entities = [
            context.entity_by_document(document=document, entity_id=entity.id())
            for entity in ecb_markable.entities()
        ]
        timex = Timex(
            id=id,
            text=text,
            tokens=tokens,
            m_type=m_type,
            length=length,
            timex_type=timex_type,
            value=value,
            temporal_function=temporal_function,
            entities=entities,
            document=document,
        )
        for entity in entities:
            entity.add_timex(timex)
        context.add_caevo2timex(document=document, caevo_timex=caevo_timex, timex=timex)
        context.add_timex(document=document, timex=timex)
        