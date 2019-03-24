import typing
from typing import List, Union, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.caevo.context import Context
    from timeline.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.timex import Timex
    from timeline.src.datamodel.caevo.event import Event
    

class TLink():
    def __init__(self, id: str, event1: Union['Timex', 'Event'], 
                 event2: Union['Timex', 'Event'], relation: str, closed: bool,
                 origin: str, tlink_type: str, document: 'Document') -> None:
        self._id = id
        self._event1 = event1
        self._event2 = event2
        self._relation = relation
        self._closed = closed
        self._origin = origin
        self._tlink_type = tlink_type
        self._document = document

    def id(self) -> str:
        return self._id

    def event1(self) -> Union['Timex', 'Event']:
        return self._event1

    def event2(self) -> Union['Timex', 'Event']:
        return self._event2

    def relation(self) -> str:
        return self._relation

    def closed(self) -> bool:
        return self._closed

    def origin(self) -> str:
        return self._origin

    def tlink_type(self) -> str:
        return self._tlink_type

    def document(self) -> 'Document':
        return self._document

    def inst_abs_id(self) -> str:
        return TLink.abs_id(
            document=self.document(),
            e1=self.event1(),
            e2=self.event2(),
        )

    @staticmethod
    def abs_id(document: 'Document', e1: Union['Event', 'Timex'], e2: Union['Event', 'Timex']) -> str:
        return "{document}_{e1}_{e2}".format(document=document.id(), e1=e1.id(), e2=e2.id())

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document', count: int, ns: Dict):
        id = str(count)
        event1_id = el.attrib['event1']
        event2_id = el.attrib['event2']
        relation = el.attrib['relation']
        closed = bool(el.attrib['closed'])
        origin = el.attrib['origin']
        tlink_type = el.attrib['type']

        def get_event(event_id: str, event_type: str) -> Union['Event', 'Timex']:
            if event_type == 'e':
                event = document.event_by_id(event_id=event_id)
            if event_type == 't':
                event = document.timex_by_id(timex_id=event_id)
            return event
        event1 = get_event(event_id=event1_id, event_type=event1_id[0])
        event2 = get_event(event_id=event2_id, event_type=event2_id[0])
        return TLink(
            id=id,
            event1=event1,
            event2=event2,
            relation=relation,
            closed=closed,
            origin=origin,
            tlink_type=tlink_type,
            document=document,
        )
        