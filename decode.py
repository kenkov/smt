#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sqlite3
#from pprint import pprint


def phrase_prob(f, e, trans, db_name=":db:"):
    """
    >>> e = u"I"
    >>> f = u"は"
    >>> prob = decode.phrase_prob(e, f, trans="en2ja", db_name=":jec_basic:")
    >>> pprint(prob)
    """
    if trans not in ["en2ja", "ja2en"]:
        raise Exception("trans argument should be either en2ja or ja2en")
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    if trans == "en2ja":
        cur.execute("""select count
                    from phrase_count where en_phrase=? and
                    ja_phrase=?""",
                    (f, e))
        count_e_f = list(cur)
        if count_e_f:
            count_e_f = count_e_f[0][0]
        cur.execute("""select count
                    from phrase_count_ja where
                    ja_phrase=?""",
                    (e,))
        count_e = list(cur)
        if count_e:
            count_e = count_e[0][0]
    elif trans == "ja2en":
        cur.execute("""select count
                    from phrase_count where en_phrase=? and
                    ja_phrase=?""",
                    (e, f))
        count_e_f = list(cur)
        if count_e_f:
            count_e_f = count_e_f[0][0]
        cur.execute("""select count
                    from phrase_count_en where
                    en_phrase=?""",
                    (e,))
        count_e = list(cur)
        if count_e:
            count_e = count_e[0][0]
    # smoothing
    if (not count_e_f) or (not count_e):
        return 1e-10
    else:
        return count_e_f / count_e


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


class HypothesisBase:
    def __init__(self,
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
                 prev_hypo
                 ):

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
        self._prev_hypo = prev_hypo
        self._prob = self._cal_prob()

    def _cal_prob(self):
        return 0

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
        d = [("sentence", self._sentence),
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

        args = {"prev_hypo": prev_hypo,
                "sentence": prev_hypo.sentence,
                "input_phrase": input_phrase,
                "output_phrase": output_phrase,
                "covered": prev_hypo.covered.union(set(input_phrase)),
                "remained": prev_hypo.remained.difference(set(input_phrase)),
                "start": input_phrase[0][0],
                "end": input_phrase[-1][0],
                "prev_start": prev_hypo.start,
                "prev_end": prev_hypo.end,
                "remain_phrases": self._calc_remain_phrases(
                    input_phrase,
                    prev_hypo.remain_phrases),
                }
        HypothesisBase.__init__(self, **args)

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
