# coding=utf8


class Settings(object):
    """存储alien invasion的所有设置"""

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # self.ship_speed_factor = 1.5
        # 子弹设置
        # self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allow = 20
        # 外星人设置
        # self.alien_speed_factor = 0.5
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1表示想右移,-1表示向左移动
        # 飞船设置
        self.ship_limit = 3
        self.speedup_scale = 1.1  # 以什么样的速度加快游戏节奏
        self.initialize_dynamic_settings()
        self.alien_point = 10  # 击落一架外星人的得分
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        self.alien_speed_factor = 0.5
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1

    def increase_speed(self):
        """提高速度设置"""
        self.alien_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.alien_point = int(self.alien_point*self.score_scale)

