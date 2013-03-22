#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import unittest
import collections
#import keitaiso
from smt.ibmmodel.ibmmodel1 import train
from smt.ibmmodel.ibmmodel2 import viterbi_alignment
#import smt.ibmmodel.ibmmodel2 as ibmmodel2
import decimal
from decimal import Decimal as D

# set deciaml context
decimal.getcontext().prec = 4
decimal.getcontext().rounding = decimal.ROUND_HALF_UP


class IBMModel1Test(unittest.TestCase):

    #def _format(self, lst):
    #    return {(k, float('{:.4f}'.format(v))) for (k, v) in lst}

    def test_train_loop1(self):
        sent_pairs = [("the house", "das Haus"),
                      ("the book", "das Buch"),
                      ("a book", "ein Buch"),
                      ]
        #t0 = train(sent_pairs, loop_count=0)
        t1 = train(sent_pairs, loop_count=1)

        loop1 = [(('house', 'Haus'), D("0.5")),
                 (('book', 'ein'), D("0.5")),
                 (('the', 'das'), D("0.5")),
                 (('the', 'Buch'), D("0.25")),
                 (('book', 'Buch'), D("0.5")),
                 (('a', 'ein'), D("0.5")),
                 (('book', 'das'), D("0.25")),
                 (('the', 'Haus'), D("0.5")),
                 (('house', 'das'), D("0.25")),
                 (('a', 'Buch'), D("0.25"))]
        # assertion
        # next assertion doesn't make sence because
        # initialized by defaultdict
        #self.assertEqual(self._format(t0.items()), self._format(loop0))
        self.assertEqual(set(t1.items()), set(loop1))

    def test_train_loop2(self):
        sent_pairs = [("the house", "das Haus"),
                      ("the book", "das Buch"),
                      ("a book", "ein Buch"),
                      ]
        #t0 = train(sent_pairs, loop_count=0)
        t2 = train(sent_pairs, loop_count=2)

        loop2 = [(('house', 'Haus'), D("0.5713")),
                 (('book', 'ein'), D("0.4284")),
                 (('the', 'das'), D("0.6367")),
                 (('the', 'Buch'), D("0.1818")),
                 (('book', 'Buch'), D("0.6367")),
                 (('a', 'ein'), D("0.5713")),
                 (('book', 'das'), D("0.1818")),
                 (('the', 'Haus'), D("0.4284")),
                 (('house', 'das'), D("0.1818")),
                 (('a', 'Buch'), D("0.1818"))]
        # assertion
        # next assertion doesn't make sence because
        # initialized by defaultdict
        #self.assertEqual(self._format(t0.items()), self._format(loop0))
        self.assertEqual(set(t2.items()), set(loop2))


class IBMModel2Test(unittest.TestCase):

    def test_viterbi_alignment(self):
        x = viterbi_alignment([1, 2, 1],
                              [2, 3, 2],
                              collections.defaultdict(int),
                              collections.defaultdict(int))
        # Viterbi_alignment selects the first token
        # if t or a doesn't contain the key.
        # This means it returns NULL token
        # in such a situation.
        self.assertEqual(x, {1: 1, 2: 1, 3: 1})

    #def test_zero_division_error(self):
    #    """
    #    at the beginning, there was this bug for ZeroDivisionError,
    #    so this test was created to check that
    #    """
    #    sentence = [(u"Xではないかとつくづく疑問に思う",
    #                 u"I often wonder if it might be X."),
    #                (u"Xがいいなといつも思います",
    #                 u"I always think X would be nice."),
    #                (u"それがあるようにいつも思います",
    #                 u"It always seems like it is there."),
    #                ]
    #    sentences = [(keitaiso.str2wakati(s1), s2) for
    #                 s1, s2 in sentence]

    #    self.assertRaises(decimal.DivisionByZero,
    #                      ibmmodel2.train,
    #                      sentences, loop_count=1000)


if __name__ == '__main__':
    unittest.main()
