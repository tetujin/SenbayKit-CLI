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
from pyzbar.pyzbar import decode
from PIL import Image
from mss import mss
import os
from datetime import datetime

# import core as sd
from senbay import SenbayData


class SenbayReader:

    reader_mode  = 0
    video_input  = None
    camera_input = 0
    preview_input = True
    mode = 0 # 0=video, 1=camera, 2=screen
    cap_area = None #{'top': 160, 'left': 160, 'width': 200, 'height': 200}
    sct  = None
    monitor_num = 1
    rescan_limit = 100
    rescan_count = 0

    # For measuring FPS
    last_ts = 0
    cur_ts  = 0
    frames  = 0
    fps     = None
    fps_monitor = None

    def __init__(self, mode=0, video_in=None, camera_in=0, cap_area=None, preview_in=True):
        self.reader_mode    = mode
        self.video_input    = video_in
        self.camera_input   = camera_in
        self.preview_input  = preview_in
        self.cap_area       = cap_area

    def set_capture_are(self, top=0, left=0, width=0, height=0):
        self.cap_area = {'top': top, 'left': left, 'width': width, 'height': height}

    def set_fps_monitor(self, monitor):
        self.fps_monitor = monitor

    def start(self, observer):
        if self.reader_mode == 0 or self.reader_mode == 'video':
            cap = cv2.VideoCapture(self.video_input)
            self.reader_mode = 0
        elif self.reader_mode == 1 or self.reader_mode == 'camera':
            cap = cv2.VideoCapture(self.camera_input)
            self.reader_mode = 1
        elif self.reader_mode == 2 or self.reader_mode == 'screen':
            self.reader_mode = 2
            sct = mss()
        else:
            print('error: The mode value should be taken 0(=video), 1(=camera), or 2(=screen).')
            return


        codes = None
        senbayData = SenbayData()

        if self.reader_mode == 0 or self.reader_mode == 1:
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
                    if codes != None and len(codes) > 0:
                        # print(codes[0].decode('utf-8'))
                        senbayDict = senbayData.decode(str(codes[0].decode('utf-8')))
                        observer(self, senbayDict);
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except ValueError:
                    print("Error")

        elif self.reader_mode == 2:
            while True:
                # capture screen
                # print(sct.monitors)
                sct_img = None
                if (self.cap_area == None):
                    sct_img = sct.grab(sct.monitors[self.monitor_num])
                    print(sct.monitors[self.monitor_num])
                else:
                    sct_img = sct.grab(self.cap_area)

                ### generate an image
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
                if self.preview_input:
                    cv2.imshow('frame', np.array(img))


                if self.cap_area == None:
                    data = decode(img)
                    if len(data) > 0:
                        qr_rect = data[0].rect

                        self.set_capture_are(top=qr_rect.top, left=qr_rect.left, width=qr_rect.width, height=qr_rect.height)

                        if zl.scan_codes('qrcode', img) == None:
                            self.set_capture_are(top=qr_rect.top/2, left=qr_rect.left/2, width=qr_rect.width/2, height=qr_rect.height/2)
                            print("is retina")
                        else:
                            print("is not retina")

                codes = zl.scan_codes('qrcode', img)
                if codes != None and len(codes) > 0:
                    # print(codes[0].decode('utf-8'))
                    senbayDict = senbayData.decode(str(codes[0].decode('utf-8')))
                    observer(self, senbayDict)

                    # FPS
                    if self.cur_ts == 0:
                        self.cur_ts  = datetime.now().timestamp()
                        self.last_ts = self.cur_ts
                    else:
                        self.cur_ts = datetime.now().timestamp()
                        self.frames = self.frames + 1
                        # print(self.cur_ts - self.last_ts)
                        if self.cur_ts - self.last_ts > 1:
                            self.fps = self.frames
                            if self.fps_monitor != None:
                                self.fps_monitor(self, self.fps)
                            self.frames = 0
                            self.last_ts = self.cur_ts

                    self.rescan_count = 0
                else:
                    self.rescan_count = self.rescan_count + 1
                    if self.rescan_count > self.rescan_limit:
                        self.cap_area = None
                        self.rescan_count = 0
                # print(self.rescan_count, self.cap_area)

                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

        cap.release()
        cv2.destroyAllWindows()
