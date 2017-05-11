#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import print_function

import cv2, pickle
import numpy as np


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


def face_detect_process(stream):
    import sys, getopt
    print(__doc__)

    args, video_src = getopt.getopt(sys.argv[1:], '', ['cascade=', 'nested-cascade='])
    args = dict(args)

    cascade_fn = args.get('--cascade', "haarcascades/haarcascade_frontalface_alt.xml")
    # nested_fn  = args.get('--nested-cascade', "haarcascades/haarcascade_eye.xml")

    cascade = cv2.CascadeClassifier(cascade_fn)
    # nested = cv2.CascadeClassifier(nested_fn)
    bytes=''

    while True:
        bytes+=stream.read(16384)
        a = bytes.find('[start]')
        b = bytes.find('[finish]')

        if a != -1 and b != -1:
            jpg = bytes[a + 7:b]
            bytes = bytes[b + 8:]
            img = pickle.loads(jpg)

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.equalizeHist(gray)
            rects = detect(gray, cascade)
            vis = img.copy()
            draw_rects(vis, rects, (0, 255, 0))
            # if not nested.empty():
            #     for x1, y1, x2, y2 in rects:
            #         roi = gray[y1:y2, x1:x2]
            #         vis_roi = vis[y1:y2, x1:x2]
            #         subrects = detect(roi.copy(), nested)
            #         draw_rects(vis_roi, subrects, (255, 0, 0))

            # r, buf = cv2.imencode(".jpg", vis)

            pickled = pickle.dumps(vis, protocol=0)

            yield ("[start]" + pickled + "[finish]")

            if cv2.waitKey(5) == 27:
                break