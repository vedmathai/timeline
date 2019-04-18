import typing
from typing import Dict

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.context import Markable

class Entity():
    def __init__(self, id: str) -> None:
        self._id = id
        self._markables: Dict[str, 'Markable'] = {}

    def id(self) -> str:
        return self._id

    def add_markable(self, markable: 'Markable'):
        self._markables[markable.id()] = markable
    
    def markables(self) -> Dict[str, 'Markable']:
        return self._markables
