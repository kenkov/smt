#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
import sqlite3
import keitaiso
#from benchmarker import Benchmarker
from progressline import ProgressLine
#from operator import itemgetter
sys.path.append("../")
import ibmmodel2


def create_corpus(trans, db_name=":db:", limit=None):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    if trans == "en2ja":
        if limit:
            cur.execute("select ja, en from sentence limit ?",
                        (limit,))
        else:
            cur.execute("select ja, en from sentence")
    elif trans == "ja2en":
        if limit:
            cur.execute("select en, ja from sentence limit ?",
                        (limit,))
        else:
            cur.execute("select en, ja from sentence")
    else:
        raise Exception("Please select en2ja or ja2en for limit argument")

    sent_pairs = []
    # use keitaiso.str2wakati for Japanese
    # use identity function for English
    if trans == "en2ja":
        _to_func = keitaiso.str2wakati
        _from_func = lambda x: x
    elif trans == "ja2en":
        _to_func = lambda x: x
        _from_func = keitaiso.str2wakati

    for item in cur:
        _to = _to_func(item[0])
        _from = _from_func(item[1])
        sent_pairs.append((_to, _from))

    con.close()
    return sent_pairs


#def benchmark_ibmmodel2():
#    sent_pairs = create_corpus()
#    with Benchmarker(width=20) as bm:
#        with bm('loop_count=100, limit=1000'):
#            t, a = ibmmodel2.train(sent_pairs, loop_count=100)


def create_train_db(trans, db_name=":db:", limit=None, loop_count=1000):

    if not trans in ["en2ja", "ja2en"]:
        raise Exception("please select en2ja or ja2en for trans argmument")

    table_prefix = trans + "_"
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # create table for word probability
    prob_tablename = table_prefix + "wordprob"
    try:
        cur.execute("drop table {0}".format(prob_tablename))
    except sqlite3.Error:
        print("{0} table does not exists.\
              creating a new table".format(prob_tablename))
    cur.execute("create table {0}\
                (to_ TEXT, from_ TEXT, prob REAL)".format(prob_tablename))
    con.commit()

    # create table for word alignment
    align_tablename = table_prefix + "wordalign"
    try:
        cur.execute("drop table {0}".format(align_tablename))
    except sqlite3.Error:
        print("{0} table does not exists.\
              creating a new table".format(align_tablename))
    cur.execute("create table {0}\
                (from_pos INTEGER, to_pos INTEGER,\
                to_len INTEGER, from_len INTEGER, prob\
                REAL)".format(align_tablename))
    con.commit()

    # IBM learning
    p = ProgressLine(0.12, title='IBM Model learning...')
    p.start()
    t, a = ibmmodel2.train(sent_pairs=create_corpus(trans,
                                                    db_name=db_name,
                                                    limit=limit),
                           loop_count=loop_count)
    p.stop()
    # insert
    p = ProgressLine(0.12, title='inserting items into database')
    for (_to, _from), prob in t.items():
        cur.execute("insert into {0}\
                     values (?, ?, ?)".format(prob_tablename),
                    (_to, _from, prob))
    for tpl, prob in a.items():
        cur.execute("insert into {0} values\
                    (?, ?, ?, ?, ?)".format(align_tablename),
                    tpl + (prob,))
    con.commit()
    p.stop()

if __name__ == "__main__":

    create_train_db(trans="en2ja",
                    db_name=":jec_basic:",
                    limit=None,
                    loop_count=100)
    create_train_db(trans="ja2en",
                    db_name=":jec_basic:",
                    limit=None,
                    loop_count=100)
