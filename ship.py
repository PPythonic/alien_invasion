# coding=utf8

import pygame
import game_functions as gf


class Ship(object):

    def __init__(self, ai_settings, screen):
        self.screen = screen  # 初始化飞船并设置其初始位置
        self.ai_settings = ai_settings
        self.image = pygame.image.load('images/ship.bmp')   # 加载飞船图形并获取其外接矩形
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx  # 将每艘新飞船放在屏幕底部中央
        self.rect.bottom = self.screen_rect.bottom-20
        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.centerx = float(self.rect.centerx)  # 在飞船的属性center中存储小数值
        self.centery = float(self.rect.bottom)
        # self.fire = False

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self, ai_settings, screen, ship, bullets):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.move_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.move_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor
        # if self.fire:
        #     gf.fire_bullet(ai_settings, screen, ship, bullets)
        # 根据self.center更新rect对象
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        self.centerx = self.rect.centerx
        self.centery = self.screen_rect.bottom-20
