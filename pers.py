import pygame


class Pers():
    """Простой перс"""
    def __init__(self, ai_game) -> None:
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('alien_invasion/images/pers.png')
        self.rect = self.image.get_rect()

        self.rect.center = self.screen_rect.center

    def blitme(self):
        """Рисует в текущей позиции."""
        self.screen.blit(self.image, self.rect)
