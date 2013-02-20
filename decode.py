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


class Hypothesis:
    def __init__(self, input_phrase, output_phrase, covered,
                 start, end, remained, phrases, sentence):

        self._input_phrase = input_phrase
        self._output_phrase = output_phrase
        self._start = start
        self._end = end
        self._covered = covered
        self._remained = remained
        self._phrases = phrases
        self._sentence = sentence
        self._probability = self._cal_prob()

    def _cal_prob(self):
        return 0

    def __unicode__(self):
        d = {"input_phrase": self._input_phrase,
             "output_phrase": self._output_phrase,
             "start": self._start,
             "end": self._end,
             "covered": self._covered,
             "remained": self._remained,
             "phrases": self._phrases,
             "sentence": self._sentence,
             "probability": self._probability
             }
        return u"\n".join([k + u": " + unicode(v) for (k, v) in d.items()])

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __hash__(self):
        return hash(unicode(self))


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


def stack_decode(fs, phrases, phrase_prob, dist_prob):
    len_fs = len(fs)
    stacks = [Stack() for i in range(len_fs)]
    avail_phrases = available_phrases(fs,
                                      {fs_ph for (es_ph, fs_ph) in phrases})
    hyp0 = Hypothesis((), (), {},
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


if __name__ == '__main__':
    from phrase_extract import available_phrases
    from pprint import pprint
    # phrases
    fs = "I am a teacher".split()
    phrases = set([("I", "am"),
                   ("a", "teacher"),
                   ("teacher",),
                   ("I", "am", "a", "teacher")])
    phrases = available_phrases(fs, phrases)
    pprint(phrases)
    #hyp0 = Hypothesis((), (), {},
    #                  0, 0, tuple(enumerate(fs, 1)),
    #                  phrases, ())
    #print(hyp0)
    #stack = Stack()
    #stack.add_hyp(hyp0)
