#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from operator import itemgetter
import math
import collections
from pprint import pprint


def _count(t, e, f, es, fs, keys=[]):
    if keys:
        _fs = [_f for (_e, _f) in keys if _e == e]
    else:
        _fs = fs
    sm = sum(t[(e, _f)] for _f in _fs)
    # for zero division
    if sm == 0:
        return 0
    else:
        return t[(e, f)] * es.count(e) * fs.count(f) / \
            sum(t[(e, _f)] for _f in _fs)


def _total(t, e, f, corpus, loop_count=1000):
    return sum(_count(t, e, f, es, fs) for (es, fs) in corpus)


def _train(corpus, loop_count=1000):
    t = collections.defaultdict(float)
    keys = set()
    e_keys = set()
    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            for e in es:
                keys.add((e, f))
    for (es, fs) in corpus:
        for (e, f) in (es, fs):
            e_keys.add(e)
            f_keys.add(f)
    # initialize the t-table
    for (e, f) in keys:
        t[(e, f)] = 1 / len(f_keys)
    # loop
    for i in xrange(loop_count):
        count = collections.defaultdict(float)
        total = collections.defaultdict(float)
        for (e, f) in keys:
            for (es, fs) in corpus:
                c = _count(t, e, f, es, fs)
                count[(e, f)] += c
                total[f] += c
        for (e, f) in keys:
            t[(e, f)] = count[(e, f)] / total[f]
    # remove zero keys
    for (k, v) in t.items():
        if v == 0:
            del t[k]
    return t


def train(sent_pairs, loop_count=1000):
    corpus = [(es.split(), fs.split()) for (es, fs) in sent_pairs]
    return _train(corpus, loop_count)


def _pprint(tbl):
    for (e, f), v in sorted(tbl.items(), key=itemgetter(1), reverse=True):
        print("p({e}|{f}) = {v}".format(e=e, f=f, v=v))


def probability(t, es, fs, epsilon=1):
    _es = es.split()
    _fs = fs.split()
    prod = 1
    for e in _es:
        t_sum = 0
        for f in _fs:
            t_sum += t[(e, f)]
        prod *= t_sum
    return epsilon * prod / math.pow((len(_fs)), len(_es))


if __name__ == '__main__':
    sent_pairs = [("the house", "das Haus"),
                  ("the book", "das Buch"),
                  ("a book", "ein Buch"),
                  ]
    t = train(sent_pairs, loop_count=0)
    pprint(t)
    print()
    t = train(sent_pairs, loop_count=1)
    pprint(t)
    print()
    t = train(sent_pairs, loop_count=2)
    pprint(t.items())
    print()
    t = train(sent_pairs, loop_count=3)
    pprint(t)
