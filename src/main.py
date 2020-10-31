#!/usr/bin/python

import sys
import morfeusz2

if __name__ == '__main__':
    morf = morfeusz2.Morfeusz()
    text = u'Jaś miał kota'
    print(text)
    analysis = morf.analyse(text)
    for interpretation in analysis:
        print(interpretation)