import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.caevo.context import Context
    from timeline.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.entities import Entity


class Event():
    def __init__(self, id: str, eiid: str, offset: int, string: str, 
                 tense: str, aspect: str, event_class: str, polarity: str,
                 modality: str, happen: str, lower_bound_duration: str,
                 upper_bound_duration: str, document: 'Document') -> None:
        self._id = id
        self._eiid = eiid
        self._offset = offset
        self._string  = string
        self._tense = tense
        self._aspect = aspect
        self._event_class = event_class
        self._polarity = polarity
        self._modality = modality
        self._happen = happen
        self._lower_bound_duration = lower_bound_duration
        self._upper_bound_duration = upper_bound_duration
        self._document = document

    def id(self) -> str:
        return self._id

    def eiid(self) -> str:
        return self._eiid

    def offset(self) -> int:
        return self._offset

    def string(self) -> str:
        return self._string

    def tense(self) -> str:
        return self._tense

    def aspect(self) -> str:
        return self._aspect

    def event_class(self) -> str:
        return self._event_class

    def polarity(self) -> str:
        return self._polarity

    def modality(self) -> str:
        return self._modality
    
    def happen(self) -> str:
        return self._happen

    def lower_bound_duration(self) -> str:
        return self._lower_bound_duration

    def upper_bound_duration(self) -> str:
        return self._upper_bound_duration

    def document(self) -> str:
        return self._document

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document', ns: Dict):
        id = el.attrib['id']
        eiid = el.attrib['eiid']
        offset = int(el.attrib['offset'])
        string = el.attrib['string']
        tense = el.attrib['tense']
        aspect = el.attrib['aspect']
        event_class = el.attrib['class']
        polarity = el.attrib['polarity']
        modality = el.attrib['modality']
        happen = el.attrib['happen']
        lower_bound_duration = el.attrib['lowerBoundDuration']
        upper_bound_duration = el.attrib['upperBoundDuration']
        return Event(
            id=id,
            eiid=eiid,
            offset=offset,
            string=string,
            tense=tense,
            aspect=aspect,
            event_class=event_class,
            polarity=polarity,
            modality=modality,
            happen=happen,
            lower_bound_duration=lower_bound_duration,
            upper_bound_duration=upper_bound_duration,
            document=document,
        )
        