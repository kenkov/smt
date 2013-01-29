#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from operator import itemgetter
import collections
from pprint import pprint
import ibmmodel1


class _keydefaultdict(collections.defaultdict):
    '''define a local function for uniform probability initialization'''
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            ret = self[key] = self.default_factory(key)
            return ret


def _train(corpus, loop_count=1000):
    f_keys = set()
    for (es, fs) in corpus:
        for f in fs:
            f_keys.add(f)
    # initialize t
    t = ibmmodel1._train(corpus, loop_count)
    # default value provided as uniform probability)

    def key_fun(key):
        ''' default_factory function for keydefaultdict '''
        i, j, l_e, l_f = key
        return 1 / (l_f + 1)
    a = _keydefaultdict(key_fun)

    # loop
    for _i in xrange(loop_count):
        # variables for estimating t
        count = collections.defaultdict(float)
        total = collections.defaultdict(float)
        # variables for estimating a
        count_a = collections.defaultdict(float)
        total_a = collections.defaultdict(float)

        s_total = collections.defaultdict(float)
        for (es, fs) in corpus:
            l_e = len(es)
            l_f = len(fs)
            # compute normalization
            for (j, e) in enumerate(es, 1):
                s_total[e] = 0
                for (i, f) in enumerate(fs, 1):
                    s_total[e] += t[(e, f)] * a[(i, j, l_e, l_f)]
            # collect counts
            for (j, e) in enumerate(es, 1):
                for (i, f) in enumerate(fs, 1):
                    c = t[(e, f)] * a[(i, j, l_e, l_f)] / s_total[e]
                    count[(e, f)] += c
                    total[f] += c
                    count_a[(i, j, l_e, l_f)] += c
                    total_a[(j, l_e, l_f)] += c
        # estimate probability
        for (e, f) in count.keys():
            t[(e, f)] = count[(e, f)] / total[f]
        for (i, j, l_e, l_f) in count_a.keys():
            a[(i, j, l_e, l_f)] = count_a[(i, j, l_e, l_f)] / \
                total_a[(j, l_e, l_f)]
    return (t, a)


def train(sent_pairs, loop_count=1000):
    corpus = [(es.split(), fs.split()) for (es, fs) in sent_pairs]
    return _train(corpus, loop_count)


def _pprint(tbl):
    for (e, f), v in sorted(tbl.items(), key=itemgetter(1), reverse=True):
        print("p({e}|{f}) = {v}".format(e=e, f=f, v=v))


if __name__ == '__main__':
    sent_pairs = [("the house", "das Haus"),
                  ("the book", "das Buch"),
                  ("a book", "ein Buch"),
                  ]
    #sent_pairs = [("day", "1 2"),
    #              ("after", "1 2")]
    t = train(sent_pairs, loop_count=0)
    pprint(t)
    t = train(sent_pairs, loop_count=1)
    pprint(t)
    t = train(sent_pairs, loop_count=2)
    pprint(t)
    t = train(sent_pairs, loop_count=3)
    pprint(t)
