#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sys
sys.path.append("../")
import decode


def remain_phrases(phrase, phrases):
    """
    >>> res = remain_phrases(((2, u'is'),),
                             set([((1, u'he'),),
                                  ((2, u'is'),),
                                  ((3, u'a'),),
                                  ((2, u'is'),
                                   (3, u'a')),
                                  ((4, u'teacher'),)]))
    set([((1, u'he'),), ((3, u'a'),), ((4, u'teacher'),)])
    >>> res = remain_phrases(((2, u'is'), (3, u'a')),
                             set([((1, u'he'),),
                                  ((2, u'is'),),
                                  ((3, u'a'),),
                                  ((2, u'is'),
                                   (3, u'a')),
                                  ((4, u'teacher'),)]))
    set([((1, u'he'),), ((4, u'teacher'),)])
    """
    s = set()
    for ph in phrases:
        for p in phrase:
            if p in ph:
                break
        else:
            s.add(ph)
    return s


if __name__ == '__main__':
    import sqlite3
    db_name = ":jec_basic:"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    fs = u"he is a teacher".split()
    #phrases = decode.available_phrases(fs,
    #                                   db_name=":jec_basic:")
    #hyp0 = decode.HypothesisBase(sentence=fs,
    #                             db_name=":jec_basic:",
    #                             input_phrase=(),
    #                             output_phrase=(),
    #                             covered=set(),
    #                             start=0,
    #                             end=0,
    #                             prev_start=0,
    #                             prev_end=0,
    #                             remained=set(enumerate(fs, 1)),
    #                             remain_phrases=phrases,
    #                             prev_hypo=None,
    #                             prob=1)
    hyp0 = decode.create_empty_hypothesis(fs, db_name=db_name)
    for phrase in hyp0.remain_phrases:
        phrase_str = u" ".join(zip(*phrase)[1])
        cur.execute("""select ja_phrase from phrase_count where
                    en_phrase=?""",
                    (phrase_str,))
        for output_phrase in cur:
            output_phrase = output_phrase[0]
            #args = {"sentence": fs,
            #        "input_phrase": phrase,
            #        "output_phrase": output_phrase,
            #        "covered": hyp0.covered.union(set(phrase)),
            #        "remained": hyp0.remained.difference(set(phrase)),
            #        "start": phrase[0][0],
            #        "end": phrase[-1][0],
            #        "prev_start": hyp0.start,
            #        "prev_end": hyp0.end,
            #        "remain_phrases": remain_phrases(phrase,
            #                                         hyp0.remain_phrases),
            #        "prev_hypo": hyp0
            #        }

            #hyp1 = decode.HypothesisBase(**args)
            hyp1 = decode.Hypothesis(prev_hypo=hyp0,
                                     input_phrase=phrase,
                                     output_phrase=output_phrase)
            print(hyp1)
