#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from progressline import ProgressLine
import xlrd

# import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, INTEGER
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Sentence(declarative_base()):
    __tablename__ = "sentence"
    id = Column(INTEGER, primary_key=True)
    target_sentence = Column(TEXT)
    source_sentence = Column(TEXT)


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
        for j in xrange(s.nrows):
            item = []
            for i in xrange(1, s.ncols - 1):
                item.append(s.cell(j, i).value)
            sentence = Sentence(target_sentence=item[0],
                                source_sentence=item[1])
            # add items
            session.add(sentence)
        session.commit()


def reverse_excel_convert(db="sqlite:///:memory:",
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
        for j in xrange(s.nrows):
            item = []
            for i in xrange(1, s.ncols - 1):
                item.append(s.cell(j, i).value)
            sentence = Sentence(target_sentence=item[1],
                                source_sentence=item[0])
            # add items
            session.add(sentence)
        session.commit()


if __name__ == "__main__":
    # new
    limit = None
    loop_count = 10000
    db = ":test:"
    excel_convert(db="sqlite:///{0}".format(db))
