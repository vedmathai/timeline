from timeline.src.datamodel.ecb_plus.dataset import Dataset
import spacy
import json

nlp = spacy.load("en_core_web_sm")


def main():
    e_folder = '/Users/vedmathai/Documents/python/temporal/data/ECB+_LREC2014/ECB+'  # noqa
    ds = Dataset.from_folders(e_folder)
    data = []
    for document in list(ds.documents().values())[:1]:
        if '32_' not in document.id():
            continue
        print(document.id())
        for entity in document.entities().values():
            e2d = entity2datapoint(entity)
            data += [e2d]
            print(len(e2d))
            if len(e2d) <= 0:
                break
    with open('intial_data.json', 'wt') as f:
        json.dump(data, f)


def entity2datapoint(entity):
    datapoints = []
    for markable in entity.markables().values():
        markable_dp = {}
        markable_dp['tokens'] = ' '.join(token.text() for token in markable.tokens())
        token = markable.tokens()[0]
        markable_dp['sentence'] = token.parent_sentence().text()
        sentence = token.parent_sentence()
        first_token = min(int(tid) for tid in sentence.tokens())
        parse = nlp(token.parent_sentence().text())
        offset_id = int(token.id()) - first_token
        spacy_token = list(parse)[offset_id]
        markable_dp['clause'] = word2clause(spacy_token)
        markable_dp['sentences'] = sentences(sentence)
        markable_dp['document'] = sentence.parent_document().id()
        markable_dp['entity'] = entity.id()
        datapoints += [markable_dp]
    return datapoints
    # print([sen.text() for sen in document.sentences().values()])


def sentences(sentence, num=2):
    prev = prev_sents(sentence.previous_sentence(), num=num/2)
    nex = next_sents(sentence.next_sentence(), num=num/2)
    return ' '.join([prev, sentence.text(), nex])


def prev_sents(sentence, num):
    if num == 0 or sentence is None:
        return ''
    else:
        return ' '.join([prev_sents(sentence.previous_sentence(), num-1), sentence.text()])


def next_sents(sentence, num):
    if num == 0 or sentence is None:
        return ''
    else:
        return ' '.join([next_sents(sentence.next_sentence(), num-1), sentence.text()])


def word2clause(word):
    word = lowest_clause_root(word)
    not_allowed = set()
    text = []
    for sub_word in word.subtree:
        if sub_word != word and clause_root(sub_word):
            not_allowed |= set(subtree_range(sub_word))
    for sub_word in word.subtree:
        if sub_word.i not in not_allowed:
            text += ['{}'.format(sub_word.text, sub_word.dep_)]
    return (' '.join(text))


def clause_root(word):
    if word.dep_ in ['ccomp', 'xcomp', 'pcomp', 'advcl']:
        return True
    if word.dep_ in ['conj'] and word.pos_ in ['VERB']:
        return True
    return False


def subtree_range(word):
    rang = [t.i for t in word.subtree]
    return range(min(rang), max(rang))


def lowest_clause_root(word):
    while word.head != word:
        if clause_root(word):
            return word
        else:
            word = word.head
    return word


if __name__ == '__main__':
    main()
    #sentence2clause('King George V and Queen Mary dismissed a nanny who pinched their eldest son, the future Edward VIII and neglected their second son, the future George VI, after she had been in their employment for three years, demonstrating that royal parents of the time were not necessarily aware of how nannies behaved toward the children in their care.')