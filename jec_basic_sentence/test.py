#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sqlite3
import sys
import collections
sys.path.append("../")
import ibmmodel2
import keitaiso


def db_viterbi_alignment(es, fs, db_name=":db:", init_val=0.00001):

    def get_wordprob(e, f, db_name=":db:"):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from en2ja_ibmmodel2_wordprob\
                    where en=? and ja=?',
                    (e, f))
        res = list(cur)
        return res[0][0] if res else init_val

    def get_wordalign(i, j, l_e, l_f, db_name=":db:", init_val=0.00001):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from en2ja_ibmmodel2_wordalign\
                    where\
                    en_pos=? and\
                    ja_pos=? and\
                    en_len=? and\
                    ja_len=?',
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
            val = get_wordprob(e, f) * get_wordalign(i, j, l_e, l_f)
            # select the first one among the maximum candidates
            if current_max[1] < val:
                current_max = (i, val)
        max_a[j] = current_max[0]
    return max_a


def db_show_matrix(es, fs, db_name=":db:"):
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
    max_a = db_viterbi_alignment(es, fs, db_name=db_name).items()
    m = len(es)
    n = len(fs)
    return ibmmodel2.matrix(m, n, max_a)


if __name__ == "__main__":

    ja = keitaiso.str2wakati(u"元気ですか")
    en = u"Are you fine"
    args = (ja.split(), en.split())
    print(db_show_matrix(*args))
