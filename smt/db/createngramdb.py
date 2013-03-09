#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import collections
# import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, TEXT, INTEGER
from sqlalchemy.orm import sessionmaker
# smt
from smt.db.createdb import Sentence
from smt.langmodel.ngram import ngram


def _create_ngram_count_db(lang, langmethod=lambda x: x,
                           n=3, db="sqilte:///:memory:"):
    engine = create_engine(db)
    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Sentence)

    ngram_dic = collections.defaultdict(float)
    for item in query:
        if lang == 1:
            sentences = langmethod(item.lang1).split()
        elif lang == 2:
            sentences = langmethod(item.lang2).split()
        sentences = ["</s>", "<s>"] + sentences + ["</s>"]
        ngrams = ngram(sentences, n)
        for tpl in ngrams:
            ngram_dic[tpl] += 1

    return ngram_dic


def create_ngram_count_db(lang, langmethod=lambda x: x,
                          n=3, db="sqilte:///:memory:"):
    engine = create_engine(db)
    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    class Trigram(declarative_base()):
        __tablename__ = 'lang{}trigram'.format(lang)
        id = Column(INTEGER, primary_key=True)
        first = Column(TEXT)
        second = Column(TEXT)
        third = Column(TEXT)
        count = Column(INTEGER)
    # create table
    Trigram.__table__.drop(engine, checkfirst=True)
    Trigram.__table__.create(engine)

    ngram_dic = _create_ngram_count_db(lang, langmethod=langmethod, n=n, db=db)

    # insert items
    for (first, second, third), count in ngram_dic.items():
        print(u"inserting {}, {}, {}".format(first, second, third))
        item = Trigram(first=first,
                       second=second,
                       third=third,
                       count=count)
        session.add(item)
    session.commit()


if __name__ == '__main__':
    pass
