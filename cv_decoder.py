#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np

import pickle, time


def cv_decode(stream):
    print(__doc__)

    bytes=''

    while True:

        bytes+=stream.read(16384)
        a = bytes.find('\xff\xd8')
        b = bytes.find('\xff\xd9')

        if a != -1 and b != -1:
            # print (time.time())
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), 1)
            pickled = pickle.dumps(i, protocol=0)
            # print(time.time())
            # print (len(pickled))
            #
            # print(bytes.count('\xff\xd8'))

            yield ("[start]" + pickled + "[finish]")

            # print(time.time())
            if cv2.waitKey(5) == 27:
                break