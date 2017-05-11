#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np
import pickle

def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects


def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


def face_detect(stream):
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    args = dict(args)

    cascade_fn = args.get('--cascade', "haarcascades/haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', "haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)

    bytes=''

    while True:
        bytes+=stream.read(16384)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)

            img = i
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            rects = detect(gray, cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))


            r, buf = cv2.imencode(".jpg", vis)
            
            cv2.imshow('image',vis)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + np.ndarray.tostring(buf) + b'\r\n\r\n')

            if cv2.waitKey(5) == 27:
                break

def decode_detect_face(stream):
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    args = dict(args)

    cascade_fn = args.get('--cascade', "haarcascades/haarcascade_frontalface_alt.xml")
    nested_fn  = args.get('--nested-cascade', "haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)

    bytes=''

    while True:
        bytes+=stream.read(16384)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)

            img = i
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            rects = detect(gray, cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))


            r, buf = cv2.imencode(".jpg", vis)

            pickled = pickle.dumps(vis, protocol=0)

            yield ("[start]" + pickled + "[finish]")

            if cv2.waitKey(5) == 27:
                break