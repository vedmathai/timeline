import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timelime.src.datamodel.ecb_plus.document import Document
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.markable import Markable

class Sentence():
    def __init__(self, id: str, document: 'Document') -> None:
        self._parent_document = document
        self._id = id
        self._tokens: Dict[str, 'Token'] = {}

    def id(self) -> str:
        return self._id

    def parent_document(self) -> 'Document':
        return self._parent_document

    def add_token(self, token: 'Token') -> None:
        self._tokens[token.id()] = token
    
    def tokens(self) -> Dict[str, 'Token']:
        return self._tokens

    def token_by_id(self, id: str) -> 'Token':
        return self._tokens[id]

    def text(self) -> str:
        tokens: List[str] = []
        for key in sorted(list(self._tokens.keys()), key=lambda x: int(x)):
            tokens += [self._tokens[key].text()]
        return ' '.join(tokens)

    @staticmethod
    def abs_id(document: 'Document', id: str) -> str:
        return '{document}_{sentence}'.format(document=document.id(), sentence=id)  # noqa


class Token():
    def __init__(self, id: str, text: str, parent_sentence: Sentence) -> None:
        self._id = id
        self._text = text
        self._parent_sentence = parent_sentence
        self._markable: 'Markable' = None

    def id(self) -> str:
        return self._id

    def parent_sentence(self) -> Sentence:
        return self._parent_sentence

    def add_markable(self, markable: 'Markable') -> None:
        self._markable = markable

    def markable(self) -> 'Markable':
        return self._markable

    def text(self) -> str:
        return self._text

    @staticmethod
    def abs_id(document: 'Document', sentence: Sentence, id: str) -> str:
        return '{document}_{sentence}_{token}'.format(
            document=document.id(),
            sentence=sentence.id(),
            token=id,
        )

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document'):
        id = el.attrib['t_id']
        parent_sentence_id = el.attrib['sentence']
        text = el.text
        parent_sentence = context.get_sentence(document=document, id=parent_sentence_id)  # noqa
        token = Token(id=id, text=text, parent_sentence=parent_sentence)
        context.add_document_to_token(document=document, token=token)
        parent_sentence.add_token(token)
        return token