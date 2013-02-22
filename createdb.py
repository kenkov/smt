#! /usr/bin/env python
# coding:utf-8

from __future__ import division, print_function
import sqlite3
import collections
import ibmmodel2
import word_alignment
import keitaiso
import phrase_extract
from progressline import ProgressLine


# create train db
def create_corpus(trans, db_name=":db:", limit=None):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    if trans == "en2ja":
        if limit:
            cur.execute("select ja, en from sentence limit ?",
                        (limit,))
        else:
            cur.execute("select ja, en from sentence")
    elif trans == "ja2en":
        if limit:
            cur.execute("select en, ja from sentence limit ?",
                        (limit,))
        else:
            cur.execute("select en, ja from sentence")
    else:
        raise Exception("Please select en2ja or ja2en for limit argument")

    sent_pairs = []
    # use keitaiso.str2wakati for Japanese
    # use identity function for English
    if trans == "en2ja":
        _to_func = keitaiso.str2wakati
        _from_func = lambda x: x
    elif trans == "ja2en":
        _to_func = lambda x: x
        _from_func = keitaiso.str2wakati

    for item in cur:
        _to = _to_func(item[0])
        _from = _from_func(item[1])
        sent_pairs.append((_to, _from))

    con.close()
    return sent_pairs


#def benchmark_ibmmodel2():
#    sent_pairs = create_corpus()
#    with Benchmarker(width=20) as bm:
#        with bm('loop_count=100, limit=1000'):
#            t, a = ibmmodel2.train(sent_pairs, loop_count=100)


def create_train_db(trans, db_name=":db:", limit=None, loop_count=1000):
    if not trans in ["en2ja", "ja2en"]:
        raise Exception("please select en2ja or ja2en for trans argmument")

    table_prefix = trans + "_"
    con = sqlite3.connect(db_name)
    cur = con.cursor()

    # create table for word probability
    prob_tablename = table_prefix + "wordprob"
    try:
        cur.execute("drop table {0}".format(prob_tablename))
    except sqlite3.Error:
        print("{0} table does not exists.\n\
              => creating a new table".format(prob_tablename))
    cur.execute("create table {0}\
                (to_ TEXT, from_ TEXT, prob REAL)".format(prob_tablename))
    con.commit()

    # create table for word alignment
    align_tablename = table_prefix + "wordalign"
    try:
        cur.execute("drop table {0}".format(align_tablename))
    except sqlite3.Error:
        print("{0} table does not exists.\n\
              => creating a new table".format(align_tablename))
    cur.execute("create table {0}\
                (from_pos INTEGER, to_pos INTEGER,\
                to_len INTEGER, from_len INTEGER, prob\
                REAL)".format(align_tablename))
    con.commit()

    # IBM learning
    p = ProgressLine(0.12, title='IBM Model learning...')
    p.start()
    t, a = ibmmodel2.train(sent_pairs=create_corpus(trans,
                                                    db_name=db_name,
                                                    limit=limit),
                           loop_count=loop_count)
    p.stop()
    # insert
    p = ProgressLine(0.12, title='inserting items into database')
    for (_to, _from), prob in t.items():
        cur.execute("insert into {0}\
                     values (?, ?, ?)".format(prob_tablename),
                    (_to, _from, prob))
    for tpl, prob in a.items():
        cur.execute("insert into {0} values\
                    (?, ?, ?, ?, ?)".format(align_tablename),
                    tpl + (prob,))
    con.commit()
    p.stop()


# create phrase db
def db_viterbi_alignment(es, fs, trans, db_name=":db:", init_val=0.00001):
    """
    Calculating viterbi_alignment using specified database.

    Arguments:
        trans:
            it can take "en2ja" or "ja2en"
    """

    def get_wordprob(e, f, trans, db_name=":db:"):
        table_name = trans + "_wordprob"
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from {0}\
                    where to_=? and from_=?'.format(table_name),
                    (e, f))
        res = list(cur)
        return res[0][0] if res else init_val

    def get_wordalign(i, j, l_e, l_f, trans, db_name=":db:",
                      init_val=0.00001):
        table_name = trans + "_wordalign"
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(u'select prob from {0}\
                    where\
                    from_pos=? and\
                    to_pos=? and\
                    to_len=? and\
                    from_len=?'.format(table_name),
                    (i, j, l_e, l_f))
        res = list(cur)
        return res[0][0] if res else init_val

    # algorithm
    max_a = collections.defaultdict(float)
    l_e = len(es)
    l_f = len(fs)
    for (j, e) in enumerate(es, 1):
        current_max = (0, -1)
        for (i, f) in enumerate(fs, 1):
            val = get_wordprob(e, f, db_name=db_name, trans=trans) *\
                get_wordalign(i, j, l_e, l_f, db_name=db_name,
                              trans=trans)
            # select the first one among the maximum candidates
            if current_max[1] < val:
                current_max = (i, val)
        max_a[j] = current_max[0]
    return max_a


def db_show_matrix(es, fs, trans, db_name=":db:"):
    '''
    print matrix according to viterbi alignment like
          fs
     -------------
    e|           |
    s|           |
     |           |
     -------------
    >>> sent_pairs = [("僕 は 男 です", "I am a man"),
                      ("私 は 女 です", "I am a girl"),
                      ("私 は 先生 です", "I am a teacher"),
                      ("彼女 は 先生 です", "She is a teacher"),
                      ("彼 は 先生 です", "He is a teacher"),
                      ]
    >>> t, a = train(sent_pairs, loop_count=1000)
    >>> args = ("私 は 先生 です".split(), "I am a teacher".split(), t, a)
    |x| | | |
    | | |x| |
    | | | |x|
    | | |x| |
    '''
    max_a = db_viterbi_alignment(es, fs, trans=trans,
                                 db_name=db_name).items()
    m = len(es)
    n = len(fs)
    return ibmmodel2.matrix(m, n, max_a)


def _db_symmetrization(es, fs, db_name=":db:"):
    '''
    calculating symmetrization of word alignment
    translationing from English to Japanese.

    Arguments:
        en: Japanese
        fs: English
    '''
    f2e = db_viterbi_alignment(es, fs, trans="en2ja",
                               db_name=db_name).items()
    e2f = db_viterbi_alignment(fs, es, trans="ja2en",
                               db_name=db_name).items()
    return word_alignment.alignment(es, fs, e2f, f2e)


def db_phrase_extract(es, fs, db_name=":db:"):
    ja = keitaiso.str2wakati(es).split()
    en = fs.split()
    alignment = _db_symmetrization(ja, en,
                                   db_name=db_name)
    return phrase_extract.phrase_extract(ja, en, alignment)


def create_phrase_db(db_name=":db:", limit=None):
    # create table
    table_name = "phrase"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop table {0}".format(table_name))
    except sqlite3.Error:
        print("{0} table does not exists.\
              creating a new table".format(table_name))
    cur.execute("create table {0}\
                (ja_phrase TEXT, en_phrase TEXT)".format(table_name))
    con.commit()

    cur_loop = con.cursor()
    if limit:
        cur_loop.execute("select ja, en from sentence limit ?",
                         (limit,))
    else:
        cur_loop.execute("select ja, en from sentence")

    print("extracting phrases...")
    for ja, en in cur_loop:
        print("  ", ja, en)
        for ja_phrase, en_phrase in db_phrase_extract(ja, en,
                                                      db_name=db_name):
            ja_p = u" ".join(ja_phrase)
            en_p = u" ".join(en_phrase)
            cur.execute("insert into {0} values\
                        (?, ?)".format(table_name),
                        (ja_p, en_p))
    print("extracting phrases done")
    con.commit()


def create_phrase_count_view(db_name=":db:"):
    # create phrase_count table
    table_name = "phrase_count"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop view {0}".format(table_name))
    except sqlite3.Error:
        print("{0} view does not exists.\n\
              => creating a new view".format(table_name))
    cur.execute("""create view {0}
                 as select *, count(*) as count from
                phrase group by ja_phrase, en_phrase order by count
                desc""".format(table_name))
    con.commit()

    # create phrase_count_ja table
    table_name_ja = "phrase_count_ja"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop view {0}".format(table_name_ja))
    except sqlite3.Error:
        print("{0} view does not exists.\n\
              => creating a new view".format(table_name_ja))
    cur.execute("""create view {0}
                as select ja_phrase,
                sum(count) as count from phrase_count group by
                ja_phrase order
                by count desc""".format(table_name_ja))
    con.commit()

    # create phrase_count_en table
    table_name_en = "phrase_count_en"
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop view {0}".format(table_name_en))
    except sqlite3.Error:
        print("{0} view does not exists.\n\
              => creating a new view".format(table_name_en))
    cur.execute("""create view {0}
                as select en_phrase,
                sum(count) as count from phrase_count group by
                en_phrase order
                by count desc""".format(table_name_en))
    con.commit()


def create_phrase_prob(trans, db_name=":db:"):
    """
    """
    # create phrase_prob table
    if trans not in ["en2ja", "ja2en"]:
        raise Exception("trans argument should be either en2ja or ja2en")
    table_name = "phrase_prob_{0}".format(trans)
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("drop table {0}".format(table_name))
    except sqlite3.Error:
        print("{0} table does not exists.\n\
              => creating a new table".format(table_name))
    if trans == "en2ja":
        cur.execute("""create table {0}
                    (en TEXT, ja TEXT, prob REAL)
                    """.format(table_name))
    if trans == "ja2en":
        cur.execute("""create table {0}
                    (ja TEXT, en TEXT, prob REAL)
                    """.format(table_name))
    con.commit()

    cur_sel = con.cursor()
    cur_rec = con.cursor()
    cur.execute("select ja_phrase, en_phrase, count from phrase_count")
    for ja_p, en_p, count in cur:
        if trans == "en2ja":
            cur_sel.execute("""select count
                            from phrase_count_ja where
                            ja_phrase=?""",
                            (ja_p,))
            count_e_j = list(cur_sel)
            count_e_j = count_e_j[0][0]
            prob = count / count_e_j
            cur_rec.execute("""insert into {0} values
                            (?, ?, ?)""".format(table_name),
                            (en_p, ja_p, prob))
            print(u"{0} => {1} : {2}".format(ja_p, en_p, prob))
        con.commit()
        # I must implement ja2en ver.
    con.commit()


if __name__ == "__main__":
    pass
    #create_train_db(trans="en2ja",
    #                db_name=":jec_basic:",
    #                limit=None,
    #                loop_count=1000)
    #create_train_db(trans="ja2en",
    #                db_name=":jec_basic:",
    #                limit=None,
    #                loop_count=1000)
    #create_phrase_db(db_name=":jec_basic:", limit=None)
    #create_phrase_count_view(db_name=":jec_basic:")
