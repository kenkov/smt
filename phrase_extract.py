#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
from pprint import pprint


def phrase_extract(es, fs, alignment):
    ext = extract(es, fs, alignment)
    ind = {((x, y), (z, w)) for x, y, z, w in ext}
    es = tuple(es)
    fs = tuple(fs)
    return {(es[e_s-1:e_e], fs[f_s-1:f_e])
            for (e_s, e_e), (f_s, f_e) in ind}


def extract(es, fs, alignment):
    """
    caution:
        alignment starts from 1 - not 0
    """
    phrases = set()
    len_es = len(es)
    for e_start in range(1, len_es+1):
        for e_end in range(e_start, len_es+1):
            # find the minimally matching foreign phrase
            f_start, f_end = (len(fs), 0)
            for (e, f) in alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)
            phrases.update(_extract(es, fs, e_start,
                                    e_end, f_start,
                                    f_end, alignment))
    return phrases


def _extract(es, fs, e_start, e_end, f_start, f_end, alignment):
    if f_end == 0:
        return {}
    for (e, f) in alignment:
        if (f_start <= f <= f_end) and (e < e_start or e > e_end):
            return {}
    ex = set()
    f_s = f_start
    while True:
        f_e = f_end
        while True:
            ex.add((e_start, e_end, f_s, f_e))
            f_e += 1
            if f_e in zip(*alignment)[1] or f_e > len(fs):
                break
        f_s -= 1
        if f_s in zip(*alignment)[1] or f_s < 1:
            break
    return ex


def available_phrases(fs, phrases):
    available = set()
    for phrase in phrases:
        for ind, f in enumerate(fs, 1):
            if f in phrase and phrase not in available:
                available.add((ind, f))
    return available


if __name__ == '__main__':
    # test 1
    #es = "michael assumes that he will stay in the house".split()
    #fs = "michael geht davon aus , dass er im haus bleibt".split()
    #alignment = set([(1, 1),
    #                 (2, 2),
    #                 (2, 3),
    #                 (2, 4),
    #                 (3, 6),
    #                 (4, 7),
    #                 (5, 10),
    #                 (6, 10),
    #                 (7, 8),
    #                 (8, 8),
    #                 (9, 9)])
    #pprint(phrase_extract(es, fs, alignment))

    # test2
    from utility import mkcorpus
    from word_alignment import symmetrization
    sentenses = [("僕 は 男 です", "I am a man"),
                 ("私 は 女 です", "I am a girl"),
                 ("私 は 先生 です", "I am a teacher"),
                 ("彼女 は 先生 です", "She is a teacher"),
                 ("彼 は 先生 です", "He is a teacher"),
                 ]
    corpus = mkcorpus(sentenses)
    es, fs = ("私 は 先生 です".split(), "I am a teacher".split())
    alignment = symmetrization(es, fs, corpus)
    ext = phrase_extract(es, fs, alignment)
    pprint(ext)
    for e, f in ext:
        print(' '.join(e), "<->", ' '.join(f))

    # phrases
    fs = "I am a teacher".split()
    phrases = set([("I", "am"),
                   ("a", "teacher"),
                   ("teacher",),
                   ("I", "am", "a", "teacher")])
    print(available_phrases(fs, phrases))
