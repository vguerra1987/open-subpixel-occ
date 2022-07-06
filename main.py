import enum
import multiprocessing as mp
import time
import numpy as np
import Camera
import cv2

import Discovery
import Processor

downlink = mp.Queue()
uplink = mp.Queue()

disc_downlink = mp.Queue()
disc_uplink = mp.Queue()

capture_process = mp.Process(target=Camera.stream_camera, args=(downlink, uplink))
capture_process.start()

discovery_process = mp.Process(target=Discovery.discover, args=(disc_downlink, disc_uplink, [480, 640], 150))
# discovery_process.start()

ACTIVATE_VIEWER = True


# Class to enumerate the different status of the receiver finite state machine #
class Status(enum.Enum):
    UNDISCOVERED = 1
    UNCALIBRATED = 2
    TRACK_AND_RECEIVE = 3
# ---------------------------------------------------------------------------- #


current_status = Status.UNDISCOVERED
processors = []


def get_xy(event, x, y, flags, param):
    global processors
    if event == cv2.EVENT_LBUTTONDOWN:
        temp_queue = mp.Queue()
        processors.append({'point': [x, y],
                           'queue': temp_queue,
                           'process': mp.Process(target=Processor.decode, args=(temp_queue, len(processors)))})
        processors[-1]['process'].start()


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', get_xy)

while True:
    time_ref = time.time()
    frame = uplink.get()

    if ACTIVATE_VIEWER:
        frame = cv2.resize(cv2.resize(frame, [64, 48], interpolation=cv2.INTER_AREA), [640, 480], interpolation=cv2.INTER_NEAREST_EXACT)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)

    if current_status == Status.UNDISCOVERED:
        disc_downlink.put(frame)
        if len(processors) == 2:
            current_status = Status.UNCALIBRATED

    elif current_status == Status.UNCALIBRATED:
        cv2.setMouseCallback('frame', lambda *args: None)
        current_status = Status.TRACK_AND_RECEIVE

    elif current_status == Status.TRACK_AND_RECEIVE:
        for proc in processors:
            proc['queue'].put(frame[proc['point'][1], proc['point'][0], 2])
