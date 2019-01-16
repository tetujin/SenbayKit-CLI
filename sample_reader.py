#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 06:17:17 2019

@author: Yuuki Nishiyama
"""

import sys
from senbay import SenbayReader

if __name__ == '__main__':

    if len(sys.argv[1:]) < 4:
        print('-----------------------------')
        print('[Error]   Please set a capture area as arguments')
        print('[Example] $ ./sample_reader.py 100 100 200 200')
        print('------------------------------')
    else:
        top    = sys.argv[1]
        left   = sys.argv[2]
        width  = sys.argv[3]
        height = sys.argv[4]

        print("top:"+top+", left:"+left+", width:"+width+", height:"+height)

        cap_area = {'top':int(top), 'left':int(left), 'width':int(width), 'height':int(height)}

        def showResult(self, data):
            print(data)

        reader = SenbayReader(mode='screen', cap_area=cap_area)
        reader.start(showResult)
