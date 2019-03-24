from timeline.src.datamodel.caevo.dataset import Dataset as CDataset
from timeline.src.datamodel.ecb_plus.dataset import Dataset as EDataset

def main():
    c_dataset = CDataset.from_folders('/Users/vedmathai/Documents/python/temporal/data/ECB_text')
    e_dataset = EDataset.from_folders('/Users/vedmathai/Documents/python/temporal/data/ECB+_LREC2014/ECB+')
    for document_id in e_dataset.documents():
        e_document = e_dataset.document_by_id(document_id)
        c_document = c_dataset.document_by_id(document_id)
        for sentence_i, sentence in enumerate(e_document.sentences().values()):
            print(sentence_i, sentence.text())
        print('-----')
        for sentence_i, sentence in enumerate(c_document.sentences().values()):
            print(sentence_i, sentence.text())
        break


if __name__ == '__main__':
    main()