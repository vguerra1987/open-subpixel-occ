import cv2 as cv


def stream_camera(downlink, uplink):

    cam = cv.VideoCapture(0)
    cam.set(cv.CAP_PROP_FPS, 30)

    while True:
        _, frame = cam.read()
        uplink.put(frame)
