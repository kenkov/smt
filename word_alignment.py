#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function


def alignment(elist, flist, e2f, f2e):
    neighboring = {(-1, 0), (0, -1), (1, 0), (0, 1),
                   (-1, -1), (-1, 1), (1, -1), (1, 1)}
    alignment = e2f.intersection(f2e)
    # marge with neighborhood
    while True:
        set_len = len(alignment)
        for e_word in xrange(len(flist)):
            for f_word in xrange(len(elist)):
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
    for e_word in xrange(len(flist)):
        for f_word in xrange(len(elist)):
            if ((e_word not in zip(*alignment)[0]
                 or f_word not in zip(*alignment)[1])
                and (e_word, f_word) in e2f.union(f2e)):
                alignment.add((e_word, f_word))
    return alignment


def show_matrix(m, n, lst):
    fmt = ""
    for i in xrange(m):
        fmt += "|"
        for j in xrange(n):
            if (j, i) in lst:
                fmt += "x|"
            else:
                fmt += " |"
        fmt += "\n"
    return fmt


if __name__ == '__main__':
    elist = ["michael",
             "assumes",
             "that",
             "he",
             "will",
             "stay",
             "in",
             "the",
             "house"]
    flist = ["michael",
             "geht",
             "davon",
             "aus",
             ",",
             "dass",
             "er",
             "im",
             "haus",
             "bleibt"]
    e2f = {(0, 0),
           (1, 1),
           (2, 1),
           (3, 1),
           (5, 2),
           (6, 3),
           (7, 6),
           (8, 8),
           (9, 5)}
    f2e = {(0, 0),
           (1, 1),
           (5, 2),
           (6, 3),
           (7, 6),
           (7, 7),
           (8, 8),
           (9, 4),
           (9, 5)}
    print(show_matrix(9, 10, e2f))
    print(show_matrix(9, 10, f2e))
    print(show_matrix(9, 10, alignment(elist, flist, e2f, f2e)))
