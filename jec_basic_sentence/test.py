#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from pprint import pprint
import sys
sys.path.append("../")
import decode


if __name__ == '__main__':
    e = u"I"
    f = u"は"
    prob = decode.phrase_prob(e, f, trans="en2ja", db_name=":jec_basic:")
    pprint(prob)
