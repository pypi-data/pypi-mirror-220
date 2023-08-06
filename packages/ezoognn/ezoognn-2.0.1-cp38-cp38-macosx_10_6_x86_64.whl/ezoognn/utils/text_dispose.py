from torchtext.data.utils import get_tokenizer
from torchtext.vocab import build_vocab_from_iterator


def build_vocab(item_texts, itemid_order=None, batch_first=True):
    '''

    Parameters
    ----------
    item_texts  文本特征，{"title": [], "content":[]}
    itemid_order 条目顺序，通常为[0,1,2,3,4,...,n]
    batch_first

    Returns
    -------

    '''
    textset = {}
    tokenizer = get_tokenizer(None)

    textlist = []

    for i in itemid_order:
        for key in item_texts.keys():
            l = tokenizer(item_texts[key][i].lower())
            textlist.append(l)
    for key, field in item_texts.items():
        vocab2 = build_vocab_from_iterator(
            textlist, specials=["<unk>", "<pad>"]
        )
        textset[key] = (
            textlist,
            vocab2,
            vocab2.get_stoi()["<pad>"],
            batch_first,
        )

    return textset