#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
import sqlite3
import keitaiso
from benchmarker import Benchmarker
from progressline import ProgressLine
#from operator import itemgetter
sys.path.append("../")
import ibmmodel2


def create_corpus():
    con = sqlite3.connect(":db:")
    cur = con.cursor()
    cur.execute("select * from jec_basic_sentence")
    sent_pairs = []
    for item in cur:
        #print(item[0].encode('utf-8'), item[1].encode('utf-8'))
        japanese = keitaiso.str2wakati(item[0])
        english = item[1]
        sent_pairs.append((japanese, english))
    con.close()
    return sent_pairs


def train_ibmmodel2():
    sent_pairs = create_corpus()
    t, a = ibmmodel2.train(sent_pairs, loop_count=100)
    return t, a


def benchmark_ibmmodel2():
    sent_pairs = create_corpus()
    with Benchmarker(width=20) as bm:
        with bm('loop_count=100, limit=1000'):
            t, a = ibmmodel2.train(sent_pairs, loop_count=100)


#for (reply, original), prob in sorted(t.items(),
#                                      key=itemgetter(1),
#                                      reverse=True):
#    print(u"{0} => {1} : {2}".format(reply, original, prob).encode('utf-8'))


con = sqlite3.connect(":db:")
cur = con.cursor()
# create table for word probability
try:
    cur.execute("drop table en2ja_ibmmodel2_wordprob")
except sqlite3.Error:
    print("en2ja_ibmmodel2_wordprob table does not exists.\
          creating a new table")
cur.execute("create table en2ja_ibmmodel2_wordprob\
            (ja TEXT, en TEXT, prob REAL)")
con.commit()
# create table for word alignment
try:
    cur.execute("drop table en2ja_ibmmodel2_wordalign")
except sqlite3.Error:
    print("en2ja_ibmmodel2_wordalign table does not exists.\
          creating a new table")
cur.execute("create table en2ja_ibmmodel2_wordalign\
            (en_pos INTEGER, ja_pos INTEGER,\
            en_len INTEGER, ja_len INTEGER, prob REAL)")
con.commit()

p = ProgressLine(0.12, title='now calculating...')
p.start()

t, a = train_ibmmodel2()
for (ja, en), prob in t.items():
    cur.execute("insert into en2ja_ibmmodel2_wordprob values (?, ?, ?)",
                (ja, en, prob))
for tpl, prob in a.items():
    cur.execute("insert into en2ja_ibmmodel2_wordalign values (?, ?, ?, ?, ?)",
                tpl + (prob,))
con.commit()
p.stop()
print("finished")
