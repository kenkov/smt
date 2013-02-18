#! /usr/bin/env python
# coding:utf-8

'''
===============================
chartype.py
===============================

公開
=====

`github <https://github.com/kenkov/chartype.py>`_ で公開しています。

ドキュメント
====================

Unicode 型の文字列がどの種類の文字列(ひらがな、カタカナ、漢字など) なのかを判定するモジュール
'''

import unicodedata

class Chartype(object):
    u'''
    Chartype クラス

    '''
    def __init__(self):
        pass

    def _typename(self, st):
        '''
        :param st: ユニコード型の文字列
        :type st: ユニコード型
        :rtype: string
        :return: 文字の種類を表す文字列
        :except IOError: IOError がでる。
        '''
        if self.is_hiragana(st):
            return 'HIRAGANA'
        elif self.is_katakana(st):
            return 'KATAKANA'
        elif self.is_halfwidthkatakana(st):
            return 'HANKAKUKATAKANA'
        elif self.is_kanji(st):
            return 'KANJI'
        elif self.is_latinsmall(st):
            return 'LATINSMALL'
        elif self.is_latincapital(st):
            return 'LATINCAPITAL'
        elif self.is_digit(st):
            return 'DIGIT'
        elif self.is_kuten(st):
            return 'KUTEN'
        elif self.is_touten(st):
            return 'TOUTEN'

    def _is_type(self, typ, st, start, end):
        '''
        '''
        return unicodedata.name(st)[start: end] == typ

    def is_hiragana(self, st):
        u"""
        ひらがなかどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype: bool

        >>> ch = Chartype()
        >>> ch.is_hiragana(u'あ')
        True
        >>> ch.is_hiragana(u'ア')
        False
        """
        return self._is_type('HIRAGANA', st, 0, 8)

    def is_katakana(self, st):
        u"""
        カタカナかどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_katakana(u'ア')
        True
        >>> ch.is_katakana(u'あ')
        False
        """
        return self._is_type('KATAKANA', st, 0, 8)

    def is_halfwidthkatakana(self, st):
        u"""
        半角カタカナかどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_halfwidthkatakana(u'ｱ')
        True
        >>> ch.is_halfwidthkatakana(u'ア')
        False
        """
        return self._is_type('HALFWIDTH KATAKANA', st, 0, 18)

    def is_kanji(self, st):
        u"""
        漢字かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_kanji(u'漢')
        True
        >>> ch.is_kanji(u'か')
        False
        """
        return self._is_type('CJK', st, 0, 3)

    def is_latinsmall(self, st):
        u"""
        [a-z]* かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_latinsmall(u'a')
        True
        >>> ch.is_latinsmall(u'あ')
        False
        """
        return self._is_type('LATIN SMALL', st, 0, 11)

    def is_latincapital(self, st):
        u"""
        [A-Z]* かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_latincapital(u'A')
        True
        >>> ch.is_latincapital(u'a')
        False
        """
        return self._is_type('LATIN CAPITAL', st, 0, 13)

    def is_digit(self, st):
        u"""
        数値かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_digit(u'1')
        True
        >>> ch.is_digit(u'a')
        False
        """
        return self._is_type('DIGIT', st, 0, 5)

    def is_kuten(self, st):
        u"""
        『。』または『．』に一致するかどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_kuten(u'。')
        True
        >>> ch.is_kuten(u'.')
        True
        """
        return self._is_type('IDEOGRAPHIC FULL STOP', st, 0, 21) or self._is_type('FULLWIDTH FULL STOP', st, 0, 19) or self._is_type('FULL STOP', st, 0, 9)
    def is_touten(self, st):
        u"""
        『、』または『．』に一致するかどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_touten(u'、')
        True
        >>> ch.is_touten(u',')
        True
        """
        return self._is_type('IDEOGRAPHIC COMMA', st, 0, 17) or self._is_type('FULLWIDTH COMMA', st, 0, 15) or self._is_type('COMMA', st, 0, 5)

    # 上を組み合わせて新しいメソッドをつくる
    def is_latin(self, st):
        '''
        ラテン文字列かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_latin(u'a')
        True
        >>> ch.is_latin(u'A')
        True
        >>> ch.is_latin(u'1')
        False
        '''
        return self.is_latinsmall(st) or self.is_latincapital(st)
    def is_ascii(self, st):
        '''
        アスキー文字列かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_ascii(u'a')
        True
        >>> ch.is_ascii(u'A')
        True
        >>> ch.is_ascii(u'1')
        True
        '''
        return self.is_digit(st) or self.is_latin(st) 

    def is_kutouten(self, st):
        u'''
        句読点かどうかを判定する
        
        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_kutouten(u'。')
        True
        >>> ch.is_kutouten(u'.')
        True
        >>> ch.is_kutouten(u'、')
        True
        >>> ch.is_kutouten(u',')
        True
        '''
        return self.is_kuten(st) or self.is_touten(st)

    def is_nihongo(self, st):
        u'''
        日本語かどうかを判定する

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_nihongo(u'あ')
        True
        >>> ch.is_nihongo(u'a')
        False
        '''
        return self.is_hiragana(st) or \
               self.is_katakana(st) or \
               self.is_halfwidthkatakana(st) or \
               self.is_kanji(st) or \
               self.is_kuten(st) or \
               self.is_touten(st)
    def otherwise(self, st):
        u"""
        上の関数でTrueになる文字以外の文字

        :param unicode st: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.otherwise(u'!')
        True
        >>> ch.otherwise(u'！')
        True
        """
        return not (self.is_hiragana(st) or
                    self.is_katakana(st) or
                    self.is_halfwidthkatakana(st) or 
                    self.is_kanji(st) or 
                    self.is_latinsmall(st) or 
                    self.is_latincapital(st) or 
                    self.is_digit(st) or 
                    self.is_kuten(st) or 
                    self.is_touten(st))

    def is_sametype(self, st1, st2):
        u'''
        st1 とst2 が同じ文字列かどうかを判定する

        :param unicode st1: ユニコード型の文字列
        :param unicode st2: ユニコード型の文字列
        :rtype bool:

        >>> ch = Chartype()
        >>> ch.is_sametype(u'あ', u'あ')
        True
        >>> ch.is_sametype(u'あ', u'い')
        True
        '''
        return self._typename(st1) == self._typename(st2)

if __name__=='__main__':
    import doctest
    doctest.testmod()
