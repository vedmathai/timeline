import typing
from typing import List

if typing.TYPE_CHECKING:
    from timeline.src.datamodel.ecb_plus.context import Context
    from timeline.src.datamodel.ecb_plus.context import Markable

class Entity():
    def __init__(self) -> None:
        self._markables: List[Markable] = []

    def add_markable(self, markable: 'Markable'):
        self._markables += [markable]
