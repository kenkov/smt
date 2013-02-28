#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import re
import sqlite3
from progressline import ProgressLine
# import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import smt module
from smt.db.createdb import Sentence
from smt.db.createdb import createdb


def _to_dict(tup):
    return {u"id": tup[0],
            u"text": tup[1],
            u"created_at": tup[2],
            u"screen_name": tup[3],
            u"in_reply_to_status_id": tup[4],
            u"in_reply_to_screen_name": tup[5],
            }


def create_reply_view(db=":twitter:"):
    # reply ありのツイートのテーブルを作成
    con = sqlite3.connect(db)
    cur = con.cursor()
    try:
        cur.execute("drop view reply")
    except sqlite3.Error:
        print("reply view does not exists. creating a new view")

    cur.execute("create view reply as select * from twitter \
                where in_reply_to_status_id is not null")
    con.commit()
    cur.close()


def reply_search(db=":twitter:"):
    con = sqlite3.connect(db)
    # create conversation table
    cur = con.cursor()
    try:
        cur.execute("drop table conversation")
    except sqlite3.Error:
        print("conversation table doesn't exist.\
              \nNow creating a new conversation table.")
    cur.execute("create table conversation (original TEXT, reply TEX)")
    cur.close()
    # search replies
    ins_cur = con.cursor()
    cur = con.cursor()
    cur.execute("select * from reply")
    with ProgressLine(0.12, title='Inserting items into {0} table...'.format(
            "conversatoin")):
        for item in cur:
            c = con.cursor()
            c.execute("select * from twitter where id=?",
                      (_to_dict(item)["in_reply_to_status_id"],))
            for to_item in c:
                ins_cur.execute("insert into conversation values (?, ?)",
                                (_to_dict(to_item)["text"],
                                 _to_dict(item)["text"]))
        con.commit()
        ins_cur.close()


def text_filter(text):
    re_objs = [r'(http|https)://[a-zA-Z0-9-./"#$%&\':?=_]+',
               u' |　|\t|\n|\r', u'@\w+']
    for reg in re_objs:
        re_obj = re.compile(reg)
        text = re_obj.sub(u'', text)
    return text


def create_sentence_db(db="sqlite:///:phrasetwitter:"):
    engine = create_engine(db)
    # first, remove table
    Sentence.__table__.drop(engine, checkfirst=True)
    # create table
    Sentence.__table__.create(engine)
    print("created table: sentence")

    con = sqlite3.connect(":twitter:")
    cur = con.cursor()
    cur.execute("select original, reply from conversation")

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    with ProgressLine(title="inserting items into sentence..."):
        for item in cur:
            origin, reply = map(text_filter, item)
            newitem = Sentence(lang1=reply, lang2=origin)
            session.add(newitem)
            session.commit()
        session.commit()


if __name__ == "__main__":
    #create_reply_view(db=":twitter:")
    #reply_search(db=":twitter:")

    import keitaiso
    # new
    limit = None
    loop_count = 1000
    db = ":phrasetwitter:"
    #create_sentence_db(db="sqlite:///{0}".format(db))
    createdb(db=db,
             lang1method=keitaiso.str2wakati,
             lang2method=keitaiso.str2wakati,
             init_val=1.0e-10,
             limit=limit,
             loop_count=loop_count,
             )
