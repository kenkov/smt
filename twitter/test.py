#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
import sqlite3
import keitaiso
from operator import itemgetter
import re
sys.path.append("../")
import ibmmodel2


def text_filter(text):
    re_objs = [r'(http|https)://[a-zA-Z0-9-./"#$%&\':?=_]+',
               u' |　|\t|\n|\r', u'@\w+']
    for reg in re_objs:
        re_obj = re.compile(reg)
        text = re_obj.sub(u'', text)
    return text


con = sqlite3.connect(":twitter:")
cur = con.cursor()
cur.execute("select * from conversation limit 100")
sent_pairs = []
for item in cur:
    filter_item = map(text_filter, item)
    original, reply = map(
        keitaiso.str2wakati,
        filter_item)
    sent_pairs.append((reply, original))

t, a = ibmmodel2.train(sent_pairs, loop_count=100)
for (reply, original), prob in sorted(t.items(),
                                      key=itemgetter(1),
                                      reverse=True):
    print(u"{0} => {1} : {2}".format(reply, original, prob).encode('utf-8'))
