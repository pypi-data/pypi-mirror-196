from abc import ABC
from gym import Env, spaces
from gym.spaces import Discrete, Box
import numpy as np
import random
from gym.utils import seeding
from kinetic_modeling import *


class all_params_env(Env, ABC):
    def __init__(self, Model, params, err, err_err, kws):
        self.np_random = []
        self.params = params
        self.state = params
        # for i, k in enumerate(self.state):
        #     self.state[i] = k + random.uniform(-0.05, 0.05)
        self.low = 0.0
        self.high = 1.6
        self.max_step_perEpisode = 0.2
        self.seed()
        # 所采取的动作空间维度，如 参数减小，参数不变，参数增加，
        self.action_space = spaces.Discrete(3)
        # 参数范围数组 Box允许在整个空间内有连续值
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.float32, shape=(6,))
        self.Model = Model  # 房室模型
        self.err = err
        self.new_err = 0
        self.err_err = err_err
        self.kws = kws
        self.next_state = params

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    # 主程序
    def step(self, action):
        # 应用动作
        # 0 - 1 = -1 params change
        # 1 - 1 = 0
        # 2 - 1 = 1
        self.state[0] += (action - 1) * 0.05
        self.state[1] += (action - 1) * 0.03
        self.state[2] += (action - 1) * 0.01
        self.state[3] += (action - 1) * 0.01
        self.state[4] += (action - 1) * 0.03
        self.state[5] += (action - 1) * 0.01
        state_temp = [self.state[0],
                      self.state[1],
                      self.state[2],
                      self.state[3],
                      self.state[4],
                      self.state[5]]
        self.next_state = state_temp
        self.err = CompartmentModelling.compartment_model_residual(
            self.Model,
            params=state_temp,
            **self.kws,
        )
        # 计算奖励
        if 5 < abs(self.err) < 10:
            reward = 3
        if abs(self.err) <= 5:
            reward = 5
        else:
            reward = -1

        # 检查终止点(每个回合)
        if abs(self.err) >= 10:  # 当误差大于10 立即终止
            done = True
        elif abs(self.err) <= 3:  # 误差小于3 立即终止
            done = True
        else:
            done = False

        # 增加干扰
        # self.state += random.uniform(-0.1, 0.1)
        # 设置信息占位符
        info = {}

        # 返回步骤信息
        return self.state, reward, done, info

    def render(self, mode="human"):
        # 渲染可视化界面
        pass

    # 重置环境
    def reset(self):
        # 重置参数为初始值
        self.state[0] = self.params[0] + random.uniform(-0.1, 0.1)  # k1
        self.state[1] = self.params[1] + random.uniform(-0.1, 0.1)  # k2
        self.state[2] = self.params[2] + random.uniform(-0.02, 0.02)  # k3
        self.state[3] = self.params[3] + random.uniform(-0.02, 0.02)  # k4
        self.state[4] = self.params[4] + random.uniform(-0.1, 0.1)  # fa
        self.state[5] = self.params[5] + random.uniform(-0.02, 0.02)  # vb
        # 不带随机大小值
        # self.state[0] = self.params[0]  # k1
        # self.state[1] = self.params[1]  # k2
        # self.state[2] = self.params[2]  # k3
        # self.state[3] = self.params[3]  # k4
        # self.state[4] = self.params[4]  # fa
        # self.state[5] = self.params[5]  # vb
        # # 重置误差
        self.err = CompartmentModelling.compartment_model_residual(
            self.Model,
            params=[self.state[0],
                    self.state[1],
                    self.state[2],
                    self.state[3],
                    self.state[4],
                    self.state[5]],
            **self.kws,
        )
        return self.state

# if __name__ == '__main__':
