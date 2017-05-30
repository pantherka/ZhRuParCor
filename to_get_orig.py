#!/usr/bin/env python
#coding=utf8
# A script to compare parallel texts in TMX and XML
# @author @netbug aka Oleg Urzhumtcev

from XML_compare import *

if __name__ == '__main__':
    f_orig = 'data/mumu.xml'
    langs1, t_orig = read_file(f_orig)
    print("Read %d lines " % len(t_orig))
    with open('MumuGS_r.txt', 'w') as fh:
      fh.write('\n'.join([i[1] for i in t_orig]))
    with open('MumuGS_zh.txt', 'w') as fh:
      fh.write('\n'.join([i[0].replace(' ', '') for i in t_orig]))