import render
import numpy as np

dataset = [
    np.array([
        [[255, 0, 0], [255, 0, 0]],  # red intensities
        [[0, 255, 0], [0, 255, 0]],  # green intensities
        [[0, 0, 255], [0, 0, 255]]   # blue intensities
    ]),
    np.array([
        [[0, 0, 255], [0, 0, 255]],
        [[0, 255, 0], [0, 255, 0]],
        [[255, 0, 0], [255, 0, 0]]
    ])
]

render.animate(dataset)
