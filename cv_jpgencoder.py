#!/usr/bin/env python

# Python 2/3 compatibility
from __future__ import print_function

import cv2
import numpy as np
import pickle, time

def jpgencodestream(stream):
    print(__doc__)
    bytes=''
    i = 0
    while True:
        # print(time.time())
        bytes += str(stream.read(163840))
        a = bytes.find('[start]')
        b = bytes.find('[finish]')


        if a != -1 and b != -1:
            # print(bytes[a+6:20])
            # print(time.time())
            jpg = bytes[a + 7:b]
            bytes = bytes[b + 8:]

            # print ("Value of a" + str(b))
            # print (len(bytes))
            # print (bytes[0:5])
            # print("to_process")
            # print(bytes.count('[finish]'))
            img = pickle.loads(jpg)

            r, buf = cv2.imencode(".jpg", img)

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + np.ndarray.tostring(buf) + b'\r\n\r\n')
            # print(time.time())

            if cv2.waitKey(5) == 27:
                break

