#!/usr/bin/env python
"""Основной класс игры.

создние Кучи всего всего.

"""

import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet
from button import Button
from gamestats import GameStats
from settings import Settings
from ship import Ship


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры."""
    def __init__(self) -> None:
        """Инициализирует игру и создает игровые ресурсы."""
        pygame.init()
        self.settings = Settings()
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        """self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))"""

        # Полноэкраный режим
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Создание экземпляра для хранения игровой статистики.
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self._create_fleet()

        # Создание кнопки Play.
        self.play_button = Button(self, "Play")

        # Создание кнопок сложности.
        self.a = {}
        for i in range(1, 6):
            self.a[i] = Button(self, str(i), i * 3 * 100)

        self.FPS = 60        # число кадров в секунду
        self.clock = pygame.time.Clock()

    def run_game(self) -> None:
        """Запуск основного цикла игры."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(self.FPS)

    def _check_events(self):
        """Обрабатывает нажатия клавиш и события мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            # Слушитель для кнопки Play
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.start_game()

        for key, btn_clk in self.a.items():
            if (btn_clk.rect.collidepoint(mouse_pos)
                    and not self.stats.game_active):
                # Сброс игровых настроек.
                self.settings.initialize_dynamic_settings()
                srt = 1.1 ** key
                self.settings.ship_speed *= srt
                self.settings.bullet_speed *= srt
                self.settings.alien_speed *= srt

        print(self.settings.ship_speed)

    def start_game(self):
        # Сброс игровой статистики.
        self.stats.reset_stats()

        # Указатель мыши скрывается.
        pygame.mouse.set_visible(False)

        self.stats.game_active = True

        # Очистка списков пришельцев и снарядов.
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре.
        self._create_fleet()
        self.ship.center_ship()

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        if event.key == pygame.K_p:
            if not self.stats.game_active:
                self.start_game()

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        if event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает старые снаряды."""
        # Обновление позиций снарядов.
        self.bullets.update()
        # Удаление снарядов, вышедших за край экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и пришельцев, участвующих в коллизиях.
        _ = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self.settings.increase_speed()
            self._create_fleet()

    def _create_fleet(self):
        """Создание прищельца"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # Определяем колв-во кораблей в ряду.
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_space_x = available_space_x // (2 * alien_width)
        # Определяем кол-во рядов на экране.
        available_space_y = (
            self.settings.screen_height -
            (3 * alien_height) - self.ship.rect.height)
        number_space_y = available_space_y // (2 * alien_height)
        # Создание флота.
        for row_number in range(number_space_y):
            for alian_number in range(number_space_x):
                self._create_alien(alian_number, row_number)

    def _create_alien(self, alian_number, row_number):
        """Создание пришельца и размещение его в ряду."""
        alien = Alien(self)
        alien_width, alien_heigh = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alian_number
        alien.rect.x = alien.x
        alien.rect.y = alien_heigh + 2 * alien_heigh * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if screen_rect.bottom <= alien.rect.bottom:
                # Происходит то же, что при столкновении с кораблем.
                self._ship_hit()
                break

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев во флоте."""
        self._check_fleet_edges()
        self.aliens.update()
        # Проверка коллизий "пришелец — корабль".
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        # Проверить, добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Обрабатывает столкновение корабля с пришельцем."""
        # Уменьшение ships_left.
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()
            # Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()
            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            # Сброс игровых настроек.
            self.settings.initialize_dynamic_settings()

    def _update_screen(self):
        """Обновляет изображения на экране и отображает новый экран."""
        # При каждом проходе цикла перерисовывается экран.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        # Отрисовка каждой пиу-пиу.
        for bullet in self.bullets:
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()
            for value in self.a.values():
                value.draw_button()
        # Отображение последнего прорисованного экрана.
        pygame.display.flip()


if __name__ == '__main__':
    # Создание экземпляра и запуск игры.
    ai = AlienInvasion()
    ai.run_game()
