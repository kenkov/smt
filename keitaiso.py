#! /usr/bin/env python
# coding:utf-8

#
# Last Updated on 2012/04/25 18:45:15 .
#

u"""
===============================
keitaiso.py
===============================

"""

import MeCab

class Keitaiso(object):
    u"""
    MeCab 形式
    表層形\t品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音

    を取り扱うクラス

    >>> k = Keitaiso(u'動か')
    >>> l = Keitaiso(u'動か')
    >>> m = Keitaiso(u'動く')
    >>> k.hyousoukei == u'動か'
    True
    >>> k.hinsi == u'動詞'
    True
    >>> k.hinsi1 == u'自立'
    True
    >>> k.hinsi2 == u'*'
    True
    >>> k.hinsi3 == u'*'
    True
    >>> k.katuyoukei == u'五段・カ行イ音便'
    True
    >>> k.katuyougata == u'未然形'
    True
    >>> k.genkei == u'動く'
    True
    >>> k.yomi == u'ウゴカ'
    True
    >>> k.hatuon == u'ウゴカ'
    True
    >>> k == l
    True
    >>> k == m
    False
    """
    def __init__(self, chasen_data):
        '''
        chasen_data: ChaSen 形式のデータの文字列
        count: 先読みの数

        '''
        self._chasen_data = chasen_data
        self._hyousoukei, self._hinsi, self._hinsi1, self._hinsi2, self._hinsi3, self._katuyoukei, self._katuyougata, self._genkei, self._yomi, self._hatuon = self._parse_keitaiso(chasen_data)

    def _get_chasen_data(self):
        return self._chasen_data
    def _get_hyousoukei(self):
        return self._hyousoukei
    def _get_hinsi(self):
        return self._hinsi
    def _get_hinsi1(self):
        return self._hinsi1
    def _get_hinsi2(self):
        return self._hinsi2
    def _get_hinsi3(self):
        return self._hinsi3
    def _get_katuyoukei(self):
        return self._katuyoukei
    def _get_katuyougata(self):
        return self._katuyougata
    def _get_genkei(self):
        return self._genkei
    def _get_yomi(self):
        return self._yomi
    def _get_hatuon(self):
        return self._hatuon

    def _parse_keitaiso(self, chasen_data):
        """
        """
        # t = MeCab.Tagger()
        # # [:-1] することで最後の空白をとりのぞく
        # res = t.parse(keitaiso.encode('utf-8')).split('\n')[:-1]

        # # 形態素が一つでないときはエラーをだす
        # for i in res:
        #     print i
        # assert len(res) == 2

        lst = chasen_data.split(u'\t')
        hyousoukei = lst[0]
        lst2 = lst[1].split(u',')

        ret_lst = [word for word in [hyousoukei] + lst2]
        lng = len(ret_lst)
        # 数値などは読みが加わらないのでそれを考慮する
        return ret_lst if lng == 10 else ret_lst + ['*'] * (10 - lng)

    def __cmp__(self, other):
        '''
        self とother が等しいかどうかを形態素の要素が全て等しいかどうかで定義する。
        '''
        return 0 if (self._hyousoukei == other._hyousoukei and \
                 self._hinsi == other._hinsi and \
                 self._hinsi1 == other._hinsi1 and \
                 self._hinsi2 == other._hinsi2 and \
                 self._hinsi3 == other._hinsi3 and \
                 self._katuyoukei == other._katuyoukei and \
                 self._katuyougata == other._katuyougata and \
                 self._genkei == other._genkei and \
                 self._yomi == other._yomi and \
                 self._hatuon == other._hatuon) \
               else 1

    def __hash__(self):
        return hash(self._get_chasen_data())

    def __str__(self):
        return self.__unicode__().encode('utf-8')

    def __unicode__(self):
        return u'{hy},{h},{h1},{h2},{h3},{kk},{kg},{g},{y},{ha}'.format(hy=self._hyousoukei, h=self._hinsi, h1=self._hinsi1, h2=self._hinsi2, h3=self.hinsi3, kk=self._katuyoukei, kg=self._katuyougata, g=self._genkei, y=self._yomi, ha=self._hatuon)

    chasen_data = property(_get_chasen_data)
    hyousoukei = property(_get_hyousoukei)
    hinsi = property(_get_hinsi)
    hinsi1 = property(_get_hinsi1)
    hinsi2 = property(_get_hinsi2)
    hinsi3 = property(_get_hinsi3)
    katuyoukei = property(_get_katuyoukei)
    katuyougata = property(_get_katuyougata)
    genkei = property(_get_genkei)
    yomi = property(_get_yomi)
    hatuon = property(_get_hatuon)

def str2keitaiso(st, cls=Keitaiso):
    u'''
    how to
        str2keitaiso(u'こんにちは。4/4 の今日は暑いですね。')
    '''

    t = MeCab.Tagger()
    # [:-1] することで最後のEOF をとりのぞく
    texts = t.parse(st.encode('utf-8')).rstrip('\n').split('\n')[:-1]
    return [cls(text.decode('utf-8')) for text in texts]


def str2wakati(st, cls=Keitaiso):
    return u" ".join([x.hyousoukei
                      for x in str2keitaiso(st, cls=Keitaiso)])


def keitaiso_similarity(klst1, klst2, obj_func=lambda x: 1):
    return sum(obj_func(item) for item in set(klst1).intersection(set(klst2)))

def similarity(str1, str2, cls=Keitaiso, obj_func=lambda x: 1):
    str1lst = str2keitaiso(str1, cls=cls)
    str2lst = str2keitaiso(str2, cls=cls)
    return keitaiso_similarity(str1lst, str2lst, obj_func=obj_func)

def _test():
    k = Keitaiso(u'動く\t動詞,自立,*,*,五段・カ行イ音便,基本形,動く,ウゴク,ウゴク')
    assert k.chasen_data == u'動く\t動詞,自立,*,*,五段・カ行イ音便,基本形,動く,ウゴク,ウゴク'
    assert k.hyousoukei == u'動く'
    assert k.hinsi == u'動詞'
    assert k.hinsi1 == u'自立'
    assert k.hinsi2 == u'*'
    assert k.hinsi3 == u'*'
    assert k.katuyoukei == u'五段・カ行イ音便'
    assert k.katuyougata == u'基本形'
    assert k.genkei == u'動く'
    assert k.yomi == u'ウゴク'
    assert k.hatuon == u'ウゴク'

    l = Keitaiso(u'1000\t名詞,数,*,*,*,*,*')
    assert l.chasen_data == u'1000\t名詞,数,*,*,*,*,*'
    assert l.hyousoukei == u'1000'
    assert l.hinsi == u'名詞'
    assert l.hinsi1 == u'数'
    assert l.hinsi2 == u'*'
    assert l.hinsi3 == u'*'
    assert l.katuyoukei == u'*'
    assert l.katuyougata == u'*'
    assert l.genkei == u'*'
    assert l.yomi == u'*'
    assert l.hatuon == u'*'

if __name__=='__main__':
    # doctest
    #import doctest
    #doctest.testmod()
    _test()

    # sample class for similarity
    class Test(Keitaiso):
        def __cmp__(self, other):
            return 0 if self._genkei == other._genkei else 1
        def __hash__(self):
            return hash(self._genkei)

    def testfunc(item):
        if item.hinsi == u'動詞':
            return 5
        elif item.hinsi == u'名詞':
            return 4
        else:
            return 1

    print similarity(u'動く', u'動かない', cls=Test)
