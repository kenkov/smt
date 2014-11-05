#! /usr/bin/env python
# coding:utf-8

from operator import itemgetter
import collections
from smt.utils import utility
import decimal
from decimal import Decimal as D

# set deciaml context
decimal.getcontext().prec = 4
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


def _constant_factory(value):
    '''define a local function for uniform probability initialization'''
    #return itertools.repeat(value).next
    return lambda: value


def _train(corpus, loop_count=1000):
    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            f_keys.add(f)
    # default value provided as uniform probability)
    t = collections.defaultdict(_constant_factory(D(1/len(f_keys))))

    # loop
    for i in range(loop_count):
        count = collections.defaultdict(D)
        total = collections.defaultdict(D)
        s_total = collections.defaultdict(D)
        for (es, fs) in corpus:
            # compute normalization
            for e in es:
                s_total[e] = D()
                for f in fs:
                    s_total[e] += t[(e, f)]
            for e in es:
                for f in fs:
                    count[(e, f)] += t[(e, f)] / s_total[e]
                    total[f] += t[(e, f)] / s_total[e]
                    #if e == u"に" and f == u"always":
                    #    print(" BREAK:", i, count[(e, f)])
        # estimate probability
        for (e, f) in count.keys():
            #if count[(e, f)] == 0:
            #    print(e, f, count[(e, f)])
            t[(e, f)] = count[(e, f)] / total[f]

    return t


def train(sentences, loop_count=1000):
    corpus = utility.mkcorpus(sentences)
    return _train(corpus, loop_count)


def _pprint(tbl):
    for (e, f), v in sorted(tbl.items(), key=itemgetter(1), reverse=True):
        print(u"p({e}|{f}) = {v}".format(e=e, f=f, v=v))


if __name__ == '__main__':
    sentences = [("the house", "das Haus"),
                 ("the book", "das Buch"),
                 ("a book", "ein Buch"),
                 ]
    t = train(sentences, loop_count=0)
    pprint(t)
    t = train(sentences, loop_count=1)
    pprint(t)
    t = train(sentences, loop_count=2)
    pprint(t)
    t = train(sentences, loop_count=3)
    pprint(t)
