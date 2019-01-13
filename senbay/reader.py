#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 16:54:04 2017

Senbay Reader

@author: Yuuki Nishiyama
"""

import sys

import numpy as np
import cv2
import fastzbarlight as zl
from PIL import Image

# import core as sd
from senbay import SenbayData

class SenbayReader:

    input = None;

    def __init__(self, input):
        self.input    = input;

    def start(self, observer):
        cap = cv2.VideoCapture(self.input)

        codes = None
        senbayData = SenbayData()

        while(cap.isOpened()):

            ret, frame = cap.read()

            if ret==False:
                continue
                #break
            try:
                normal = cv2.cvtColor(frame, 0)
                cv2.imshow('frame',normal)

                image = Image.fromarray(np.uint8(frame))

                codes = zl.scan_codes('qrcode', image)
                if len(codes) > 0:
                    # print(codes[0].decode('utf-8'))
                    senbayDict = senbayData.getSenbayDataAsDect(str(codes[0].decode('utf-8')))
                    observer(self, senbayDict);
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except ValueError:
                print("Error")

        cap.release()
        cv2.destroyAllWindows()
