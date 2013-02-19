#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sqlite3
import sys
import collections
from pprint import pprint
sys.path.append("../")
import ibmmodel2
import word_alignment
import keitaiso
import phrase_extract


def db_viterbi_alignment(es, fs, trans, db_name=":db:", init_val=0.00001):

    def get_wordprob(e, f, trans, db_name=":db:"):
        table_name = trans + "_wordprob"
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from {0}\
                    where to_=? and from_=?'.format(table_name),
                    (e, f))
        res = list(cur)
        return res[0][0] if res else init_val

    def get_wordalign(i, j, l_e, l_f, trans, db_name=":db:",
                      init_val=0.00001):
        table_name = trans + "_wordalign"
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from {0}\
                    where\
                    from_pos=? and\
                    to_pos=? and\
                    to_len=? and\
                    from_len=?'.format(table_name),
                    (i, j, l_e, l_f))
        res = list(cur)
        return res[0][0] if res else init_val

    # algorithm
    max_a = collections.defaultdict(float)
    l_e = len(es)
    l_f = len(fs)
    for (j, e) in enumerate(es, 1):
        current_max = (0, -1)
        for (i, f) in enumerate(fs, 1):
            val = get_wordprob(e, f, db_name=db_name, trans=trans) *\
                get_wordalign(i, j, l_e, l_f, db_name=db_name,
                              trans=trans)
            # select the first one among the maximum candidates
            if current_max[1] < val:
                current_max = (i, val)
        max_a[j] = current_max[0]
    return max_a


def db_show_matrix(es, fs, trans, db_name=":db:"):
    '''
    print matrix according to viterbi alignment like
          fs
     -------------
    e|           |
    s|           |
     |           |
     -------------
    >>> sent_pairs = [("僕 は 男 です", "I am a man"),
                      ("私 は 女 です", "I am a girl"),
                      ("私 は 先生 です", "I am a teacher"),
                      ("彼女 は 先生 です", "She is a teacher"),
                      ("彼 は 先生 です", "He is a teacher"),
                      ]
    >>> t, a = train(sent_pairs, loop_count=1000)
    >>> args = ("私 は 先生 です".split(), "I am a teacher".split(), t, a)
    |x| | | |
    | | |x| |
    | | | |x|
    | | |x| |
    '''
    max_a = db_viterbi_alignment(es, fs, trans=trans,
                                 db_name=db_name).items()
    m = len(es)
    n = len(fs)
    return ibmmodel2.matrix(m, n, max_a)


def db_symmetrization(es, fs, db_name=":db:"):
    '''
    translation from English to Japanese
    en: Japanese
    fs: English
    '''
    f2e = db_viterbi_alignment(es, fs, trans="en2ja",
                               db_name=db_name).items()
    e2f = db_viterbi_alignment(fs, es, trans="ja2en",
                               db_name=db_name).items()
    return word_alignment.alignment(es, fs, e2f, f2e)


if __name__ == "__main__":

    ja = keitaiso.str2wakati(u"人生とは何ですか")
    en = u"what is life"
    args = (ja.split(), en.split())
    print(db_show_matrix(*args, trans="en2ja", db_name=":jec_basic:"))

    alignment = db_symmetrization(*args,
                                  db_name=":jec_basic:")
    ext = phrase_extract.phrase_extract(args[0], args[1], alignment)
    pprint(ext)
    for e, f in ext:
        print(' '.join(e), "<->", ' '.join(f))
