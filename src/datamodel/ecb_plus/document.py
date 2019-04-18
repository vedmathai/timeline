import xml.etree.ElementTree as ET 
import typing
from typing import Dict, List

from timeline.src.datamodel.ecb_plus.text import Token
from timeline.src.datamodel.ecb_plus.text import Sentence
from timeline.src.datamodel.ecb_plus.markable import Markable

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.Entity import Entity


class Document():
    def __init__(self, xml_file: str = '') -> None:
        self._id = id
        self._xml_file = xml_file
        self._sentences: Dict[str, Sentence] = {}
        self._markables: Dict[str, Markable] = {}
        self._entities: Dict[str, Entity] = {}

    def id(self) -> str:
        return self._xml_file

    def sentences(self) -> Dict[str, Sentence]:
        return self._sentences

    def markables(self) -> Dict[str, Markable]:
        return self._markables

    def entities(self) -> Dict[str, 'Entity']:
        return self._entities

    def sentence_by_id(self, id: str) -> Sentence:
        return self._sentences[id]

    def markable_by_id(self, id: str) -> Markable:
        return self._markables[id]

    def set_entities(self, entities: Dict[str, 'Entity']) -> None:
        self._entities = entities

    def set_sentences(self, sentences: List[Sentence]) -> None:
        self._sentences = {sentence.id(): sentence for sentence in sentences}

    def set_markables(self, markables: List[Markable]) -> None:
        self._markables = {markable.id(): markable for markable in markables}

    def text(self) -> str:
        sentences: List[str] = []
        for sentence in self._sentences.values():
            sentences += [sentence.text()]
        return ' '.join(sentences)

    @staticmethod
    def from_xml(xml_file: str, context: 'Context'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        file_name = root.attrib['doc_name']
        document = Document(xml_file=file_name)
        for el in root.findall('token'):
            Token.from_xml(el=el, context=context, document=document)
        sentences = context.get_sentences_by_document(document=document)
        document.set_sentences(sentences=sentences)
        markables = root.find('Markables')
        for el in markables.getchildren():
            markable = Markable.from_xml(el=el, context=context, document=document)
        document.set_markables(context.get_markables_by_document(document=document))
        relations = root.find('Relations')
        for el in relations.getchildren():
            sources: List[str] = []
            if 'note' not in el.attrib:
                continue
            entity = context.get_entity_by_id(el.attrib['note'])
            for el2 in el.getchildren():
                if el2.tag == 'source':
                    id = el2.attrib['m_id']
                    markable = document.markable_by_id(id)
                    entity.add_markable(markable)
                    markable.set_entity(entity=entity)
        document.set_entities(context.entities())
        return document
