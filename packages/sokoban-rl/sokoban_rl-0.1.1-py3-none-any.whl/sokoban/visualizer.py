import numpy as np


def get_image_numpy(epi):

    """
    A function that converts dictionary-type episodes into numpy ndarray image forms.
    """

    nrow = epi['nrow']
    ncol = epi['ncol']
    player_position = epi['player_position']
    box_position = epi['box_position']
    storage_position = epi['storage_position']
    wall_position = epi['wall_position']

    image = np.ones((nrow, ncol, 3))
    for position, rgb_code in zip([storage_position, [player_position], box_position, wall_position],
                                  [[0, 1, 0], [0, 0, 1], [1, 0, 0], [0, 0, 0]]):
        for pos in position:
            image[pos // ncol, pos % ncol, :] = rgb_code
    return image
