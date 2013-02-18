#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import xlrd
import sqlite3

# db setup
con = sqlite3.connect(":db:")
cur = con.cursor()
try:
    cur.execute("drop table jec_basic_sentence")
except sqlite3.Error:
    print("jec_basic_sentence table does not exists. creating a new table")

cur.execute("create table jec_basic_sentence (japanese TEXT, english TEXT)")
con.commit()

wb = xlrd.open_workbook("./JEC_basic_sentence_v1-2.xls")
sheets = wb.sheets()
s = sheets[0]

for j in xrange(s.nrows):
    item = []
    for i in xrange(1, s.ncols - 1):
        item.append(s.cell(j, i).value)
    #print(item)
    cur.execute("insert into jec_basic_sentence values (?, ?)", tuple(item))

con.commit()
cur.close()
