#! /usr/bin/env python
# coding:utf-8

import unittest
from fractions import Fraction as Frac
from smt.decoder.stackdecoder import _future_cost_estimate
from smt.decoder.stackdecoder import _create_estimate_dict
from smt.decoder.stackdecoder import ArgumentNotSatisfied
from smt.decoder.stackdecoder import future_cost_estimate
from smt.decoder.stackdecoder import TransPhraseProb
from smt.decoder.stackdecoder import Phrase
# sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBSetup(object):

    def __init__(self, db="sqlite:///:memory:"):
        self.db = db
        self.tables = [TransPhraseProb, Phrase]

    def __enter__(self):
        self.engine = create_engine(self.db)
        # create tables
        for Table in self.tables:
            Table.__table__.create(self.engine)

        # create session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # drop table
        for Table in self.tables:
            Table.__table__.drop(self.engine, checkfirst=True)
        self.session.close()


class FutureCostEstimateTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_future_cost_estimate_2to1(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        transfrom = 2
        transto = 1
        init_val = 100.0
        db = "sqlite:///test/:test:"

        # data set
        dataset = [("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 2
                   ("1", "tourism", Frac(-2), 0),
                   ("1", "tourism", Frac(-3), 0),
                   # 3
                   ("1", "initiative", Frac(-15, 10), 0),
                   ("1", "initiative", Frac(-25, 10), 0),
                   # 4
                   ("1", "addresses", Frac(-24, 10), 0),
                   ("1", "addresses", Frac(-34, 10), 0),
                   # 5
                   ("1", "this", Frac(-14, 10), 0),
                   ("1", "this", Frac(-24, 10), 0),
                   # 6
                   ("1", "for", Frac(-1), 0),
                   ("1", "for", Frac(-2), 0),
                   # 7
                   ("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 8
                   ("1", "first", Frac(-19, 10), 0),
                   ("1", "first", Frac(-29, 10), 0),
                   # 9
                   ("1", "time", Frac(-16, 10), 0),
                   ("1", "time", Frac(-26, 10), 0),
                   # 10
                   ("1", "initiative addresses", Frac(-4), 0),
                   ("1", "initiative addresses", Frac(-4), 0),
                   # 11
                   ("1", "this for", Frac(-25, 10), 0),
                   ("1", "this for", Frac(-35, 10), 0),
                   # 12
                   ("1", "the first", Frac(-22, 10), 0),
                   ("1", "the first", Frac(-32, 10), 0),
                   # 13
                   ("1", "for the", Frac(-13, 10), 0),
                   ("1", "for the", Frac(-23, 10), 0),
                   # 14
                   ("1", "first time", Frac(-24, 10), 0),
                   ("1", "first time", Frac(-34, 10), 0),
                   # 15
                   ("1", "this for the", Frac(-27, 10), 0),
                   ("1", "this for the", Frac(-37, 10), 0),
                   # 16
                   ("1", "for the first", Frac(-23, 10), 0),
                   ("1", "for the first", Frac(-33, 10), 0),
                   # 17
                   ("1", "the first time", Frac(-23, 10), 0),
                   ("1", "the first time", Frac(-33, 10), 0),
                   # 18
                   ("1", "for the first time", Frac(-23, 10), 0),
                   ("1", "for the first time", Frac(-33, 10), 0),
                   ]
        val = {(1, 1): -1.0,
               (1, 2): -3.0,
               (1, 3): -4.5,
               (1, 4): -6.9,
               (1, 5): -8.3,
               (1, 6): -9.3,
               (1, 7): -9.6,
               (1, 8): -10.6,
               (1, 9): -10.6,
               (2, 2): -2.0,
               (2, 3): -3.5,
               (2, 4): -5.9,
               (2, 5): -7.3,
               (2, 6): -8.3,
               (2, 7): -8.6,
               (2, 8): -9.6,
               (2, 9): -9.6,
               (3, 3): -1.5,
               (3, 4): -3.9,
               (3, 5): -5.3,
               (3, 6): -6.3,
               (3, 7): -6.6,
               (3, 8): -7.6,
               (3, 9): -7.6,
               (4, 4): -2.4,
               (4, 5): -3.8,
               (4, 6): -4.8,
               (4, 7): -5.1,
               (4, 8): -6.1,
               (4, 9): -6.1,
               (5, 5): -1.4,
               (5, 6): -2.4,
               (5, 7): -2.7,
               (5, 8): -3.6999999999999997,
               (5, 9): -3.6999999999999997,
               (6, 6): -1.0,
               (6, 7): -1.3,
               (6, 8): -2.3,
               (6, 9): -2.3,
               (7, 7): -1.0,
               (7, 8): -2.2,
               (7, 9): -2.3,
               (8, 8): -1.9,
               (8, 9): -2.4,
               (9, 9): -1.6,
               }

        with DBSetup(db) as dbobj:
            dbobj.session.add_all(TransPhraseProb(lang1p=item[0],
                                                  lang2p=item[1],
                                                  p2_1=item[2],
                                                  p1_2=item[3])
                                  for item in dataset)
            dbobj.session.add_all(Phrase(lang1p=item[0],
                                         lang2p=item[1])
                                  for item in dataset)
            dbobj.session.commit()

            ans = future_cost_estimate(sentences,
                                       transfrom=transfrom,
                                       transto=transto,
                                       init_val=init_val,
                                       db=db)
        # assert
        self.assertEqual(ans, val)

    def test_future_cost_estimate_2to1_argument_not_satisfied(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        transfrom = 2
        transto = 1
        init_val = 100.0
        db = "sqlite:///test/:test:"

        # data set
        dataset = [("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 2
                   ("1", "tourism", Frac(-2), 0),
                   ("1", "tourism", Frac(-3), 0),
                   # 3
                   ("1", "initiative", Frac(-15, 10), 0),
                   ("1", "initiative", Frac(-25, 10), 0),
                   # 4
                   ("1", "addresses", Frac(-24, 10), 0),
                   ("1", "addresses", Frac(-34, 10), 0),
                   # 5
                   #("1", "this", Frac(-14, 10), 0),
                   #("1", "this", Frac(-24, 10), 0),
                   # 6
                   ("1", "for", Frac(-1), 0),
                   ("1", "for", Frac(-2), 0),
                   # 7
                   ("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 8
                   ("1", "first", Frac(-19, 10), 0),
                   ("1", "first", Frac(-29, 10), 0),
                   # 9
                   ("1", "time", Frac(-16, 10), 0),
                   ("1", "time", Frac(-26, 10), 0),
                   # 10
                   ("1", "initiative addresses", Frac(-4), 0),
                   ("1", "initiative addresses", Frac(-4), 0),
                   # 11
                   ("1", "this for", Frac(-25, 10), 0),
                   ("1", "this for", Frac(-35, 10), 0),
                   # 12
                   ("1", "the first", Frac(-22, 10), 0),
                   ("1", "the first", Frac(-32, 10), 0),
                   # 13
                   ("1", "for the", Frac(-13, 10), 0),
                   ("1", "for the", Frac(-23, 10), 0),
                   # 14
                   ("1", "first time", Frac(-24, 10), 0),
                   ("1", "first time", Frac(-34, 10), 0),
                   # 15
                   ("1", "this for the", Frac(-27, 10), 0),
                   ("1", "this for the", Frac(-37, 10), 0),
                   # 16
                   ("1", "for the first", Frac(-23, 10), 0),
                   ("1", "for the first", Frac(-33, 10), 0),
                   # 17
                   ("1", "the first time", Frac(-23, 10), 0),
                   ("1", "the first time", Frac(-33, 10), 0),
                   # 18
                   ("1", "for the first time", Frac(-23, 10), 0),
                   ("1", "for the first time", Frac(-33, 10), 0),
                   ]

        val = {(1, 1): -1.0,
               (1, 2): -3.0,
               (1, 3): -4.5,
               (1, 4): -6.9,
               (1, 5): -106.9,
               (1, 6): -9.4,
               (1, 7): -9.6,
               (1, 8): -11.5,
               (1, 9): -11.7,
               (2, 2): -2.0,
               (2, 3): -3.5,
               (2, 4): -5.9,
               (2, 5): -105.9,
               (2, 6): -8.4,
               (2, 7): -8.6,
               (2, 8): -10.5,
               (2, 9): -10.7,
               (3, 3): -1.5,
               (3, 4): -3.9,
               (3, 5): -103.9,
               (3, 6): -6.4,
               (3, 7): -6.6,
               (3, 8): -8.5,
               (3, 9): -8.7,
               (4, 4): -2.4,
               (4, 5): -102.4,
               (4, 6): -4.9,
               (4, 7): -5.1,
               (4, 8): -7.0,
               (4, 9): -7.199999999999999,
               (5, 5): -100.0,
               (5, 6): -2.5,
               (5, 7): -2.7,
               (5, 8): -4.6,
               (5, 9): -4.8,
               (6, 6): -1.0,
               (6, 7): -1.3,
               (6, 8): -2.3,
               (6, 9): -2.3,
               (7, 7): -1.0,
               (7, 8): -2.2,
               (7, 9): -2.3,
               (8, 8): -1.9,
               (8, 9): -2.4,
               (9, 9): -1.6,
               }

        with DBSetup(db) as dbobj:
            dbobj.session.add_all(TransPhraseProb(lang1p=item[0],
                                                  lang2p=item[1],
                                                  p2_1=item[2],
                                                  p1_2=item[3])
                                  for item in dataset)
            dbobj.session.add_all(Phrase(lang1p=item[0],
                                         lang2p=item[1])
                                  for item in dataset)
            dbobj.session.commit()

            ans = future_cost_estimate(sentences,
                                       transfrom=transfrom,
                                       transto=transto,
                                       init_val=init_val,
                                       db=db)

        # assert
        self.assertEqual(ans, val)

    def test_future_cost_estimate_1to2(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        transfrom = 1
        transto = 2
        init_val = 100.0
        db = "sqlite:///test/:test:"

        # data set
        dataset = [("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 2
                   ("1", "tourism", Frac(-2), 0),
                   ("1", "tourism", Frac(-3), 0),
                   # 3
                   ("1", "initiative", Frac(-15, 10), 0),
                   ("1", "initiative", Frac(-25, 10), 0),
                   # 4
                   ("1", "addresses", Frac(-24, 10), 0),
                   ("1", "addresses", Frac(-34, 10), 0),
                   # 5
                   ("1", "this", Frac(-14, 10), 0),
                   ("1", "this", Frac(-24, 10), 0),
                   # 6
                   ("1", "for", Frac(-1), 0),
                   ("1", "for", Frac(-2), 0),
                   # 7
                   ("1", "the", Frac(-1), 0),
                   ("1", "the", Frac(-2), 0),
                   # 8
                   ("1", "first", Frac(-19, 10), 0),
                   ("1", "first", Frac(-29, 10), 0),
                   # 9
                   ("1", "time", Frac(-16, 10), 0),
                   ("1", "time", Frac(-26, 10), 0),
                   # 10
                   ("1", "initiative addresses", Frac(-4), 0),
                   ("1", "initiative addresses", Frac(-4), 0),
                   # 11
                   ("1", "this for", Frac(-25, 10), 0),
                   ("1", "this for", Frac(-35, 10), 0),
                   # 12
                   ("1", "the first", Frac(-22, 10), 0),
                   ("1", "the first", Frac(-32, 10), 0),
                   # 13
                   ("1", "for the", Frac(-13, 10), 0),
                   ("1", "for the", Frac(-23, 10), 0),
                   # 14
                   ("1", "first time", Frac(-24, 10), 0),
                   ("1", "first time", Frac(-34, 10), 0),
                   # 15
                   ("1", "this for the", Frac(-27, 10), 0),
                   ("1", "this for the", Frac(-37, 10), 0),
                   # 16
                   ("1", "for the first", Frac(-23, 10), 0),
                   ("1", "for the first", Frac(-33, 10), 0),
                   # 17
                   ("1", "the first time", Frac(-23, 10), 0),
                   ("1", "the first time", Frac(-33, 10), 0),
                   # 18
                   ("1", "for the first time", Frac(-23, 10), 0),
                   ("1", "for the first time", Frac(-33, 10), 0),
                   ]

        val = {(1, 1): -1.0,
               (1, 2): -3.0,
               (1, 3): -4.5,
               (1, 4): -6.9,
               (1, 5): -8.3,
               (1, 6): -9.3,
               (1, 7): -9.6,
               (1, 8): -10.6,
               (1, 9): -10.6,
               (2, 2): -2.0,
               (2, 3): -3.5,
               (2, 4): -5.9,
               (2, 5): -7.3,
               (2, 6): -8.3,
               (2, 7): -8.6,
               (2, 8): -9.6,
               (2, 9): -9.6,
               (3, 3): -1.5,
               (3, 4): -3.9,
               (3, 5): -5.3,
               (3, 6): -6.3,
               (3, 7): -6.6,
               (3, 8): -7.6,
               (3, 9): -7.6,
               (4, 4): -2.4,
               (4, 5): -3.8,
               (4, 6): -4.8,
               (4, 7): -5.1,
               (4, 8): -6.1,
               (4, 9): -6.1,
               (5, 5): -1.4,
               (5, 6): -2.4,
               (5, 7): -2.7,
               (5, 8): -3.6999999999999997,
               (5, 9): -3.6999999999999997,
               (6, 6): -1.0,
               (6, 7): -1.3,
               (6, 8): -2.3,
               (6, 9): -2.3,
               (7, 7): -1.0,
               (7, 8): -2.2,
               (7, 9): -2.3,
               (8, 8): -1.9,
               (8, 9): -2.4,
               (9, 9): -1.6,
               }

        with DBSetup(db) as dbobj:
            dbobj.session.add_all(TransPhraseProb(lang2p=item[0],
                                                  lang1p=item[1],
                                                  p1_2=item[2],
                                                  p2_1=item[3])
                                  for item in dataset)
            dbobj.session.add_all(Phrase(lang1p=item[0],
                                         lang2p=item[1])
                                  for item in dataset)
            dbobj.session.commit()

            ans = future_cost_estimate(sentences,
                                       transfrom=transfrom,
                                       transto=transto,
                                       init_val=init_val,
                                       db=db)
        # assert
        self.assertEqual(ans, val)

    def test__future_cost_estimate(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        phrase_prob = {(1, 1): Frac(-1),
                       (2, 2): Frac(-2),
                       (3, 3): Frac(-15, 10),
                       (4, 4): Frac(-24, 10),
                       (5, 5): Frac(-14, 10),
                       (6, 6): Frac(-1),
                       (7, 7): Frac(-1),
                       (8, 8): Frac(-19, 10),
                       (9, 9): Frac(-16, 10),
                       (3, 4): Frac(-4),
                       (5, 6): Frac(-25, 10),
                       (7, 8): Frac(-22, 10),
                       (6, 7): Frac(-13, 10),
                       (8, 9): Frac(-24, 10),
                       (5, 7): Frac(-27, 10),
                       (6, 8): Frac(-23, 10),
                       (7, 9): Frac(-23, 10),
                       (6, 9): Frac(-23, 10),
                       }
        val = {(1, 1): Frac(-1),
               (1, 2): Frac(-3),
               (1, 3): Frac(-45, 10),
               (1, 4): Frac(-69, 10),
               (1, 5): Frac(-83, 10),
               (1, 6): Frac(-93, 10),
               (1, 7): Frac(-96, 10),
               (1, 8): Frac(-106, 10),
               (1, 9): Frac(-106, 10),
               (2, 2): Frac(-2),
               (2, 3): Frac(-35, 10),
               (2, 4): Frac(-59, 10),
               (2, 5): Frac(-73, 10),
               (2, 6): Frac(-83, 10),
               (2, 7): Frac(-86, 10),
               (2, 8): Frac(-96, 10),
               (2, 9): Frac(-96, 10),
               (3, 3): Frac(-15, 10),
               (3, 4): Frac(-39, 10),
               (3, 5): Frac(-53, 10),
               (3, 6): Frac(-63, 10),
               (3, 7): Frac(-66, 10),
               (3, 8): Frac(-76, 10),
               (3, 9): Frac(-76, 10),
               (4, 4): Frac(-24, 10),
               (4, 5): Frac(-38, 10),
               (4, 6): Frac(-48, 10),
               (4, 7): Frac(-51, 10),
               (4, 8): Frac(-61, 10),
               (4, 9): Frac(-61, 10),
               (5, 5): Frac(-14, 10),
               (5, 6): Frac(-24, 10),
               (5, 7): Frac(-27, 10),
               (5, 8): Frac(-37, 10),
               (5, 9): Frac(-37, 10),
               (6, 6): Frac(-1),
               (6, 7): Frac(-13, 10),
               (6, 8): Frac(-23, 10),
               (6, 9): Frac(-23, 10),
               (7, 7): Frac(-1),
               (7, 8): Frac(-22, 10),
               (7, 9): Frac(-23, 10),
               (8, 8): Frac(-19, 10),
               (8, 9): Frac(-24, 10),
               (9, 9): Frac(-16, 10)}
        ans = _future_cost_estimate(sentences,
                                    phrase_prob)
        self.assertEqual(ans, val)

    def test__future_cost_estimate_dict_not_satisfied(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        phrase_prob = {(1, 1): Frac(-1),
                       (2, 2): Frac(-2),
                       # lack one value
                       #(3, 3): Frac(-15, 10),
                       (4, 4): Frac(-24, 10),
                       (5, 5): Frac(-14, 10),
                       (6, 6): Frac(-1),
                       (7, 7): Frac(-1),
                       (8, 8): Frac(-19, 10),
                       (9, 9): Frac(-16, 10),
                       (3, 4): Frac(-4),
                       (5, 6): Frac(-25, 10),
                       (7, 8): Frac(-22, 10),
                       (6, 7): Frac(-13, 10),
                       (8, 9): Frac(-24, 10),
                       (5, 7): Frac(-27, 10),
                       (6, 8): Frac(-23, 10),
                       (7, 9): Frac(-23, 10),
                       (6, 9): Frac(-23, 10),
                       }
        self.assertRaises(ArgumentNotSatisfied,
                          _future_cost_estimate,
                          sentences,
                          phrase_prob)

    def test_create_estimate_dict(self):
        sentences = u"the tourism initiative addresses this\
            for the first time".split()
        init_val = Frac(-100)
        phrase_prob = {(1, 1): Frac(-1),
                       (2, 2): Frac(-2),
                       # lack one value
                       #(3, 3): Frac(-15, 10),
                       (4, 4): Frac(-24, 10),
                       (5, 5): Frac(-14, 10),
                       #(6, 6): Frac(-1),
                       (7, 7): Frac(-1),
                       # lack one value
                       #(8, 8): Frac(-19, 10),
                       (9, 9): Frac(-16, 10),
                       (3, 4): Frac(-4),
                       (5, 6): Frac(-25, 10),
                       (7, 8): Frac(-22, 10),
                       (6, 7): Frac(-13, 10),
                       (8, 9): Frac(-24, 10),
                       (5, 7): Frac(-27, 10),
                       (6, 8): Frac(-23, 10),
                       (7, 9): Frac(-23, 10),
                       (6, 9): Frac(-23, 10),
                       }
        correct = {(1, 1): Frac(-1),
                   (2, 2): Frac(-2),
                   # lack one value
                   (3, 3): init_val,
                   (4, 4): Frac(-24, 10),
                   (5, 5): Frac(-14, 10),
                   (6, 6): init_val,
                   (7, 7): Frac(-1),
                   # lack one value
                   (8, 8): init_val,
                   (9, 9): Frac(-16, 10),
                   (3, 4): Frac(-4),
                   (5, 6): Frac(-25, 10),
                   (7, 8): Frac(-22, 10),
                   (6, 7): Frac(-13, 10),
                   (8, 9): Frac(-24, 10),
                   (5, 7): Frac(-27, 10),
                   (6, 8): Frac(-23, 10),
                   (7, 9): Frac(-23, 10),
                   (6, 9): Frac(-23, 10),
                   }
        ans = _create_estimate_dict(sentences,
                                    phrase_prob,
                                    init_val=init_val)
        self.assertEqual(ans, correct)


if __name__ == '__main__':
    unittest.main()
