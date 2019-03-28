import typing
from typing import List, Dict
from xml.etree.ElementTree import Element

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.caevo.text import Token
    from timeline.src.datamodel.caevo.context import Context
    from timeline.src.datamodel.caevo.document import Document
    from timeline.src.datamodel.caevo.entities import Entity
    from timeline.src.datamodel.caevo.event import Event as CEvent
    from timeline.src.datamodel.ecb_plus.markable import markable as EMarkable
    from timeline.src.datamodel.fabric.tlink import TLink


class Event():
    def __init__(self, id: str, eiid: str, tokens: List['Token'], string: str, 
                 tense: str, aspect: str, event_class: str, polarity: str,
                 modality: str, happen: str, lower_bound_duration: str,
                 upper_bound_duration: str, entities: List['Entity'],
                 document: 'Document') -> None:
        self._id = id
        self._eiid = eiid
        self._tokens = tokens
        self._string  = string
        self._tense = tense
        self._aspect = aspect
        self._event_class = event_class
        self._polarity = polarity
        self._modality = modality
        self._happen = happen
        self._lower_bound_duration = lower_bound_duration
        self._upper_bound_duration = upper_bound_duration
        self._entities = entities
        self._tlinks: Dict[str, 'TLink'] = {}
        self._document = document

    def id(self) -> str:
        return '{}_{}'.format(self.document().id(), self._id)

    def eiid(self) -> str:
        return self._eiid

    def tokens(self) -> List['Token']:
        return self._tokens

    def string(self) -> str:
        return self._string

    def tense(self) -> str:
        return self._tense

    def aspect(self) -> str:
        return self._aspect

    def event_class(self) -> str:
        return self._event_class

    def polarity(self) -> str:
        return self._polarity

    def modality(self) -> str:
        return self._modality
    
    def happen(self) -> str:
        return self._happen

    def lower_bound_duration(self) -> str:
        return self._lower_bound_duration

    def upper_bound_duration(self) -> str:
        return self._upper_bound_duration

    def entities(self) -> List['Entity']:
        return self._entities

    def add_tlink(self, tlink: 'TLink') -> None:
        self._tlinks[tlink.id()] = tlink

    def tlinks(self) -> Dict[str, 'TLink']:
        return self._tlinks

    def document(self) -> 'Document':
        return self._document

    @staticmethod
    def from_caevo_ecb_plus(document: 'Document', context: 'Context',
                            ecb_plus_markable: 'EMarkable',
                            caevo_event: 'CEvent'):
        if ecb_plus_markable is None:
            return
        id = ecb_plus_markable.id()
        eiid = caevo_event.eiid()
        tokens = ecb_plus_markable.tokens()
        string = caevo_event.string()
        tense = caevo_event.tense()
        aspect = caevo_event.aspect()
        event_class = caevo_event.event_class()
        polarity = caevo_event.polarity()
        modality = caevo_event.modality()
        happen = caevo_event.happen()
        lower_bound_duration = caevo_event.lower_bound_duration()
        upper_bound_duration = caevo_event.upper_bound_duration()
        entities = [
            context.entity_by_document(document=document, entity_id=entity.id())
            for entity in ecb_plus_markable.entities()
        ]
        event = Event(
            id=id,
            eiid=eiid,
            tokens=tokens,
            string=string,
            tense=tense,
            aspect=aspect,
            event_class=event_class,
            polarity=polarity,
            modality=modality,
            happen=happen,
            lower_bound_duration=lower_bound_duration,
            upper_bound_duration=upper_bound_duration,
            document=document,
            entities=entities,
        )
        for entity in entities:
            entity.add_event(event)
        context.add_event(document=document, event=event)
        context.add_caevo2event(document=document, caevo_event=caevo_event, event=event)
        