#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sqlite3
import math
#from pprint import pprint


def phrase_prob(f, e, trans, db_name=":db:"):
    """
    >>> e = u"I am"
    >>> f = u"私 は"
    >>> prob = decode.phrase_prob(e, f, trans="en2ja", db_name=":jec_basic:")
    """
    if trans not in ["en2ja", "ja2en"]:
        raise Exception("trans argument should be either en2ja or ja2en")
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    if trans == "en2ja":
        cur.execute("""select prob
                    from phrase_prob_en2ja where
                    en_phrase=? and ja_phrase=?""",
                    (f, e))
        ans = list(cur)
    if ans:
        return ans[0][0]
    else:
        # define the default value
        # in the case no mached probability is found.
        return 1.0e-10


def available_phrases(fs, db_name=":db:"):
    """
    >>> decode.available_phrases(u"He is a teacher.".split(),
                                 db_name=":db:"))
    set([((1, u'He'),),
         ((1, u'He'), (2, u'is')),
         ((2, u'is'),),
         ((2, u'is'), (3, u'a')),
         ((3, u'a'),),
         ((4, u'teacher.'),)])
    """
    available = set()
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    for i, f in enumerate(fs):
        f_rest = ()
        for fr in fs[i:]:
            f_rest += (fr,)
            cur.execute("""select * from phrase where
                        en_phrase=?""",
                        (" ".join(f_rest),))
            lst = list(cur)
            if lst:
                available.add(tuple(enumerate(f_rest, i+1)))
    return available


class HypothesisBase(object):
    def __init__(self,
                 db_name,
                 sentence,
                 input_phrase,
                 output_phrase,
                 covered,
                 remained,
                 start,
                 end,
                 prev_start,
                 prev_end,
                 remain_phrases,
                 prob,
                 prev_hypo
                 ):

        self._db_name = db_name
        self._sentence = sentence
        self._input_phrase = input_phrase
        self._output_phrase = output_phrase
        self._covered = covered
        self._remained = remained
        self._start = start
        self._end = end
        self._prev_start = prev_start
        self._prev_end = prev_end
        self._remain_phrases = remain_phrases
        self._prob = prob
        self._prev_hypo = prev_hypo

    @property
    def db_name(self):
        return self._db_name

    @property
    def sentence(self):
        return self._sentence

    @property
    def input_phrase(self):
        return self._input_phrase

    @property
    def output_phrase(self):
        return self._output_phrase

    @property
    def covered(self):
        return self._covered

    @property
    def remained(self):
        return self._remained

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def prev_start(self):
        return self._prev_start

    @property
    def prev_end(self):
        return self._prev_end

    @property
    def prob(self):
        return self._prob

    @property
    def remain_phrases(self):
        return self._remain_phrases

    def __unicode__(self):
        d = [("db_name", self._db_name),
             ("sentence", self._sentence),
             ("input_phrase", self._input_phrase),
             ("output_phrase", self._output_phrase),
             ("covered", self._covered),
             ("remained", self._remained),
             ("start", self._start),
             ("end", self._end),
             ("prev_start", self._prev_start),
             ("prev_end", self._prev_end),
             ("remain_phrases", self._remain_phrases),
             ("probability", self._prob)
             #("prev_hypo", ""),
             ]
        return u"Hypothesis Object\n" +\
               u"\n".join([u"    " + k + u": " +
                           unicode(v) for (k, v) in d])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __hash__(self):
        return hash(unicode(self))


class Hypothesis(HypothesisBase):
    """
    Realize like the following class

    >>> args = {"sentence": fs,
    ...         "input_phrase": phrase,
    ...         "output_phrase": output_phrase,
    ...         "covered": hyp0.covered.union(set(phrase)),
    ...         "remained": hyp0.remained.difference(set(phrase)),
    ...         "start": phrase[0][0],
    ...         "end": phrase[-1][0],
    ...         "prev_start": hyp0.start,
    ...         "prev_end": hyp0.end,
    ...         "remain_phrases": remain_phrases(phrase,
    ...                                          hyp0.remain_phrases),
    ...         "prev_hypo": hyp0
    ...         }

    >>> hyp1 = decode.HypothesisBase(**args)
    """

    def __init__(self,
                 prev_hypo,
                 input_phrase,
                 output_phrase,
                 ):

        start = input_phrase[0][0]
        end = input_phrase[-1][0]
        prev_start = prev_hypo.start
        prev_end = prev_hypo.end
        args = {"db_name": prev_hypo.db_name,
                "prev_hypo": prev_hypo,
                "sentence": prev_hypo.sentence,
                "input_phrase": input_phrase,
                "output_phrase": output_phrase,
                "covered": prev_hypo.covered.union(set(input_phrase)),
                "remained": prev_hypo.remained.difference(set(input_phrase)),
                "start": start,
                "end": end,
                "prev_start": prev_start,
                "prev_end": prev_end,
                "remain_phrases": self._calc_remain_phrases(
                    input_phrase,
                    prev_hypo.remain_phrases),
                # set provability for a moment,
                # The exact probability is set below
                "prob": 1
                }
        HypothesisBase.__init__(self, **args)
        # set the exact probability
        self._prob = self._cal_prob(start - prev_end)

    def _cal_phrase_prob(self):
        input_phrase = " ".join(zip(*self._input_phrase)[1])
        output_phrase = " ".join(self._output_phrase)
        return phrase_prob(input_phrase, output_phrase,
                           trans="en2ja", db_name=self._db_name)

    def _cal_prob(self, dist):
        val = self._prev_hypo.prob *\
            self._reordering_model(0.1, dist) *\
            self._cal_phrase_prob()
        return val

    def _reordering_model(self, alpha, dist):
        return math.pow(alpha, math.fabs(dist))

    def _calc_remain_phrases(self, phrase, phrases):
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


def create_empty_hypothesis(fs, db_name):
    phrases = available_phrases(fs,
                                db_name=db_name)
    hyp0 = HypothesisBase(sentence=fs,
                          db_name=db_name,
                          input_phrase=(),
                          output_phrase=(),
                          covered=set(),
                          start=0,
                          end=0,
                          prev_start=0,
                          prev_end=0,
                          remained=set(enumerate(fs, 1)),
                          remain_phrases=phrases,
                          prev_hypo=None,
                          prob=1)
    return hyp0


class Stack(set):
    def __init__(self, size=100):
        set.__init__(self)
        self._min_hyp = None
        self._size = size

    def add_hyp(self, hyp):
        self.add(hyp)
        #if len(self) > self._size:
        #    self.remove(self.get_min_hyp())

    def get_min_hyp(self):
        pass


"""
def stack_decode(fs, phrases, phrase_prob, dist_prob):
    len_fs = len(fs)
    stacks = [Stack() for i in range(len_fs)]
    avail_phrases = available_phrases(fs,
                                      {fs_ph for (es_ph, fs_ph) in phrases})
    hyp0 = HypothesisBase((), (), {},
                          0, 0, tuple(enumerate(fs, 1)),
                          avail_phrases, ())
    stacks[0].add(hyp0)
    for i in range(len_fs):
        for hyp in stacks[i]:
            for phrase in hyp._phrases:
                output_phrases = {outpt for outpt, inpt in phrases if
                                  zip(*phrase)[1] == inpt}
                for output_phrase in output_phrases:
                    new_hyp = Hypothesis(phrase, output_phrase,
                                         hyp._covered + phrase,
                                         phrase[0][0],
                                         phrase[-1][0],
                                         None,
                                         None,
                                         None)
                    stacks[len(new_hyp._covered)].add_hyp(new_hyp)
                    # recombine
                    # prune
"""


if __name__ == '__main__':
    pass
