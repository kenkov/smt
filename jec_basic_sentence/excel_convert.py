#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import xlrd
import sqlite3

# db setup
con = sqlite3.connect(":jec_basic:")
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
