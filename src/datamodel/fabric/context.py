from typing import Dict, List
from collections import defaultdict

from timeline.src.datamodel.caevo.document import Document
from timeline.src.datamodel.caevo.timex import Timex
from timeline.src.datamodel.caevo.text import Sentence
from timeline.src.datamodel.caevo.event import Event
from timeline.src.datamodel.fabric.entity import Entity
from timeline.src.datamodel.fabric.tlink import TLink


class Context():
    def __init__(self):
        self._entities = {}
        self._documents = {}
        self._document2sentences = defaultdict(lambda: [])
        self._document2events = defaultdict(lambda: defaultdict(lambda: None))
        self._document2timex = defaultdict(lambda: defaultdict(lambda: None))
        self._document2entity = defaultdict(lambda: defaultdict(lambda: None))
        self._document2tlink = defaultdict(lambda: defaultdict(lambda: None))
        self._caevo2event = defaultdict(lambda: None)
        self._caevo2timex = defaultdict(lambda: None)

    def add_document(self, document: Document) -> None:
        self._documents[document.id()] = document

    def add_event(self, event: Event, document: Document) -> None:
        self._document2events[document.id()][event.id()] = event

    def add_timex(self, timex: Timex, document: Document) -> None:
        self._document2timex[document.id()][timex.id()] = timex

    def add_sentence(self, sentence: Sentence, document: Document) -> None:
        self._document2sentences[document.id()].append(sentence)

    def add_entity(self, entity_id: str, document: Document) -> None:
        if entity_id not in self._entities:
            entity = Entity(id=entity_id)
            self._entities[entity.id()] = entity
        self._document2entity[document.id()][entity_id] = self._entities[entity_id]  # noqa

    def document_by_id(self, document_id: str) -> Document:
        return self._documents[document_id]

    def documents(self) -> Dict[str, Document]:
        return self._documents

    def events_by_document(self, document: Document) -> Dict[str, Event]:
        return self._document2events[document.id()]
    
    def event_by_id(self, document: Document, event_id: str) -> Event:
        return self._document2events[document.id()][event_id]

    def timex_by_id(self, document: Document, timex_id: str) -> Timex:
        return self._document2events[document.id()][timex_id]

    def timexes_by_document(self, document: Document) -> Dict[str, Timex]:
        return self._document2timex[document.id()]

    def sentences_by_document(self, document: Document) -> Sentence:
        return self._document2sentences[document.id()]

    def entities_by_document(self, document: Document) -> Dict[str, Entity]:
        return dict(self._document2entity[document.id()])

    def entity_by_document(self, document: Document, entity_id: str) -> Entity:
        return self._document2entity[document.id()][entity_id]
    
    def add_tlink(self, document: Document, tlink: TLink) -> None:
        self._document2tlink[document.id()][tlink.id()] = tlink

    def tlink_by_document(self, document: Document, tlink_id: str) -> TLink:
        return self._document2tlink[document.id()][tlink_id]

    def tlinks_by_document(self, document: Document) -> Dict[str, TLink]:
        return self._document2tlink[document.id()]

    def add_caevo2event(self, document: Document, caevo_event: 'CEvent', event: Event) -> None:  # noqa
        self._caevo2event[caevo_event] = event

    def add_caevo2timex(self, document: Document, caevo_timex: 'CTimex', timex: Timex) -> None:  # noqa
        self._caevo2timex[caevo_timex] = timex

    def caevo2event(self, document: Document, caevo_event: 'CEvent') -> Event:
        return self._caevo2event[caevo_event]

    def caevo2timex(self, document: Document, caevo_timex: 'CTimex') -> Event:
        return self._caevo2timex[caevo_timex]
