# coding=utf8

import pygame.font


class ScoreBoard(object):
    """显示得分信息的类"""

    def __init__(self, ai_settings, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        self.pre_score()  # 准备初始化得分图像
        self.pre_high_score()
        self.pre_level()

    def pre_score(self):
        """将得分转化为一幅渲染的图像"""
        score_str = "point: " + str(self.stats.score) + " " + "life: " + str(self.stats.ship_left-1)
        self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def pre_high_score(self):
        """将最高得分转化为一幅渲染的图像"""
        high_score_str = "high score: " + str(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
        # 将高分显示到屏幕顶部中间
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def pre_level(self):
        """将当前等级转化为一张渲染的图片"""
        level_str = "level: " + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.ai_settings.bg_color)
        self.level_image_rect = self.level_image.get_rect()
        self.level_image_rect.left = self.screen_rect.left
        self.level_image_rect.top = self.score_rect.top

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_image_rect)
        

        