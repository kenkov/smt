#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from operator import itemgetter
import math
import collections
from pprint import pprint
import itertools


def _constant_factory(value):
    '''define a local function for uniform probability initialization'''
    return itertools.repeat(value).next


def _train(corpus, loop_count=1000):
    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            f_keys.add(f)
    # defaulwt value provided as uniform probability)
    t = collections.defaultdict(_constant_factory(1/len(f_keys)))

    # loop
    for i in xrange(loop_count):
        count = collections.defaultdict(float)
        total = collections.defaultdict(float)
        s_total = collections.defaultdict(float)
        for (es, fs) in corpus:
            # compute normalization
            for e in es:
                s_total[e] = 0
                for f in fs:
                    s_total[e] += t[(e, f)]
            for e in es:
                for f in fs:
                    count[(e, f)] += t[(e, f)] / s_total[e]
                    total[f] += t[(e, f)] / s_total[e]
        # estimate probability
        for (e, f) in count.keys():
            t[(e, f)] = count[(e, f)] / total[f]
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
    #sent_pairs = [("day", "1 2"),
    #              ("after", "1 2 3")]
    t = train(sent_pairs, loop_count=0)
    pprint(t)
    t = train(sent_pairs, loop_count=1)
    pprint(t)
    t = train(sent_pairs, loop_count=2)
    pprint(t)
    t = train(sent_pairs, loop_count=3)
    pprint(t)
