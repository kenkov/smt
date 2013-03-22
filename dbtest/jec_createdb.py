#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from progressline import ProgressLine
import xlrd
from smt.db.createdb import createdb

# import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, REAL, INTEGER

# import smt module
import smt.db.tables as tables
import math

Sentence = tables.Tables().get_sentence_table()


def excel_convert(db="sqlite:///:memory:",
                  excel_file="./JEC_basic_sentence_v1-2.xls"):
    engine = create_engine(db)
    # first, remove table
    Sentence.__table__.drop(engine, checkfirst=True)
    # create table
    Sentence.__table__.create(engine)
    print("created table: sentence")

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    # get sentence from excel file
    wb = xlrd.open_workbook(excel_file)
    sheets = wb.sheets()
    s = sheets[0]

    with ProgressLine(title="inserting items..."):
        #
        # set 10 rows for test
        #
        for j in range(s.nrows)[:3]:
            item = []
            for i in xrange(1, s.ncols - 1):
                item.append(s.cell(j, i).value)
            sentence = Sentence(lang1=item[0], lang2=item[1])
            # add items
            session.add(sentence)
        session.commit()


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
    # test
    import keitaiso
    # new
    limit = None
    loop_count = 10
    db = ":test:"
    excel_convert(db="sqlite:///{0}".format(db))
    createdb(db=db,
             lang1method=keitaiso.str2wakati,
             init_val=1.0e-10,
             limit=limit,
             loop_count=loop_count,
             )
