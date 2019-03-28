import xml.etree.ElementTree as ET 
import typing
from typing import Dict, List

from timeline.src.datamodel.caevo.text import Token
from timeline.src.datamodel.caevo.text import Sentence
from timeline.src.datamodel.caevo.event import Event
from timeline.src.datamodel.caevo.timex import Timex
from timeline.src.datamodel.caevo.tlink import TLink

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.context import Context


class Document():
    def __init__(self, xml_file: str = '') -> None:
        self._id = id
        self._xml_file = xml_file
        self._sentences: Dict[str, Sentence] = {}
        self._events: Dict[str, Event] = {}
        self._timexes: Dict[str, Timex] = {}
        self._tlinks: Dict[str, TLink] = {}

    def id(self) -> str:
        return self._xml_file

    def sentences(self) -> Dict[str, Sentence]:
        return self._sentences

    def sentence_by_id(self, id: str) -> Sentence:
        return self._sentences[id]
    
    def event_by_id(self, event_id: str) -> Event:
        return self._events[event_id]

    def timex_by_id(self, timex_id: str) -> Timex:
        return self._timexes[timex_id]

    def set_sentences(self, sentences: List[Sentence]) -> None:
        self._sentences = {sentence.id(): sentence for sentence in sentences}

    def set_events(self, events: List[Event]) -> None:
        self._events = {event.eiid(): event for event in events}

    def set_timexes(self, timexes: List[Timex]) -> None:
        self._timexes = {timex.id(): timex for timex in timexes}

    def add_tlink(self, tlink: TLink) -> None:
        self._tlinks[tlink.inst_abs_id()] = tlink
    
    def tlinks(self) -> Dict[str, TLink]:
        return self._tlinks
    
    def timexes(self) -> Dict[str, Timex]:
        return self._timexes

    def text(self) -> str:
        sentences: List[str] = []
        for sentence in self._sentences.values():
            sentences += [sentence.text()]
        return ' '.join(sentences)

    @staticmethod
    def from_xml(xml_file: str, context: 'Context', ns: Dict):
        
        tree = ET.parse(xml_file)
        root = tree.getroot()

        file_el = root.find('d:file', namespaces=ns)
        document_name = file_el.attrib['name']
        document = Document(xml_file=document_name)
        for el in file_el.findall('d:entry', namespaces=ns):
            Sentence.from_xml(el=el, document=document, context=context, ns=ns)
        document.set_sentences(context.sentences_by_document(document=document))
        document.set_events(context.events_by_document(document=document))
        document.set_timexes(context.timexes_by_document(document=document))
        for el_i, el in enumerate(file_el.findall('d:tlink', namespaces=ns)):
            document.add_tlink(
                TLink.from_xml(
                    el=el,
                    context=context,
                    document=document,
                    count=el_i,
                    ns=ns,
                )
            )
        return document
