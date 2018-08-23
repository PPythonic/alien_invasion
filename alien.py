# coding=utf8

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """外星飞船类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其起始位置"""
        super(Alien, self).__init__()
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()
        self.screen = screen
        self.ai_settings = ai_settings
        self.screen_rect = screen.get_rect()
        self.rect.y = self.rect.height
        self.rect.x = self.rect.width
        self.x = float(self.rect.x)  # 储存外星人的精确位置

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += (self.ai_settings.alien_speed_factor*self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人舰队碰到屏幕边缘,返回true"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        if self.rect.left <= screen_rect.left:
            return True