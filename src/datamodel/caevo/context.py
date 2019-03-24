from typing import Dict, List
from collections import defaultdict

from timeline.src.datamodel.caevo.document import Document
from timeline.src.datamodel.caevo.timex import Timex
from timeline.src.datamodel.caevo.text import Sentence
from timeline.src.datamodel.caevo.event import Event


class Context():
    def __init__(self):
        self._entities = {}
        self._document2sentences = defaultdict(lambda: [])
        self._document2events = defaultdict(lambda: [])
        self._document2timex = defaultdict(lambda: [])

    def add_event(self, event: Event, document: Document) -> None:
        self._document2events[document.id()].append(event)

    def add_timex(self, timex: Timex, document: Document) -> None:
        self._document2timex[document.id()].append(timex)

    def add_sentence(self, sentence: Sentence, document: Document) -> None:
        self._document2sentences[document.id()].append(sentence)

    def events_by_document(self, document: Document) -> Event:
        return self._document2events[document.id()]

    def timexes_by_document(self, document: Document) -> Timex:
        return self._document2timex[document.id()]

    def sentences_by_document(self, document: Document) -> Sentence:
        return self._document2sentences[document.id()]
