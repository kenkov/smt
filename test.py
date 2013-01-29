#! /usr/bin/env python
# coding:utf-8

import unittest
from ibmmodel1 import train
from word_alignment import alignment


class WordAlignmentTest(unittest.TestCase):

    def test_alignment(self):
        elist = ["michael",
                 "assumes",
                 "that",
                 "he",
                 "will",
                 "stay",
                 "in",
                 "the",
                 "house"]
        flist = ["michael",
                 "geht",
                 "davon",
                 "aus",
                 ",",
                 "dass",
                 "er",
                 "im",
                 "haus",
                 "bleibt"]
        e2f = {(0, 0),
               (1, 1),
               (2, 1),
               (3, 1),
               (5, 2),
               (6, 3),
               (7, 6),
               (8, 8),
               (9, 5)}
        f2e = {(0, 0),
               (1, 1),
               (5, 2),
               (6, 3),
               (7, 6),
               (7, 7),
               (8, 8),
               (9, 4),
               (9, 5)}
        ans = {(0, 0),
               (1, 1),
               (2, 1),
               (3, 1),
               (5, 2),
               (6, 3),
               (7, 6),
               (7, 7),
               (8, 8),
               (9, 4),
               (9, 5)}
        self.assertEqual(alignment(elist, flist, e2f, f2e), ans)


class IBMModel1Test(unittest.TestCase):

    def _format(self, lst):
        return {(k, float('{:.4f}'.format(v))) for (k, v) in lst}

    def test_train(self):
        sent_pairs = [("the house", "das Haus"),
                      ("the book", "das Buch"),
                      ("a book", "ein Buch"),
                      ]
        t0 = train(sent_pairs, loop_count=0)
        t1 = train(sent_pairs, loop_count=1)
        t2 = train(sent_pairs, loop_count=2)

        loop0 = [(('house', 'Haus'), 0.25),
                 (('book', 'ein'), 0.25),
                 (('the', 'das'), 0.25),
                 (('the', 'Buch'), 0.25),
                 (('book', 'Buch'), 0.25),
                 (('a', 'ein'), 0.25),
                 (('book', 'das'), 0.25),
                 (('the', 'Haus'), 0.25),
                 (('house', 'das'), 0.25),
                 (('a', 'Buch'), 0.25)]

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
        self.assertEqual(self._format(t0.items()), self._format(loop0))
        self.assertEqual(self._format(t1.items()), self._format(loop1))
        self.assertEqual(self._format(t2.items()), self._format(loop2))


if __name__ == '__main__':
    unittest.main()
