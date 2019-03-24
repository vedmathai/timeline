from timeline.src.datamodel.ecb_plus.dataset import Dataset
import os

def main():
    folder = '/Users/vedmathai/Documents/python/temporal/data/ECB+_LREC2014/ECB+'
    output = '/Users/vedmathai/Documents/python/temporal/data/ECB_text'
    dataset = Dataset.from_folders(folder)
    for documenti, document in dataset.documents().items():
        inner_folder, doc = documenti[len(folder)+1:].split('/')
        if not os.path.exists(os.path.join(output, inner_folder)):
            os.mkdir(os.path.join(output, inner_folder))
        with open(os.path.join(output, inner_folder, doc), 'wt') as f:
            f.write(document.text())

if __name__ == '__main__':
    main()