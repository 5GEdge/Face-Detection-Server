#!/usr/bin/env python


'''
face detection using haar cascades in remote fashion
'''

from __future__ import print_function
import urllib
import sys
from flask import Flask, render_template, Response, g
from detect_haar import face_detect

app = Flask(__name__)


@app.route('/video')
def video():
    streamurl = str(sys.argv[1])
    stream = urllib.urlopen(streamurl)
    return Response(face_detect(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)