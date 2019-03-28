import xml.etree.ElementTree as ET 
import typing
from typing import Dict, List
import editdistance

from timeline.src.datamodel.ecb_plus.document import Document as EDocument
from timeline.src.datamodel.caevo.document import Document as CDocument
from timeline.src.datamodel.ecb_plus.text import Token
from timeline.src.datamodel.ecb_plus.text import Sentence
from timeline.src.datamodel.ecb_plus.markable import Markable
from timeline.src.datamodel.caevo.event import Event as CEvent
from timeline.src.datamodel.fabric.entity import Entity
from timeline.src.datamodel.fabric.event import Event
from timeline.src.datamodel.fabric.timex import Timex
from timeline.src.datamodel.fabric.tlink import TLink

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.context import Context


class Document():
    def __init__(self, name: str = '') -> None:
        self._name = name
        self._sentences: Dict[str, Sentence] = {}

    def id(self) -> str:
        return self._name

    def sentences(self) -> Dict[str, Sentence]:
        return self._sentences

    def sentence_by_id(self, id: str) -> Sentence:
        return self._sentences[id]

    def entity_by_id(self, id: str) -> Entity:
        return self._entities[id]

    def timex_by_id(self, id: str) -> Timex:
        return self._timexes[id]
    
    def event_by_id(self, id: str) -> Event:
        return self._events[id]

    def events(self) -> Dict[str, Event]:
        return self._events

    def entities(self) -> Dict[str, Entity]:
        return self._entities

    def timexes(self) -> Dict[str, Timex]:
        return self._timexes

    def tlinks(self) -> Dict[str, TLink]:
        return self._tlinks

    def set_entities(self, entities: Dict[str, Entity]) -> None:
        self._entities = entities

    def set_events(self, events: Dict[str, Event]) -> None:
        self._events = events

    def set_timexes(self, timexes: Dict[str, Timex]) -> None:
        self._timexes = timexes

    def set_tlinks(self, tlinks: Dict[str, TLink]) -> None:
        self._tlinks = tlinks

    def set_sentences(self, sentences: List[Sentence]) -> None:
        self._sentences = {sentence.id(): sentence for sentence in sentences}

    def text(self) -> str:
        sentences: List[str] = []
        for sentence in self._sentences.values():
            sentences += [sentence.text()]
        return ' '.join(sentences)

    @staticmethod
    def from_caevo_ecb_plus(caevo_doc: CDocument, ecb_doc: EDocument, context: 'Context'):
        events: List[CEvent] = []
        document = Document(name=caevo_doc.id())
        for e_entity in ecb_doc.entities().values():
            Entity.from_ecb_plus(context=context, document=document, e_entity=e_entity)
        # Have to see why alignment isn't working in some cases and what about the rest of the markables.
        for sentence in caevo_doc.sentences().values():
            events += list(sentence.events().values())
        for sentence in ecb_doc.sentences().values():
            for tokeni, token in sentence.tokens().items():
                if len(events) == 0:
                    continue
                if editdistance.eval(token.text(), events[0].string()) <= 1:
                    Event.from_caevo_ecb_plus(
                        document=document,
                        context=context,
                        ecb_plus_markable=token.markable(),
                        caevo_event=events[0]
                    )
                    events = events[1:]
        timexes: List[Timex] = []
        for sentence in caevo_doc.sentences().values():
            timexes += list(sentence.timexes().values())
        for sentence in ecb_doc.sentences().values():
            tokens = list(sentence.tokens().values())
            for tokeni, token in enumerate(sentence.tokens().values()):
                if len(timexes) == 0:
                    continue
                str_size = len(timexes[0].text().split())
                token_text = ' '.join(t.text() for t in tokens[int(tokeni): int(tokeni)+str_size])
                if editdistance.eval(token_text, timexes[0].text()) <= 1:
                    Timex.from_caevo_ecb_plus(
                        document=document,
                        context=context,
                        ecb_markable=token.markable(),
                        caevo_timex=timexes[0]
                    )
                    timexes = timexes[1:]
        for tlink in caevo_doc.tlinks().values():
            TLink.from_caevo(c_tlink=tlink, document=document, context=context)
        document.set_entities(context.entities_by_document(document=document))
        document.set_events(context.events_by_document(document=document))
        document.set_timexes(context.timexes_by_document(document=document))
        document.set_tlinks(context.tlinks_by_document(document=document))
        context.add_document(document)
        
                