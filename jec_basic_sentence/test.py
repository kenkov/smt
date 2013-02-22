#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
sys.path.append("../")
import decode


if __name__ == '__main__':
    fs = u"He teaches studies English".split()
    db_name = ":jec_basic:"
    dec = decode.stack_decoder(fs, db_name)
    dec = [list(item) for item in list(dec)]
    print(dec)
    mx = dec[-1][0]
    for item in dec[-1]:
        if item.prob > mx.prob:
            mx = item
    print(mx)
