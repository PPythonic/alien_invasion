# coding=utf8

# import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


def run_game():
    # 初始化程序并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')
    stats = GameStats(ai_settings)  # 创建一个用于统计游戏信息的实例
    ship = Ship(ai_settings, screen)
    bullets = Group()  # 创建一个用于子弹的编组
    aliens = Group()   # 创建一个外星人编组
    gf.creat_fleet(ai_settings, screen, aliens, ship)
    play_button = Button(ai_settings, screen, "PLAY")
    sb = ScoreBoard(ai_settings, screen, stats)

    # 开始程序的主循环
    while True:
        # 监视键盘和鼠标事件
        gf.check_event(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb)
        if stats.game_avtive:
            ship.update(ai_settings, screen, ship, bullets)
            gf.update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb)
            gf.update_aliens(ai_settings, aliens, ship, stats, bullets, screen, sb)
            # 更新屏幕信息
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb)
        

if __name__ == "__main__":
    run_game()
