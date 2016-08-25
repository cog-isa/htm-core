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

episode_count = 222
max_steps = 100
ss = set()

for current_episode in range(episode_count):
    obs = env.reset()
    cur_reward = 0
    x, y = env.cur_position_discrete
    finish = env.cur_task.finish
    # print("start:", x, y)
    # if current_episode * 2 > episode_count:
    # print("BEGIN" * 5)
    P = [[0 for ___ in range(size)] for _____ in range(size)]

    a = np.zeros(shape=(10, 10))
    tx, ty = env.cur_position_discrete
    a[tx, ty] = 1
    temporal_pooler_region.step_forward(a)

    for current_step in range(max_steps):

        p = temporal_pooler_region.get_binary_prediction()
        p_actions = []
        x, y = env.cur_position_discrete
        P[x][y] = 1
        for i in BY_PIXEL_ACTION_DIFFS:
            dx, dy = BY_PIXEL_ACTION_DIFFS[i]
            try:
                if p[x + dx][y + dy]:
                    p_actions.append(i)
            except IndexError:
                pass

        if not len(p_actions) or (
                current_episode < 0.7 * episode_count and numpy.random.randint(max_steps) / 4 < current_step):
            action = numpy.random.randint(agent.number_of_actions)
        else:
            action = p_actions[numpy.random.randint(len(p_actions))]

        obs, reward, done, info = env.step(action)

        cur_reward += reward

        a = np.zeros(shape=(10, 10))
        x, y = env.cur_position_discrete
        a[x, y] = 1

        ss.add(reward)

        dec_delta = transform_reward_to_weight_dec(reward)
        dec_delta, temporal_pooler_region.temporal_settings.dendrite_permanence_dec_delta = temporal_pooler_region.temporal_settings.dendrite_permanence_dec_delta, dec_delta
        inc_delta = transform_reward_to_weight_inc(reward)
        inc_delta, temporal_pooler_region.temporal_settings.dendrite_permanence_inc_delta = temporal_pooler_region.temporal_settings.dendrite_permanence_inc_delta, inc_delta

        temporal_pooler_region.step_forward(a)
        # if current_episode * 2 > episode_count:
        #     temporal_pooler_region.out_prediction()
        inc_delta, temporal_pooler_region.temporal_settings.dendrite_permanence_inc_delta = temporal_pooler_region.temporal_settings.dendrite_permanence_inc_delta, inc_delta
        dec_delta, temporal_pooler_region.temporal_settings.dendrite_permanence_dec_delta = temporal_pooler_region.temporal_settings.dendrite_permanence_dec_delta, dec_delta

        if done == 100:
            print(done)
            print("finish:", x, y)
            a = np.zeros(shape=(10, 10))
            temporal_pooler_region.step_forward(a)
            break

    print("iter: ", current_episode, "reward: ", cur_reward)
    if current_episode > episode_count - 50:
        P[7][4] = 2
        draw_image("pic2/last_path_on_grid" + str(current_episode), P)

    if current_episode == episode_count - 1:
        Foo(temporal_pooler_region, finish)
        break