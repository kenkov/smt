#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function

# import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, REAL, INTEGER

# import smt module
import math


class TransPhraseProb(declarative_base()):
    __tablename__ = "phraseprob"
    id = Column(INTEGER, primary_key=True)
    lang1p = Column(TEXT)
    lang2p = Column(TEXT)
    p1_2 = Column(REAL)
    p2_1 = Column(REAL)


def convert_to_log_prob(dbfrom="sqlite:///:memory:",
                        dbto="sqlite:///:memory:"):
    fromengine = create_engine(dbfrom)
    # create session
    FromSession = sessionmaker(bind=fromengine)
    fromsession = FromSession()
    query = fromsession.query(TransPhraseProb)

    toengine = create_engine(dbto)
    # first, remove table
    TransPhraseProb.__table__.drop(toengine, checkfirst=True)
    # create table
    TransPhraseProb.__table__.create(toengine)
    print("create phraseprob table for log")
    # create session
    ToSession = sessionmaker(bind=toengine)
    tosession = ToSession()
    tosession.add_all(TransPhraseProb(lang1p=item.lang1p,
                                      lang2p=item.lang2p,
                                      p1_2=math.log(item.p1_2),
                                      p2_1=math.log(item.p2_1),
                                      )
                      for item in query)
    tosession.commit()


if __name__ == '__main__':
    """
    # test
    import keitaiso
    # new
    limit = None
    loop_count = 10000
    db = ":test:"
    excel_convert(db="sqlite:///{0}".format(db))
    createdb(db=db,
             lang1method=keitaiso.str2wakati,
             init_val=1.0e-10,
             limit=limit,
             loop_count=loop_count,
             )
    """
    convert_to_log_prob(dbfrom="sqlite:///:phrasetwitter:",
                        dbto="sqlite:///:log_twitter:")
