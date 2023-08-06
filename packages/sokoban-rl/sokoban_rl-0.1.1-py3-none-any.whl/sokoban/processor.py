import numpy as np
from skimage.transform import resize
from rl.core import Processor


class BaseCNNProcessor(Processor):

    """
    Processor for 4-Channel, Base-Image Input

    Description
        An input "observation" is a dict which contains 'nrow', 'ncol', 'player_position', 'box_position',
        'storage_position', and 'wall_position'. This module preprocesses this object to 4-channel 2D image.
        Each channel contains an binary(0 or 1) values, which means whether the corresponding location has a player, box, storage, and wall, respectively.
    
    Parameters
    ----------
    resolution : tuple(int)
        Shape of each channel of image for input of the CNN model
    """

    def __init__(self, resolution=(32, 32)):
        assert len(resolution) == 2
        self.state_space = (1,) + resolution + (4,)

        return

    def process_observation(self, observation):
        nrow = observation['nrow']
        ncol = observation['ncol']

        result = []
        for channel in ['player_position', 'box_position', 'storage_position', 'wall_position']:
            screen = np.zeros_like([False], shape=(nrow, ncol, 1), dtype='bool')
            position = observation[channel]
            position = position if isinstance(position, list) else [position]
            for pos in position:
                screen[pos // ncol, pos % ncol, 0] = 1
            cval = 1 if channel == 'wall_position' else 0
            screen = np.pad(screen, pad_width=1, mode='constant', constant_values=cval)
            screen = resize(screen, (self.state_space[1], self.state_space[2], 1))
            result.append(screen)
        result = np.concatenate(result, axis=2)

        return result


class POCNNProcessor(Processor):

    """
    Player-Oriented CNN Processor for 4-Channel Image Input

    Description
        An input "observation" is a dict which contains 'nrow', 'ncol', 'player_position', 'box_position',
        'storage_position', and 'wall_position'. This module preprocesses this object to 4-channel 2D image.
        Each channel contains an binary(0 or 1) values, which means whether the corresponding location has a player, box, storage, and wall, respectively.
        
        *** NOTE ***
        POCNNProcessor differs from BaseCNNProcessor in two areas:
            1. Rebalance the image so that the player's position is in the center.
            2. Take only the image of the radius "scope" and use it as an input for the cnn model.
    
    Parameters
    ----------
    scope : tuple(int)
        The radius of the image to be snatched. The first element is for height, the second element is for width.
        The size of the actual image taken is (2 * scope[0] + 1, 2 * scope[1] + 1).
    resolution : tuple(int)
        Shape of each channel of image for input of the CNN model
    """

    def __init__(self, scope=(5, 5), resolution=(15, 15)):
        assert len(resolution) == 2
        self.scope = scope
        self.screen_shape = (self.scope[0] * 2 + 1, self.scope[1] * 2 + 1, 1)
        self.channel_list = ['player_position', 'box_position', 'storage_position', 'wall_position']
        self.state_space = (1,) + resolution + (len(self.channel_list),)

        return

    def process_observation(self, observation):
        nrow = observation['nrow']
        ncol = observation['ncol']

        result = []
        player_position = observation['player_position']
        row_base, col_base = player_position // ncol, player_position % ncol
        row_center, col_center = self.scope
        for channel in self.channel_list:
            is_channel_wall = channel == 'wall_position'
            if is_channel_wall:
                screen = np.ones_like([], shape=self.screen_shape, dtype='bool')
                position = [i for i in range(nrow * ncol) if i not in observation[channel]]
            else:
                screen = np.zeros_like([], shape=self.screen_shape, dtype='bool')
                if channel == 'player_position':
                    position = [observation[channel]]
                else:
                    position = observation[channel]
            for pos in position:
                adjusted_row = pos // ncol - row_base + row_center
                adjusted_col = pos % ncol - col_base + col_center
                if 0 <= adjusted_row < self.screen_shape[0] and 0 <= adjusted_col < self.screen_shape[1]:
                    screen[adjusted_row, adjusted_col, 0] = int(not is_channel_wall)
            screen = resize(screen, (self.state_space[1], self.state_space[2], 1))
            result.append(screen)
        result = np.concatenate(result, axis=2)

        return result
