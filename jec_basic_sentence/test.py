#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
sys.path.append("../")
import keitaiso
from smt.decoder.stackdecoder import stack_decoder


if __name__ == '__main__':
    #sentence = u"He teaches English".split()
    sentence = u"He will go abroad".split()
    db = "sqlite:///:test:"
    stacks = stack_decoder(sentence,
                           transfrom=2,
                           transto=1,
                           stacksize=10,
                           lang1method=keitaiso.str2wakati,
                           lang2method=lambda x: x,
                           db=db)
    for i, stack in enumerate(stacks):
        print("STACK: {0}, len: {1}".format(i, len(stack)))
        #for item in stack:
        #    print(item)
    #print(dec)
    stack = stacks[3]
    stack_lst = list(stack)
    mx = stack_lst[0]
    for item in stack_lst:
        #print(item)
        if item.prob > mx.prob:
            mx = item
    print(mx)
    print(u' '.join(mx.output_sentences))
