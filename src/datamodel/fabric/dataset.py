import os
from typing import List, Dict

from timeline.src.datamodel.ecb_plus.dataset import Dataset as EDataset
from timeline.src.datamodel.caevo.dataset import Dataset as CDataset
from timeline.src.datamodel.fabric.document import Document
from timeline.src.datamodel.fabric.entity import Entity
from timeline.src.datamodel.fabric.context import Context


class Dataset():
    def __init__(self, context: Context) -> None:
        super().__init__()
        self._documents: Dict[str, Document] = {}

    def set_documents(self, documents: Dict[str, Document]) -> None:
        self._documents = documents

    def document_by_id(self, id: str) -> Document:
        return self._documents[id]

    def documents(self) -> Dict[str, Document]:
        return self._documents

    def set_entities(self, entities: Dict[str, Entity]) -> None:
        self._entities = entities

    def entities(self) -> Dict[str, Entity]:
        return self._entities

    @staticmethod
    def from_caevo_ecb_plus(caevo_folder: str, ecb_plus_folder: str):
        context = Context()
        dataset = Dataset(context=context)
        caevo = CDataset.from_folders(caevo_folder)
        ecb_plus = EDataset.from_folders(ecb_plus_folder)
        context = Context()
        for doci, doc in enumerate(caevo.documents()):
            if doc[:2] != '2_':
                continue
            print(doc)
            Document.from_caevo_ecb_plus(
                caevo_doc=caevo.document_by_id(doc),
                ecb_doc=ecb_plus.document_by_id(doc),
                context=context,
            )
        dataset.set_documents(context.documents())
        return dataset
