# coding=utf8


class GameStats(object):
    """跟踪游戏的统计信息"""
    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_avtive = False  # 使游戏一开始处于非活动状态
        self.high_score = 0  # 游戏的最高分

    def reset_stats(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1  # 当前等级
        