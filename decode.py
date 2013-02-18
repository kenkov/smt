#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
#from pprint import pprint


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
        return "\n".join([k + ": " + unicode(v) for (k, v) in d.items()])

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
    # phrases
    fs = "I am a teacher".split()
    phrases = set([("I", "am"),
                   ("a", "teacher"),
                   ("teacher",),
                   ("I", "am", "a", "teacher")])
    phrases = available_phrases(fs, phrases)
    hyp0 = Hypothesis((), (), {},
                      0, 0, tuple(enumerate(fs, 1)),
                      phrases, ())
    print(hyp0)
    stack = Stack()
    stack.add_hyp(hyp0)
