#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import ibmmodel2


def alignment(elist, flist, e2f, f2e):
    '''
    elist, flist
        wordlist for each language
    e2f
        translatoin alignment from e to f
        alignment is
        [(f, e)]
    f2e
        translatoin alignment from f to e
        alignment is
        [(f, e)]
    return
        alignment: {(f, e)}
             flist
          -----------------
        e |               |
        l |               |
        i |               |
        s |               |
        t |               |
          -----------------

    '''
    neighboring = {(-1, 0), (0, -1), (1, 0), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)}
    alignment = e2f.intersection(f2e)
    # marge with neighborhood
    while True:
        set_len = len(alignment)
        for e_word in xrange(1, len(flist)+1):
            for f_word in xrange(1, len(elist)+1):
                if (e_word, f_word) in alignment:
                    for (e_diff, f_diff) in neighboring:
                        e_new = e_word + e_diff
                        f_new = f_word + f_diff
                        if ((e_new not in zip(*alignment)[0]
                             or f_new not in zip(*alignment)[1])
                            and (e_new, f_new) in e2f.union(f2e)):
                            alignment.add((e_new, f_new))
        if set_len == len(alignment):
            break
    # finalize
    for e_word in xrange(1, len(flist)+1):
        for f_word in xrange(1, len(elist)+1):
            if ((e_word not in zip(*alignment)[0]
                 or f_word not in zip(*alignment)[1])
                and (e_word, f_word) in e2f.union(f2e)):
                alignment.add((e_word, f_word))
    return alignment


def symmetrization(es, fs, corpus):
    '''
    forpus
        for translation from fs to es
    return
        alignment **from fs to es**
    '''
    f2e_train = ibmmodel2._train(corpus, loop_count=1000)
    f2e_alignment = ibmmodel2.viterbi_alignment(es, fs, *f2e_train).items()
    f2e = zip(*reversed(zip(*f2e_alignment)))

    e2f_corpus = zip(*reversed(zip(*corpus)))
    e2f_train = ibmmodel2._train(e2f_corpus, loop_count=1000)
    e2f = ibmmodel2.viterbi_alignment(fs, es, *e2f_train).items()

    return alignment(es, fs, set(e2f), set(f2e))


def show_matrix(es, fs, corpus):
    '''
    return
        matrix like
                    fs
             ----------------
             |              |
            e|              |
            s|              |
             |              |
             ----------------
    '''
    m = len(es)
    n = len(fs)
    lst = symmetrization(es, fs, corpus)
    fmt = ""
    for i in xrange(m):
        fmt += "|"
        for j in xrange(n):
            if (j+1, i+1) in lst:
                fmt += "x|"
            else:
                fmt += " |"
        fmt += "\n"
    return fmt


if __name__ == '__main__':
    sent_pairs = [("僕 は 男 です", "I am a man"),
                  ("私 は 女 です", "I am a girl"),
                  ("私 は 先生 です", "I am a teacher"),
                  ("彼女 は 先生 です", "She is a teacher"),
                  ("彼 は 先生 です", "He is a teacher"),
                  ]
    #sent_pairs = [("the house", "das Haus"),
    #              ("the book", "das Buch"),
    #              ("a book", "ein Buch"),
    #              ]
    corpus = [(es.split(), fs.split()) for (es, fs) in sent_pairs]
    args = ("私 は 先生 です".split(), "I am a teacher".split(), corpus)
    #args = ("a house".split(), "ein Buch".split(), corpus)
    ans = symmetrization(*args)
    print(ans)
    print(show_matrix(*args))
