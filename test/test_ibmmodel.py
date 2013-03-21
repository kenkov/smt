#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import unittest
import collections
import keitaiso
from smt.ibmmodel.ibmmodel1 import train
from smt.ibmmodel.ibmmodel2 import viterbi_alignment
import smt.ibmmodel.ibmmodel2 as ibmmodel2


class IBMModel1Test(unittest.TestCase):

    def _format(self, lst):
        return {(k, float('{:.4f}'.format(v))) for (k, v) in lst}

    def test_train(self):
        sent_pairs = [("the house", "das Haus"),
                      ("the book", "das Buch"),
                      ("a book", "ein Buch"),
                      ]
        #t0 = train(sent_pairs, loop_count=0)
        t1 = train(sent_pairs, loop_count=1)
        t2 = train(sent_pairs, loop_count=2)

        #loop0 = [(('house', 'Haus'), 0.25),
        #         (('book', 'ein'), 0.25),
        #         (('the', 'das'), 0.25),
        #         (('the', 'Buch'), 0.25),
        #         (('book', 'Buch'), 0.25),
        #         (('a', 'ein'), 0.25),
        #         (('book', 'das'), 0.25),
        #         (('the', 'Haus'), 0.25),
        #         (('house', 'das'), 0.25),
        #         (('a', 'Buch'), 0.25)]

        loop1 = [(('house', 'Haus'), 0.5),
                 (('book', 'ein'), 0.5),
                 (('the', 'das'), 0.5),
                 (('the', 'Buch'), 0.25),
                 (('book', 'Buch'), 0.5),
                 (('a', 'ein'), 0.5),
                 (('book', 'das'), 0.25),
                 (('the', 'Haus'), 0.5),
                 (('house', 'das'), 0.25),
                 (('a', 'Buch'), 0.25)]
        loop2 = [(('house', 'Haus'), 0.5714),
                 (('book', 'ein'), 0.4286),
                 (('the', 'das'), 0.6364),
                 (('the', 'Buch'), 0.1818),
                 (('book', 'Buch'), 0.6364),
                 (('a', 'ein'), 0.5714),
                 (('book', 'das'), 0.1818),
                 (('the', 'Haus'), 0.4286),
                 (('house', 'das'), 0.1818),
                 (('a', 'Buch'), 0.1818)]
        # assertion
        # next assertion doesn't make sence because
        # initialized by defaultdict
        #self.assertEqual(self._format(t0.items()), self._format(loop0))
        self.assertEqual(self._format(t1.items()), self._format(loop1))
        self.assertEqual(self._format(t2.items()), self._format(loop2))


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

    def test_zero_division_error(self):
        """
        at the beginning, there was this bug for ZeroDivisionError,
        so this test was created to check that
        """
        sentence = [(u"Xではないかとつくづく疑問に思う",
                     u"I often wonder if it might be X."),
                    (u"Xがいいなといつも思います",
                     u"I always think X would be nice."),
                    (u"それがあるようにいつも思います",
                     u"It always seems like it is there."),
                    ]
        sentences = [(keitaiso.str2wakati(s1), s2) for
                     s1, s2 in sentence]

        self.assertRaises(ZeroDivisionError,
                          ibmmodel2.train,
                          sentences, loop_count=1000)


if __name__ == '__main__':
    unittest.main()
