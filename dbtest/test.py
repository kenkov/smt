#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import keitaiso
from smt.decoder.stackdecoder import stack_decoder


if __name__ == '__main__':
    sentence = u"I like him"
    #sentence = u"the tourism initiative addresses this\
    #    for the first time"
    db = "sqlite:///:test:"

    stacks = stack_decoder(sentence,
                           transfrom=2,
                           transto=1,
                           stacksize=10,
                           searchsize=10,
                           lang1method=keitaiso.str2wakati,
                           lang2method=lambda x: x,
                           db=db,
                           verbose=True)
    for i, stack in enumerate(stacks):
        print("STACK: {0}, len: {1}".format(i, len(stack)))
        #for item in stack:
        #    print(item)
    #print(dec)
    # search non-empty stack

    def search_nonempty_stack(stacks):
        for i, stack in reversed(list(enumerate(stacks))):
            if stack == set([]):
                continue
            else:
                return i, stack

    i, stack = search_nonempty_stack(stacks)
    print("non-empty stack is {0}".format(i))
    stack_lst = list(stack)
    mx = stack_lst[0]
    for item in stack_lst:
        #print(item)
        if item.prob_with_cost > mx.prob_with_cost:
            mx = item
    print(mx)
    print(u' '.join(mx.output_sentences))
