import gym
from copy import deepcopy
from .moving import SokobanMoving
from .utils import Logger


class AllActionsEnv(gym.Env):

    """
    A class inherited from gym.Env, especially optimized for Sokoban Reinforcement Learning

    Description
        In this module, the actions for each step are always fixed to four in any cases of state.

    Parameters
    ----------
    episode_sampler : Type[BaseSampler] or None
        Any class inherited from basesampler. See help(BaseSampler).
        If None, an agent in keras-rl2 cannot run the environment. Users must manually place episodes in their environment each time reset() runs.
    max_steps : int
        The maximum number of steps allowed in one episode
    history_dir : None or str
        Directory to write learning logs (do not write learning logs if None)
    """

    def __init__(self, episode_sampler=None, max_steps=60, history_dir=None):
        # Inputs
        self.EPISODE_SAMPLER = episode_sampler
        self.MAX_STEPS = max_steps
        self.HISTORY_DIR = history_dir

        # Settings
        self.n_episodes = -1
        self.n_total_steps = 0
        self.n_step = 0
        self.now_state = None
        self.mover = None
        self.action_decoder = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
        self.action_space = gym.spaces.Discrete(len(self.action_decoder))
        self.log_yn = self.HISTORY_DIR is not None

        # Logger
        self.log_handler = {}
        if self.log_yn:
            for prefix in ['step', 'reset']:
                self.log_handler[prefix] = Logger()
                self.log_handler[prefix].get_logger(self.HISTORY_DIR, prefix)
                print(f"AllActionsEnv create file {self.log_handler[prefix].path_output}")

        return

    def reset(self, episode=None, **kwargs):
        # Reset index
        self.n_episodes += 1
        self.n_step = 0

        # Episode sampling
        if episode is None:
            # Train mode : The sampler samples episode
            self.now_state = self.EPISODE_SAMPLER.sample(n_total_steps=self.n_total_steps)
        else:
            # Test mode : User put episode manually in environment
            self.now_state = deepcopy(episode)
        self.mover = SokobanMoving(nrow=self.now_state['nrow'],
                                   ncol=self.now_state['ncol'],
                                   storage_position=self.now_state['storage_position'],
                                   wall_position=self.now_state['wall_position'])

        # Initial observation
        observation = deepcopy(self.now_state)

        # Logging
        if self.log_yn:
            logger_comment = f"EPI: {self.n_episodes}, " \
                             f"NROW: {observation['nrow']}, NCOL: {observation['ncol']}, " + \
                             f"PLAYER: {observation['player_position']}, BOX: {observation['box_position']}, " + \
                             f"STORAGE: {observation['storage_position']}, WALL: {observation['wall_position']}"
            self.log_handler['reset'].write(logger_comment)

        return observation

    def step(self, action):
        # Now state
        now_pos = self.now_state['player_position']
        now_box = self.now_state['box_position']
        direction = self.action_decoder[action]
        storages = self.now_state['storage_position']
        now_success = sum([int(box in storages) for box in now_box])

        # Moving
        movable, next_pos, next_box = self.mover.do_action(now_pos, now_box, direction)
        next_success = sum([int(box in storages) for box in next_box])

        # Reward
        if not movable:
            # Attempt to move where it can't reach
            reward = -1.0
        elif now_success + 1 == next_success:
            # Get the box on storage
            reward = 5.0
        elif now_success - 1 == next_success:
            # Get the box out of storage
            reward = -4.5
        elif next_pos in now_box:
            # Move the box
            reward = 1.0
        else:
            # Others
            reward = -0.1

        # Terminate condition
        if not movable:
            # Attempt to move where it can't reach
            done = True
            done_reason = 'block'
        elif self.n_step > self.MAX_STEPS - 2:
            # Exceeded the specified maximum number of steps
            done = True
            done_reason = 'step'
        elif (now_success == len(storages)) or (next_success == len(storages)):
            # Get all the boxes on storage
            done = True
            done_reason = 'finish'
        elif self.mover.is_boxes_stuck(next_box):
            # Any of the boxes are stucked
            done = True
            done_reason = 'stuck'
        else:
            done = False
            done_reason = 'none'

        # Logging
        if self.log_yn:
            logger_comment = f"EPI: {self.n_episodes}, " \
                             f"STEP: {self.n_step}, PLAY: {now_pos} -> {next_pos} ({direction.upper()}), " + \
                             f"BOX: {now_box} -> {next_box}, REWARD: {reward}, DONE_REASON: {done_reason}"
            self.log_handler['step'].write(logger_comment)

        # Next state
        self.now_state['player_position'] = next_pos
        self.now_state['box_position'] = next_box
        observation = deepcopy(self.now_state)
        self.n_total_steps += 1
        self.n_step += 1
        info = {}

        return observation, reward, done, info
