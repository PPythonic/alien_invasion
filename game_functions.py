# coding=utf8

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_event(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_UP:
        ship.move_up = True
    elif event.key == pygame.K_DOWN:
        ship.move_down = True
    elif event.key == pygame.K_SPACE:
        # ship.fire = True
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False
    elif event.key == pygame.K_UP:
        ship.move_up = False
    elif event.key == pygame.K_DOWN:
        ship.move_down = False
    # elif event.key == pygame.K_SPACE:
    #     ship.fire = False


def check_event(ai_settings, screen, ship, bullets, stats, play_button, aliens, sb):
    for event in pygame.event.get():
        """响应按键和鼠标事件"""
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb)


def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, ship, aliens, bullets, sb):
    """在玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_avtive:
        ai_settings.initialize_dynamic_settings()  # 重置游戏设置
        pygame.mouse.set_visible(False)  # 设置光标不可见
        stats.reset_stats()
        sb.pre_score()
        stats.game_avtive = True
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        

def update_screen(ai_settings, screen, ship, aliens, bullets, play_button, stats, sb):
    """更新屏幕上的图像,并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 绘制一艘飞船
    ship.blitme()
    # 绘制一艘外星人飞船
    aliens.draw(screen)
    # 绘制得分板
    sb.show_score()
    # 绘制所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_avtive:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets, aliens, ai_settings, screen, ship, stats, sb):
    # 更新子弹的位置
    bullets.update()
    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # 检查是否有子弹击中了外星人
    check_aliens_bullets_collide(bullets, aliens, ai_settings, screen, ship, stats, sb)


def check_aliens_bullets_collide(bullets, aliens, ai_settings, screen, ship, stats, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_point*len(aliens)
            sb.pre_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        creat_fleet(ai_settings, screen, aliens, ship)
        stats.level += 1
        sb.pre_level()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allow:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def creat_fleet(ai_settings, screen, aliens, ship):
    """创建外星人舰队"""
    alien = Alien(ai_settings, screen)
    alien_nums_x = get_alien_num(ai_settings, alien.rect.width)
    alien_nums_y = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人舰队群
    for row_number in range(alien_nums_y):
        for alien_number in range(alien_nums_x):
            # 创建第一行外星人
            creat_alien(alien_number, ai_settings, screen, aliens, row_number)


def get_alien_num(ai_settings, alien_width):
    """获取可创建的飞船数"""
    available_space_x = ai_settings.screen_width - (alien_width*2)
    alien_nums = int(available_space_x/(alien_width*2))
    return alien_nums


def creat_alien(alien_number, ai_settings, screen, aliens, row_number):
    # 创建一个外星人并加入当前行
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    available_space_y = ai_settings.screen_height-3*alien_height-ship_height
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows


def update_aliens(ai_settings, aliens, ship, stats, bullets, screen, sb):
    check_aliens_edges(ai_settings, aliens)
    check_aliens_bottom(ai_settings, aliens, ship, stats, bullets, screen, sb)
    aliens.update()
    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print "ship hit!!! "+"you have %d life" % (stats.ship_left-1)
        ship_hit(ai_settings, aliens, ship, stats, bullets, screen, sb)
        sleep(0.5)


def check_aliens_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def check_aliens_bottom(ai_settings, aliens, ship, stats, bullets, screen, sb):  # 检查飞船是否通过屏幕底部
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            if stats.ship_left > 1:
                # print "aliens move in!! "+"you have %d life" % (stats.ship_left-1)
                ship_hit(ai_settings, aliens, ship, stats, bullets, screen, sb)
                break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, aliens, ship, stats, bullets, screen, sb):
    if stats.ship_left > 1:
        stats.ship_left -= 1
        sb.pre_score()
        aliens.empty()
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
    else:
        stats.game_avtive = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.pre_high_score()