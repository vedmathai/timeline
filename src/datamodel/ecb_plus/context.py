from typing import Dict, List
from collections import defaultdict

from timeline.src.datamodel.ecb_plus.document import Document
from timeline.src.datamodel.ecb_plus.entities import Entity
from timeline.src.datamodel.ecb_plus.text import Sentence
from timeline.src.datamodel.ecb_plus.markable import Markable


class Context():
    def __init__(self):
        self._entities = {}
        self._dataset_id = None
        self._sentences = {}
        self._document2sentences = defaultdict(lambda: [])
        self._markables: Dict[str, Markable] = {}
        self._document2markables = defaultdict(lambda: [])

    def dataset_id(self) -> str:
        return self._dataset_id

    def get_entities_dict(self) -> Dict:
        return self._entities

    def get_entity_by_id(self, id: str, create: bool = True) -> Entity:
        if create is True:
            if id not in self._entities:
                self._entities[id] = Entity()
        return self._entities[id]

    def get_sentence(self, document: Document, id: str, create: bool = True) -> Sentence:
        sentence_id = Sentence.abs_id(document, id)
        if create is True and sentence_id not in self._sentences:
            sentence = Sentence(document=document, id=id)
            self._sentences[sentence_id] = sentence
            self._document2sentences[document.id()].append(sentence)
        return self._sentences[sentence_id]
        
    def get_sentences_by_document(self, document: Document) -> List[Sentence]:
        return self._document2sentences[document.id()]

    def get_markable(self, document: Document, markable_id: str, create: bool) -> Markable:
        return self._markables[markable_id]

    def get_markables_by_document(self, document: Document) -> List[Markable]:
        return self._document2markables[document.id()]

    def add_markable_to_document(self, document: Document, markable: Markable) -> None:
        self._document2markables[document.id()] += [markable]