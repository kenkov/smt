#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import keitaiso
from smt.db.createngramdb import create_ngram_db


if __name__ == '__main__':
    db = "sqlite:///:jec_log_basic:"
    lang = 1
    langmethod = keitaiso.str2wakati
    n = 3
    create_ngram_db(lang=lang,
                    langmethod=langmethod,
                    n=n,
                    db=":jec_log_basic:")
