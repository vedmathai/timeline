import typing
from typing import List, Union, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.caevo.context import Context
    from timeline.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.timex import Timex as CTimex
    from timeline.src.datamodel.caevo.event import Event as CEvent
    from timeline.src.datamodel.caevo.tlink import TLink as CTLink
    from timeline.src.datamodel.fabric.timex import Timex
    from timeline.src.datamodel.fabric.event import Event
    

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
    def from_caevo(c_tlink: 'CTLink', context: 'Context', document: 'Document'):
        id = c_tlink.id()
        event1 = c_tlink.event1()
        event2 = c_tlink.event2()
        relation = c_tlink.relation()
        closed = c_tlink.closed()
        origin = c_tlink.origin()
        tlink_type = c_tlink.tlink_type()

        def get_event(event: Union['CEvent', 'CTimex'], event_type: str) -> Union['Event', 'Timex']:  # noqa
            if event_type == 'e':
                event = context.caevo2event(document=document, caevo_event=event)  # noqa
            if event_type == 't':
                event = context.caevo2timex(document=document, caevo_timex=event)  # noqa
            return event
        event1 = get_event(event=event1, event_type=tlink_type[0])
        event2 = get_event(event=event2, event_type=tlink_type[1])
        t_link = TLink(
            id=id,
            event1=event1,
            event2=event2,
            relation=relation,
            closed=closed,
            origin=origin,
            tlink_type=tlink_type,
            document=document,
        )
        if event1 is not None and event2 is not None:
            event1.add_tlink(tlink=t_link)
            event2.add_tlink(tlink=t_link)
            context.add_tlink(document, t_link)
