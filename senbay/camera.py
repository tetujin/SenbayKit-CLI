#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 06:17:17 2017

@author: Yuuki Nishiyama
"""

import sys

import numpy as np
import cv2
import time
import qrcode
from PIL import Image
from datetime import datetime

class SenbayFrame:
    w = 640;
    h = 360;
    frame = None;
    data = None;
    qr_maker = None;

    def __init__(self, w, h, frame, data):
        self.w = w;
        self.h = h;
        self.frame = frame;
        self.data = data;
        self.qr_maker = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1
                )

    def gen(self):
        self.qr_maker.add_data(self.data)
        self.qr_maker.make(fit=True)
        qrimg = self.qr_maker.make_image()
        self.qr_maker.clear()

        pil_image = qrimg.convert('RGB')
        qr_layer = np.array(pil_image)
        qr_layer = qr_layer[:, :, ::-1].copy()

        # Our operations on the frame come here
        base_layer = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        # Overlay an image (QR code) to a base image
        return self.overlay(base_layer, qr_layer, 0, 0)

    # PILを使って画像を合成
    def overlay(self, src_image, overlay_image, pos_x, pos_y):
        # オーバレイ画像のサイズを取得
        ol_height, ol_width = overlay_image.shape[:2]
        # OpenCVの画像データをPILに変換
        #　BGRAからRGBAへ変換
        src_image_RGBA = src_image
        overlay_image_RGBA = overlay_image

        #　PILに変換
        src_image_PIL=Image.fromarray(src_image_RGBA)
        overlay_image_PIL=Image.fromarray(overlay_image_RGBA)

        # 合成のため、RGBAモードに変更
        src_image_PIL = src_image_PIL.convert('RGBA')
        overlay_image_PIL = overlay_image_PIL.convert('RGBA')

        # 同じ大きさの透過キャンパスを用意
        tmp = Image.new('RGBA', src_image_PIL.size, (255, 255, 255, 0))
        # 用意したキャンパスに上書き
        tmp.paste(overlay_image_PIL, (pos_x, pos_y), overlay_image_PIL)
        # オリジナルとキャンパスを合成して保存
        result = Image.alpha_composite(src_image_PIL, tmp)

        # COLOR_RGBA2BGRA から COLOR_RGBA2BGRに変更。アルファチャンネルを含んでいるとうまく動画に出力されない。
        return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)
        #return  cv2.cvtColor(np.asarray(result), 0)

class SenbayCamera:
    width  = 640
    height = 360
    fps = 30 # fps
    camera_number  = None
    video_output = None
    video_out = None
    debug = False

    ESC_KEY  = 27     # Escキー
    interval = 10     # 待ち時間

    preview = True
    stdout = False

    content_handler = None
    completion_handler = None
    frame_handler = None

    def __init__(self, camera_number=0, video_output=None, width=640, height=360, fps=30, debug=False, preview=True, stdout=False, content_handler=None, completion_handler=None, frame_handler=None):
        self.camera_number = camera_number
        self.video_output =video_output
        self.height = height
        self.width = width
        self.fps = fps
        self.debug = debug
        self.preview = preview
        self.stdout = stdout
        self.content_handler = content_handler
        self.completion_handler = completion_handler
        self.frame_handler = frame_handler

    def start(self):

        camera_in = cv2.VideoCapture(self.camera_number)

        # http://www.fourcc.org/codecs.php
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # fourcc = cv2.VideoWriter_fourcc(*'XVID') ##  XVID: XVID MPEG-4

        if self.video_output != None:
            video_out = cv2.VideoWriter(self.video_output, fourcc, self.fps,(self.width, self.height))

        while(camera_in.isOpened()):
            '''
            def content_handler(self):
                sd = SenbayData.SenbayData(121);
                now = time.time()
                sd.addNumber("TIME",now)
                data = sd.getSenbayFormattedData(True);
                return data;
            '''
            if self.content_handler != None:
                data = self.content_handler()
            else:
                data = ""

            # Capture frame-by-frame
            ret, frame = camera_in.read()
            frame = cv2.resize(frame, (self.width, self.height))
            frame = cv2.flip(frame,1)
            if ret==False:
                break

            # handling frame
            if self.frame_handler != None:
                frame = self.frame_handler(frame)

            # generate a Senbay Frame
            sbframe = SenbayFrame(self.width, self.height, frame, data);
            senbay_frame = sbframe.gen()

            # preview
            if self.preview == True:
                cv2.imshow('frame', senbay_frame)

            # video out put
            if self.video_output != None:
                video_out.write(senbay_frame)

            # stdout
            if self.stdout == True:
                sys.stdout.buffer.write(senbay_frame.tobytes())

            key = cv2.waitKey(self.interval) & 0xFF
            if key is self.ESC_KEY:
                break

        # When everything done, release the capture
        camera_in.release()
        if self.video_output != None:
            video_out.release()
        cv2.destroyAllWindows()
        if self.completion_handler != None:
            self.completion_handler()
