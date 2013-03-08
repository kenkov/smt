#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import unittest
from smt.langmodel.ngram import ngram
from smt.langmodel.ngram import NgramException


class NgramTest(unittest.TestCase):
    def test_ngram_3(self):
        sentence = ["I am teacher",
                    "I am",
                    "I",
                    ""]
        test_sentences = (["</s>", "<s>"] + item.split() + ["</s>"]
                          for item in sentence)
        anss = [[("</s>", "<s>", "I"),
                 ("<s>", "I", "am"),
                 ("I", "am", "teacher"),
                 ("am", "teacher", "</s>")],
                [("</s>", "<s>", "I"),
                 ("<s>", "I", "am"),
                 ("I", "am", "</s>")],
                [("</s>", "<s>", "I"),
                 ("<s>", "I", "</s>")],
                [("</s>", "<s>", "</s>")],
                ]

        for sentences, ans in zip(test_sentences, anss):
            a = ngram(sentences, 3)
            self.assertEqual(list(a), ans)

    def test_ngram_illegal_input(self):
        sentences = ["I", "am"]
        self.assertRaises(NgramException, ngram, sentences, 3)


if __name__ == '__main__':
    unittest.main()
