import gym
import numpy as np

from temporalPooler.htm__region import Region as TemporalPoolerRegion
from apps.settings import *
from dlpf.agents import RandomAgent
from dlpf.io import *
from main_chain_extractor import Foo
from main_image_drawer import draw_image

import_tasks_from_xml_to_compact('data/sample/raw/', 'data/sample/imported/')

env = gym.make('PathFindingByPixel-v2')
env.configure(tasks_dir=os.path.abspath('data/sample/imported/'), monitor_scale=10, map_shape=(10, 10))
env.monitor.start('data/sample/results/basic_dqn', force=True, seed=0)

size = 10
temporal_settings = TemporalSettings(region_size=size, column_size=1, initial_permanence=0.5,
                                     dendrite_activate_threshold=1, dendrite_permanence_inc_delta=0.02,
                                     dendrite_permanence_dec_delta=-0.1, passive_time_to_active_threshold=1000,
                                     synapse_threshold=0.45)

temporal_pooler_region = TemporalPoolerRegion(temporal_settings=temporal_settings)
agent = RandomAgent(env.action_space.n)


def transform_reward_to_weight_inc(reward_):
    if reward_ == -1:   return -0.05
    if reward_ == -0.1: return -0.01
    if reward_ == 0:    return 0.008
    if reward_ == 1:    return 0.4  # 0.02
    if reward_ == 10:   return 0.9  # 0.03
    raise ValueError


def transform_reward_to_weight_dec(reward_):
    if reward_ == -1:   return -1
    if reward_ == -0.1: return -1
    if reward_ == 0:    return -1
    if reward_ == 1:    return -0.01
    if reward_ == 10:   return -0.01
    raise ValueError


BY_PIXEL_ACTION_DIFFS = {
    0: [-1, 0],
    1: [-1, 1],
    2: [0, 1],
    3: [1, 1],
    4: [1, 0],
    5: [1, -1],
    6: [0, -1],
    7: [-1, -1]
}

episode_count = 5000
max_steps = 100
ss = set()

for i in range(8):
    print("----" * 5)
    obs = env.reset()
    x, y = env.cur_position_discrete
    print(x, y)
    obs, reward, done, info = env.step(i)
    x, y = env.cur_position_discrete
    print(x, y)

    print(reward)
exit(0)
