#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from progressline import ProgressLine
import xlrd
from smt.db.createdb import createdb

# import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import smt module
from smt.db.createdb import Sentence


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
            sentence = Sentence(lang1=item[0], lang2=item[1])
            # add items
            session.add(sentence)
        session.commit()


if __name__ == '__main__':
    pass
    # test
    '''
    limit = 10
    loop_count = 10
    db_name = ":test:"
    excel_convert(db_name=db_name)
    create_train_db(trans="en2ja",
                    db_name=db_name,
                    limit=limit,
                    loop_count=loop_count)
    create_train_db(trans="ja2en",
                    db_name=db_name,
                    limit=limit,
                    loop_count=loop_count)
    create_phrase_db(db_name=db_name, limit=limit)
    create_phrase_count_view(db_name=":test:")
    create_phrase_prob(trans="en2ja", db_name=":jec_basic:")
    '''
    import keitaiso
    # new
    limit = None
    loop_count = 1000
    db = ":test:"
    excel_convert(db="sqlite:///{0}".format(db))
    createdb(db=db,
             lang1method=keitaiso.str2wakati,
             init_val=1.0e-10,
             )
