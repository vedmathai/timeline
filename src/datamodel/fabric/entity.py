import typing
from typing import List, Dict
from collections import defaultdict

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.fabric.context import Context
    from timeline.src.datamodel.ecb_plus.entity import Entity as EEntity
    from timeline.src.datamodel.fabric.document import Document
    from timeline.src.datamodel.fabric.event import Event
    from timeline.src.datamodel.fabric.timex import Timex

class Entity():
    def __init__(self, id: str) -> None:
        self._id = id
        self._events: Dict[str, 'Event'] = defaultdict(lambda: None)
        self._timexes: Dict[str, 'Timex'] = defaultdict(lambda: None)

    def id(self) -> str:
        return self._id

    def add_event(self, event: 'Event') -> None:
        self._events[event.id()] = event

    def add_timex(self, timex: 'Timex') -> None:
        self._timexes[timex.id()] = timex

    def timex_by_id(self, timex_id: str) -> 'Timex':
        return self._timexes[timex_id]

    def event_by_id(self, event_id: str) -> 'Event':
        return self._events[event_id]

    def timexes(self) -> Dict[str, 'Timex']:
        return self._timexes

    def events(self) -> Dict[str, 'Event']:
        return self._events

    @staticmethod
    def from_ecb_plus(context: 'Context', document: 'Document', e_entity: 'EEntity'):
        context.add_entity(document=document, entity_id=e_entity.id())
