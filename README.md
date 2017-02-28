# Video Face Detection on server side using Flask

### Description
This piece of code aims to create a service that reads from a remote camera, performs face recognition processing and provides its results.

### Important
This code is created only for experimental purposes.

### Credits
This is a modified (joining) version of [Video Streaming with Flask Example][1] and the [open cv face recognition][2]

### Usage
1. Install Python dependencies: cv2, flask.
2. Run "python main.py" followed by your image address. Example:
```
  python main.py http://96.10.1.168/mjpg/1/video.mjpg
```

3. On your browser, navigate to the address given in the console.



[1]:https://github.com/log0/video_streaming_with_flask_example
[2]:https://github.com/opencv/opencv
