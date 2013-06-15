#! /usr/bin/env python
# coding:utf-8

import unittest
from smt.phrase.word_alignment import _alignment
from smt.phrase.word_alignment import symmetrization
from smt.phrase.phrase_extract import extract
from smt.phrase.phrase_extract import phrase_extract
from smt.phrase.phrase_extract import available_phrases
from smt.utils.utility import mkcorpus


class WordAlignmentTest(unittest.TestCase):

    def test_alignment(self):
        elist = "michael assumes that he will stay in the house".split()
        flist = "michael geht davon aus , dass er im haus bleibt".split()
        e2f = [(1, 1), (2, 2), (2, 3), (2, 4), (3, 6),
               (4, 7), (7, 8), (9, 9), (6, 10)]
        f2e = [(1, 1), (2, 2), (3, 6), (4, 7), (7, 8),
               (8, 8), (9, 9), (5, 10), (6, 10)]
        ans = set([(1, 1),
                   (2, 2),
                   (2, 3),
                   (2, 4),
                   (3, 6),
                   (4, 7),
                   (5, 10),
                   (6, 10),
                   (7, 8),
                   (8, 8),
                   (9, 9)])
        self.assertEqual(_alignment(elist, flist, e2f, f2e), ans)

    def test_symmetrization(self):
        sentenses = [("僕 は 男 です", "I am a man"),
                     ("私 は 女 です", "I am a girl"),
                     ("私 は 先生 です", "I am a teacher"),
                     ("彼女 は 先生 です", "She is a teacher"),
                     ("彼 は 先生 です", "He is a teacher"),
                     ]
        corpus = mkcorpus(sentenses)
        es = "私 は 先生 です".split()
        fs = "I am a teacher".split()
        syn = symmetrization(es, fs, corpus)
        ans = set([(1, 1), (1, 2), (2, 3), (3, 4), (4, 3)])
        self.assertEqual(syn, ans)


class PhraseExtractTest(unittest.TestCase):
    def test_extract(self):

        # next alignment matrix is like
        #
        # | |x|x| | |
        # |x| | |x| |
        # | | | | |x|
        #
        es = range(1, 4)
        fs = range(1, 6)
        alignment = [(2, 1),
                     (1, 2),
                     (1, 3),
                     (2, 4),
                     (3, 5)]
        ans = set([(1, 1, 2, 3), (1, 3, 1, 5), (3, 3, 5, 5), (1, 2, 1, 4)])
        self.assertEqual(extract(es, fs, alignment), ans)

        # next alignment matrix is like
        #
        # |x| | | | | | | | | |
        # | |x|x|x| | | | | | |
        # | | | | | |x| | | | |
        # | | | | | | |x| | | |
        # | | | | | | | | | |x|
        # | | | | | | | | | |x|
        # | | | | | | | |x| | |
        # | | | | | | | |x| | |
        # | | | | | | | | |x| |
        #
        es = "michael assumes that he will stay in the house".split()
        fs = "michael geht davon aus , dass er im haus bleibt".split()
        alignment = set([(1, 1),
                         (2, 2),
                         (2, 3),
                         (2, 4),
                         (3, 6),
                         (4, 7),
                         (5, 10),
                         (6, 10),
                         (7, 8),
                         (8, 8),
                         (9, 9)])
        ans = set([(1, 1, 1, 1),
                   (1, 2, 1, 4),
                   (1, 2, 1, 5),
                   (1, 3, 1, 6),
                   (1, 4, 1, 7),
                   (1, 9, 1, 10),
                   (2, 2, 2, 4),
                   (2, 2, 2, 5),
                   (2, 3, 2, 6),
                   (2, 4, 2, 7),
                   (2, 9, 2, 10),
                   (3, 3, 5, 6),
                   (3, 3, 6, 6),
                   (3, 4, 5, 7),
                   (3, 4, 6, 7),
                   (3, 9, 5, 10),
                   (3, 9, 6, 10),
                   (4, 4, 7, 7),
                   (4, 9, 7, 10),
                   (5, 6, 10, 10),
                   (5, 9, 8, 10),
                   (7, 8, 8, 8),
                   (7, 9, 8, 9),
                   (9, 9, 9, 9)])

        self.assertEqual(extract(es, fs, alignment), ans)

    def test_phrase_extract(self):
        # next alignment matrix is like
        #
        # |x| | | | | | | | | |
        # | |x|x|x| | | | | | |
        # | | | | | |x| | | | |
        # | | | | | | |x| | | |
        # | | | | | | | | | |x|
        # | | | | | | | | | |x|
        # | | | | | | | |x| | |
        # | | | | | | | |x| | |
        # | | | | | | | | |x| |
        #
        es = "michael assumes that he will stay in the house".split()
        fs = "michael geht davon aus , dass er im haus bleibt".split()
        alignment = set([(1, 1),
                         (2, 2),
                         (2, 3),
                         (2, 4),
                         (3, 6),
                         (4, 7),
                         (5, 10),
                         (6, 10),
                         (7, 8),
                         (8, 8),
                         (9, 9)])
        ans = set([(('assumes',), ('geht', 'davon', 'aus')),
                   (('assumes',), ('geht', 'davon', 'aus', ',')),
                   (('assumes', 'that'),
                    ('geht', 'davon', 'aus', ',', 'dass')),
                   (('assumes', 'that', 'he'),
                    ('geht', 'davon', 'aus', ',', 'dass', 'er')),
                   (('assumes', 'that', 'he',
                     'will', 'stay', 'in', 'the', 'house'),
                    ('geht', 'davon', 'aus', ',', 'dass',
                     'er', 'im', 'haus', 'bleibt')),
                   (('he',), ('er',)),
                   (('he', 'will', 'stay', 'in', 'the', 'house'),
                    ('er', 'im', 'haus', 'bleibt')),
                   (('house',), ('haus',)),
                   (('in', 'the'), ('im',)),
                   (('in', 'the', 'house'), ('im', 'haus')),
                   (('michael',), ('michael',)),
                   (('michael', 'assumes'),
                    ('michael', 'geht', 'davon', 'aus')),
                   (('michael', 'assumes'),
                    ('michael', 'geht', 'davon', 'aus', ',')),
                   (('michael', 'assumes', 'that'),
                    ('michael', 'geht', 'davon', 'aus', ',', 'dass')),
                   (('michael', 'assumes', 'that', 'he'),
                    ('michael', 'geht', 'davon', 'aus', ',', 'dass', 'er')),
                   (('michael',
                     'assumes',
                     'that',
                     'he',
                     'will',
                     'stay',
                     'in',
                     'the',
                     'house'),
                    ('michael',
                     'geht',
                     'davon',
                     'aus',
                     ',',
                     'dass',
                     'er',
                     'im',
                     'haus',
                     'bleibt')),
                   (('that',), (',', 'dass')),
                   (('that',), ('dass',)),
                   (('that', 'he'), (',', 'dass', 'er')),
                   (('that', 'he'), ('dass', 'er')),
                   (('that', 'he', 'will', 'stay', 'in', 'the', 'house'),
                    (',', 'dass', 'er', 'im', 'haus', 'bleibt')),
                   (('that', 'he', 'will', 'stay', 'in', 'the', 'house'),
                    ('dass', 'er', 'im', 'haus', 'bleibt')),
                   (('will', 'stay'), ('bleibt',)),
                   (('will', 'stay', 'in', 'the', 'house'),
                    ('im', 'haus', 'bleibt'))])
        self.assertEqual(phrase_extract(es, fs, alignment), ans)

        # another test
        es, fs = ("私 は 先生 です".split(), "I am a teacher".split())
        sentenses = [("僕 は 男 です", "I am a man"),
                     ("私 は 女 です", "I am a girl"),
                     ("私 は 先生 です", "I am a teacher"),
                     ("彼女 は 先生 です", "She is a teacher"),
                     ("彼 は 先生 です", "He is a teacher"),
                     ]
        corpus = mkcorpus(sentenses)
        alignment = symmetrization(es, fs, corpus)
        ans = set([(('\xe3\x81\xaf',
                     '\xe5\x85\x88\xe7\x94\x9f',
                     '\xe3\x81\xa7\xe3\x81\x99'),
                    ('a', 'teacher')),
                   (('\xe5\x85\x88\xe7\x94\x9f',), ('teacher',)),
                   (('\xe7\xa7\x81',), ('I', 'am')),
                   (('\xe7\xa7\x81',
                     '\xe3\x81\xaf',
                     '\xe5\x85\x88\xe7\x94\x9f',
                     '\xe3\x81\xa7\xe3\x81\x99'),
                    ('I', 'am', 'a', 'teacher'))])
        self.assertEqual(phrase_extract(es, fs, alignment), ans)

    def test_available_phrases(self):
        fs = "I am a teacher".split()
        phrases = set([("I", "am"),
                       ("a", "teacher"),
                       ("teacher",),
                       ("I", "am", "a", "teacher")])

        ans = set([((4, 'teacher'),),
                   ((1, 'I'), (2, 'am')),
                   ((3, 'a'), (4, 'teacher')),
                   ((1, 'I'), (2, 'am'), (3, 'a'), (4, 'teacher'))])
        self.assertEqual(available_phrases(fs, phrases), ans)

if __name__ == '__main__':
    unittest.main()
