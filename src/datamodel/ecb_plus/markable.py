import typing
from typing import List
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.text import Token
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.document import Document
    from timeline.src.datamodel.ecb_plus.entities import Entity


class Markable():
    def __init__(self, id: str, m_type: str) -> None:
        self._id = id
        self._m_type = m_type
        self._tokens: List['Token'] = []
        self._is_entity: bool = False
        self._entities: List[Entity] = []

    def id(self) -> str:
        return self._id

    def m_type(self) -> str:
        return self._m_type

    def is_entity(self) -> bool:
        return self._is_entity

    def tokens(self) -> List['Token']:
        return self._tokens

    def set_is_entity(self, val: bool) -> None:
        self._is_entity = val

    def add_token(self, token: 'Token') -> None:
        self._tokens.append(token)

    def set_entity(self, entity: 'Entity') -> None:
        self._entities.append(entity)

    @staticmethod
    def from_xml(el: Element, context: 'Context', document: 'Document'):
        m_type = el.tag
        id = el.attrib['m_id']
        markable = Markable(id=id, m_type=m_type)
        if 'TAG_DESCRIPTOR' in el.attrib:
            is_entity = True
            if 'instance_id' not in el:
                return
            context.get_entity_by_id(id=el.attrib['instance_id'])
            descriptor = el.attrib['TAG_DESCRIPTOR']
            markable.set_is_entity(True)
        else:
            markable.set_is_entity(False)
            for el2 in el.getchildren():
                if el.tag == 'token_anchor':
                    markable.add_token(context.get_token(document=document, id=el.attrib['t_id']))
        context.add_markable_to_document(document=document, markable=markable)