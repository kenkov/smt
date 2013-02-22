#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
import sqlite3
import xlrd
sys.path.append("../")
from createdb import create_train_db
from createdb import create_phrase_db
from createdb import create_phrase_count_view
from createdb import create_phrase_prob


def excel_convert(db_name=":jec_basic:"):

    # db setup
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop table sentence")
    except sqlite3.Error:
        print("sentence table does not exists. creating a new table")

    cur.execute("create table sentence (ja TEXT, en TEXT)")
    con.commit()

    wb = xlrd.open_workbook("./JEC_basic_sentence_v1-2.xls")
    sheets = wb.sheets()
    s = sheets[0]

    for j in xrange(s.nrows):
        item = []
        for i in xrange(1, s.ncols - 1):
            item.append(s.cell(j, i).value)
        #print(item)
        cur.execute("insert into sentence values (?, ?)", tuple(item))
    con.commit()
    cur.close()


if __name__ == '__main__':
    pass
    # test
    #limit = 10
    #loop_count = 10
    #db_name = ":test:"
    #excel_convert(db_name=db_name)
    #create_train_db(trans="en2ja",
    #                db_name=db_name,
    #                limit=limit,
    #                loop_count=loop_count)
    #create_train_db(trans="ja2en",
    #                db_name=db_name,
    #                limit=limit,
    #                loop_count=loop_count)
    #create_phrase_db(db_name=db_name, limit=limit)
    #create_phrase_count_view(db_name=":test:")
    #create_phrase_prob(trans="en2ja", db_name=":jec_basic:")
