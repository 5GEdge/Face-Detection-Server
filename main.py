#!/usr/bin/env python


'''
face detection using haar cascades in remote fashion
'''

from __future__ import print_function
import urllib
import sys
from flask import Flask, render_template, Response, g
from detect_haar import face_detect, decode_detect_face
from cv_decoder import *
from cv_jpgencoder import *
from cv_haar_processor import *

app = Flask(__name__)


@app.route('/decode')
def decode():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    from flask import stream_with_context
    return Response(stream_with_context(cv_decode(stream)))

@app.route('/decode_detect')
def decode_detect():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    from flask import stream_with_context
    return Response(stream_with_context(decode_detect_face(stream)))


@app.route('/jpgencode')
def jpgencode():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    return Response(jpgencodestream(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/serve_face')
def serve_face():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    from flask import stream_with_context
    return Response(stream_with_context(face_detect_process(stream)))

@app.route('/video')
def video():
    streamurl = str(sys.argv[2])
    stream = urllib.urlopen(streamurl)
    return Response(face_detect(stream),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port, debug=True)