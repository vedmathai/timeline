import os
from typing import List, Dict

from timeline.src.datamodel.ecb_plus.document import Document
from timeline.src.datamodel.ecb_plus.entities import Entity
from timeline.src.datamodel.ecb_plus.context import Context


class Dataset():
    def __init__(self, documents: List[Document], context: Context) -> None:
        super().__init__()
        self._documents = {document.id(): document for document in documents}
        self._entities: List[Entity] = []

    def document_by_id(self, id: str) -> Document:
        return self._documents[id]

    def documents(self) -> Dict[str, Document]:
        return self._documents

    @staticmethod
    def from_folders(folder: str):
        documents = []
        context = Context()
        for inner_folder in os.listdir(folder):
            if inner_folder[0] == '.':
                continue
            for xml_file in os.listdir(os.path.join(folder, inner_folder)):
                if 'plus' not in xml_file or xml_file[0] == '.':
                    continue
                file_name = os.path.join(folder, inner_folder, xml_file)
                documents.append(Document.from_xml(xml_file=file_name, context=context))  # noqa
        return Dataset(documents=documents, context=context)
