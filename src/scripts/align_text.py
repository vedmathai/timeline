from timeline.src.datamodel.fabric.dataset import Dataset
from collections import defaultdict

def main():
    c_folder = '/Users/vedmathai/Documents/python/temporal/data/ECB_text'
    e_folder = '/Users/vedmathai/Documents/python/temporal/data/ECB+_LREC2014/ECB+'
    dataset = Dataset.from_caevo_ecb_plus(caevo_folder=c_folder, ecb_plus_folder=e_folder)
    documents = list(dataset.documents().values())
    adj = defaultdict(lambda: defaultdict(lambda: '0'))
    entities = set()
    for document in documents:
        for tlink in document.tlinks().values():
            rel = tlink.relation()
            if len(tlink.event1().entities()) > 0 and\
               len(tlink.event2().entities()) > 0 and\
               rel != 'VAGUE':
                entity1 = tlink.event1().entities()[0]
                entity2 = tlink.event2().entities()[0]
                print(entity1.id(), rel, entity2.id(), document.id())
                if rel == 'AFTER':
                    adj[entity2.id()][entity1.id()] = '1'
                if rel == 'BEFORE':
                    adj[entity1.id()][entity2.id()] = '1'
                entities.add(entity1.id())
                entities.add(entity2.id())
    entities = sorted(list(entities))
    for row in entities:
        for col in entities:
            print(adj[row][col]+', ', end='')
        print(end='\n')

    #for timex in document.timexes().values():
    #    print(timex.id(), timex.text(), timex.entities())


if __name__ == '__main__':
    main()