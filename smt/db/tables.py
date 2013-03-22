#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
# import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, REAL, INTEGER


class Tables(object):

    def get_sentence_table(tablename="sentence"):

        class Sentence(declarative_base()):
            __tablename__ = tablename
            id = Column(INTEGER, primary_key=True)
            lang1 = Column(TEXT)
            lang2 = Column(TEXT)

        return Sentence

    def get_wordprobability_table(tablename):

        class WordProbability(declarative_base()):
            __tablename__ = tablename
            id = Column(INTEGER, primary_key=True)
            transto = Column(TEXT)
            transfrom = Column(TEXT)
            prob = Column(REAL)

        return WordProbability

    def get_wordalignment_table(tablename):

        class WordAlignment(declarative_base()):
            __tablename__ = tablename
            id = Column(INTEGER, primary_key=True)
            from_pos = Column(INTEGER)
            to_pos = Column(INTEGER)
            to_len = Column(INTEGER)
            from_len = Column(INTEGER)
            prob = Column(REAL)

        return WordAlignment

    def get_phrase_table(tablename):

        class Phrase(declarative_base()):
            __tablename__ = tablename
            id = Column(INTEGER, primary_key=True)
            lang1p = Column(TEXT)
            lang2p = Column(TEXT)

        return Phrase

    def get_transphraseprob_table(tablename):

        class TransPhraseProb(declarative_base()):
            __tablename__ = tablename
            id = Column(INTEGER, primary_key=True)
            lang1p = Column(TEXT)
            lang2p = Column(TEXT)
            p1_2 = Column(REAL)
            p2_1 = Column(REAL)

        return TransPhraseProb
