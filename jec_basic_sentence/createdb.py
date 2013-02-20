#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
sys.path.append("../")
from create_train_db import create_train_db
from create_phrase_db import create_phrase_db
from create_phrase_db import create_phrase_count_view


if __name__ == '__main__':
    #create_train_db(trans="en2ja",
    #                db_name=":jec_basic:",
    #                limit=None,
    #                loop_count=1000)
    #create_train_db(trans="ja2en",
    #                db_name=":jec_basic:",
    #                limit=None,
    #                loop_count=1000)
    #create_phrase_db.create_phrase_db(db_name=":jec_basic:", limit=None)
    create_phrase_count_view(db_name=":jec_basic:")
