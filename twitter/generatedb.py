#! /usr/bin/env python
# coding:utf-8

#
# Last Updated on 2012/04/20 03:38:36 .
#
import sqlite3


def _to_dict(tup):
    return {u"id": tup[0],
            u"text": tup[1],
            u"created_at": tup[2],
            u"screen_name": tup[3],
            u"in_reply_to_status_id": tup[4],
            u"in_reply_to_screen_name": tup[5],
            }


def create_reply_view(twitterdb):
    # reply ありのツイートのテーブルを作成
    con = sqlite3.connect(twitterdb)
    cur = con.cursor()
    try:
        cur.execute("drop view reply")
    except sqlite3.Error:
        print "reply view does not exists. creating a new view"

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
        print "conversation table doesn't exist.\
               \nNow creating a new conversation table."
    cur.execute("create table conversation (original TEXT, reply TEX)")
    cur.close()
    # search replies
    ins_cur = con.cursor()
    cur = con.cursor()
    cur.execute("select * from reply")
    for item in cur:
        c = con.cursor()
        c.execute("select * from twitter where id=?",
                  (_to_dict(item)["in_reply_to_status_id"],))
        for to_item in c:
            #print u"{_from}\n   {to}".format(_from=_to_dict(to_item)["text"],
            #                                 to=_to_dict(item)["text"])
            ins_cur.execute("insert into conversation values (?, ?)",
                            (_to_dict(to_item)["text"],
                             _to_dict(item)["text"]))
    con.commit()
    ins_cur.close()

if __name__ == "__main__":
    create_reply_view(":twitter:")
    reply_search()
