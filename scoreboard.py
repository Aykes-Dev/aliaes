import pygame


class Scoreboard():
    """Класс для вывода игровой информации."""
    def __init__(self, ai_game):
        """Инициализирует атрибуты подсчета очков."""
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для вывода счета.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # Подготовка исходного изображения.
        self.prep_score()
