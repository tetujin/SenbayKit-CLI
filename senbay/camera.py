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
import threading
import qrcode
from PIL import Image
from datetime import datetime

class ActivePool(object):
    video_output = None;
    pre_time = 0;
    def __init__(self, video_output):
        super(ActivePool, self).__init__()
        self.active = []
        self.lock = threading.Lock()
        self.video_output = video_output;

    def lockAndWriteFrame(self, frame, name, now):
        with self.lock:
            if self.pre_time < now:
                # self.active.append(name)
                self.video_output.write(frame)
                # print('Running: %s', self.active)
                self.pre_time = now
                # cv2.imshow('frame',frame)
#            else:
#                print('Skipping: %s', self.active);
    #def unLock(self, name):
        #with self.lock:
        #    print('Unlock');
            # self.active.remove(name)


class SenbayThread(threading.Thread):
    video_output = None;
    w = 640;
    h = 360;
    frame = None;
    data = None;
    qr_maker = None;
    pool = None;

    def __init__(self, video_output, w, h, frame, data, pool):
        super(SenbayThread, self).__init__()
        self.pool = pool;
        self.video_output = video_output;
        self.w = w;
        self.h = h;
        self.frame = frame;
        self.data = data;
        self.qr_maker = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=3,
                border=1
                )

    def run(self):
        self.qr_maker.add_data(self.data)
        self.qr_maker.make(fit=True)
        qrimg = self.qr_maker.make_image()
        self.qr_maker.clear()

        pil_image = qrimg.convert('RGB')
        img2 = np.array(pil_image)
        img2 = img2[:, :, ::-1].copy()

        # Our operations on the frame come here
        img1 = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        # Overlay an image (QR code) to a base image
        img1 = self.overlayOnPart(img1, img2, 0, 0);

        name = threading.currentThread().getName()
        now = time.time()
        self.pool.lockAndWriteFrame(img1,name,now);

    # pool.unLock(name);

    # PILを使って画像を合成
    def overlayOnPart(self, src_image, overlay_image, posX, posY):
        # オーバレイ画像のサイズを取得
        ol_height, ol_width = overlay_image.shape[:2]
        # OpenCVの画像データをPILに変換
        #　BGRAからRGBAへ変換
        src_image_RGBA = src_image # cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB)
        #src_image_RGBA = cv2.cvtColor(src_image,0)
        #overlay_image_RGBA = cv2.cvtColor(overlay_image, cv2.COLOR_BGRA2RGBA)
        #overlay_image_RGBA = cv2.cvtColor(overlay_image,0)
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
        tmp.paste(overlay_image_PIL, (posX, posY), overlay_image_PIL)
        # オリジナルとキャンパスを合成して保存
        result = Image.alpha_composite(src_image_PIL, tmp)

        # COLOR_RGBA2BGRA から COLOR_RGBA2BGRに変更。アルファチャンネルを含んでいるとうまく動画に出力されない。
        return  cv2.cvtColor(np.asarray(result), cv2.COLOR_RGBA2BGR)
        #return  cv2.cvtColor(np.asarray(result), 0)

class SenbayCamera:
    width  = 640
    height = 360
    fps = 30 # fps
    max_trehad = 10 # threading
    camera_number  = None
    video_path = None
    video_out = None
    pool = None
    debug = False

    ESC_KEY  = 27     # Escキー
    interval = 10     # 待ち時間

    def __init__(self, camera_number=0, video_path='senbay_video_output.m4v', width=640, height=360, fps=30, max_trehad = 10, debug=False):
        self.camera_number = camera_number;
        self.video_path = video_path;
        self.height = height;
        self.width = width;
        self.fps = fps;
        self.max_trehad = max_trehad;
        self.debug = debug;

    def start(self, delegate, completion, preview=True):

        camera_in = cv2.VideoCapture(self.camera_number)

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        video_out = cv2.VideoWriter(self.video_path, fourcc, self.fps,(self.width, self.height))

        self.pool = ActivePool(video_out);

        while(camera_in.isOpened()):
            '''
            def delegatedMethod(self):
                sd = SenbayData.SenbayData(122);
                now = time.time()
                sd.addNumber("TIME",now)
                data = sd.getSenbayFormattedData(True);
                return data;
            '''
            content = delegate();
            # if self.debug:
            #     print("[SenbayCamera] content: " + content)

            # Capture frame-by-frame
            ret, frame = camera_in.read()
            frame = cv2.resize( frame, (self.width, self.height))
            if ret==False:
                break

            if threading.active_count() < self.max_trehad:
                senbay_th = SenbayThread(video_out,
                                        self.width,
                                        self.height,
                                        frame,
                                        content,
                                        self.pool);
                senbay_th.start()

            key = cv2.waitKey(self.interval) & 0xFF
            if key is self.ESC_KEY:
                break

            # if self.debug:
            #     print(threading.active_count())

            if preview is True:
                cv2.imshow('frame',frame)

        # When everything done, release the capture
        camera_in.release()
        video_out.release()
        cv2.destroyAllWindows()
        completion()
