import typing
from typing import List

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.context import Markable

class Entity():
    def __init__(self, id: str) -> None:
        self._id = id
        self._markables: List[Markable] = []

    def id(self) -> str:
        return self._id

    def add_markable(self, markable: 'Markable'):
        self._markables += [markable]
