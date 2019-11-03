import sys
sys.path.append('../hallucinator')
import numpy as np
import hallucinator as hl
import random


def sparkle(h, w, frames, repetions=1):
    h = random.randint(0, h-1)
    w = random.randint(0, w-1)
    t = []
    for i in range(repetions):
        t.append(random.randint(0, frames-duration))
    return h, w, t


height = 500
width = 500
num_frames = 500
num_sparkles = 2000
duration = 3

frames = []


for i in range(num_frames):
    frames.append(np.zeros((height, width)))

for i in range(num_sparkles):
    h, w, t = sparkle(height, width, num_frames, repetions=1)
    for time in t:
        for j in range(duration):
            frames[time+j][h][w] = 255
        frames[time] = frames[time].astype(np.uint8)


def return_frame(frame):
    return frames[frame]


frame_arguments = range(num_frames)

hl.video2(frame_func=return_frame,
          frame_arguments=frame_arguments,
          filename="./videos/sparkles",
          fps=15)

