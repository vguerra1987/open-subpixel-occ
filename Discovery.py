import enum
import time
from matplotlib import pyplot as plt
import numpy as np
import cv2


class Status(enum.Enum):
    buffering = 1
    processing = 2


def discover(downlink, uplink, frame_shape, buffer_length):
    buffer = np.zeros((frame_shape[0], frame_shape[1], buffer_length))
    status = Status.buffering
    counter = 0

    while True:

        if status == Status.buffering:
            buffer[:, :, counter] = cv2.cvtColor(downlink.get(), cv2.COLOR_BGR2GRAY)
            counter += 1
            if counter >= buffer.shape[-1]:
                counter = 0
                status = Status.processing

        elif status == Status.processing:
            print('Processing started')
            STD = np.std(buffer, axis=2)
            mega_point = np.argwhere(STD == np.max(STD.flatten()))[0]
            plt.plot(buffer[mega_point[1], mega_point[0], :])
            plt.show()
            status = Status.buffering

