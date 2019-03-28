import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

from timeline.src.datamodel.caevo.event import Event
from timeline.src.datamodel.caevo.timex import Timex

if typing.TYPE_CHECKING:
    from timelime.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.context import Context

class Token():
    def __init__(self, id: str, text: str, parent_sentence: 'Sentence') -> None:
        self._id = id
        self._text = text
        self._parent_sentence = parent_sentence

    def id(self) -> str:
        return self._id

    def parent_sentence(self) -> 'Sentence':
        return self._parent_sentence

    def text(self) -> str:
        return self._text

    @staticmethod
    def abs_id(document: 'Document', sentence: 'Sentence', id: str) -> str:
        return '{document}_{sentence}_{token}'.format(
            document=document.id(),
            sentence=sentence.id(),
            token=id,
        )

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document',
                 parent_sentence: 'Sentence', count: int, ns: Dict):
        id = str(count)
        text = el.text.strip('" " "')
        token = Token(id=id, text=text, parent_sentence=parent_sentence)
        return token


class Sentence():
    def __init__(self, id: str, document: 'Document') -> None:
        self._parent_document = document
        self._id = id
        self._tokens: Dict[str, 'Token'] = {}
        self._timexes: Dict[str, Timex] = {}
        self._events: Dict[str, Event] = {}

    def id(self) -> str:
        return self._id

    def parent_document(self) -> 'Document':
        return self._parent_document

    def add_token(self, token: 'Token') -> None:
        self._tokens[token.id()] = token

    def add_timex(self, timex: Timex) -> None:
        self._timexes[timex.id()] = timex
    
    def add_event(self, event: Event) -> None:
        self._events[event.id()] = event

    def text(self) -> str:
        tokens: List[str] = []
        for key in sorted(list(self._tokens.keys()), key=lambda x: int(x)):
            tokens += [self._tokens[key].text()]
        return ' '.join(tokens)

    @staticmethod
    def abs_id(document: 'Document', id: str) -> str:
        return '{document}_{sentence}'.format(document=document.id(), sentence=id)  # noqa
    
    @staticmethod
    def from_xml(el, context: 'Context', document: 'Document', ns: Dict) -> 'Sentence':
        id = el.attrib['sid']
        sentence = Sentence(id=id, document=document)
        for token_i, token in enumerate(el.find('d:tokens', namespaces=ns).getchildren()):
            sentence.add_token(
                token=Token.from_xml(
                    el=token,
                    context=context,
                    document=document,
                    parent_sentence=sentence,
                    count=token_i,
                    ns=ns,
                )
            )
        context.add_sentence(sentence=sentence, document=document)
        for timex_el in el.find('d:timexes', namespaces=ns).getchildren():
            timex = Timex.from_xml(el=timex_el, context=context, document=document, ns=ns)
            context.add_timex(timex=timex, document=document)
            sentence.add_timex(timex=timex)
        for event_el in el.find('d:events', namespaces=ns).getchildren():
            event = Event.from_xml(el=event_el, context=context, document=document, ns=ns)
            context.add_event(event=event, document=document)
            sentence.add_event(event=event)
        return sentence
