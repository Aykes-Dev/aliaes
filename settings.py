class Settings():
    """Класс для хранения всех настроек игры Alien Invasion."""
    def __init__(self) -> None:
        # Настройки экрана
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (22, 133, 227)

        # Настройки корабля
        self.ship_limit = 3  # Кол-во жизней

        # Параметры снаряда
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Инициализирует настройки, изменяющиеся в ходе игры."""
        self.ship_speed = 5
        self.bullet_speed = 10
        self.alien_speed = 3.3

        # fleet_direction = 1 обозначает движение вправо; а -1 - влево.
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеличивает настройки скорости."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
