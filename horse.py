import pygame

class Horse:
    def __init__(self, name, y_pos, start_x, bat_image):
        self.name = name
        self.x_pos = start_x
        self.y_pos = y_pos
        self.bat_image = bat_image

    def draw(self, screen, font):
        # Zeichne die Fledermaus und den Teamnamen
        screen.blit(self.bat_image, (self.x_pos, self.y_pos))
        horse_name_text = font.render(self.name, True, (0, 0, 0))
        text_rect = horse_name_text.get_rect(center=(self.x_pos + 25, self.y_pos + 45))
        screen.blit(horse_name_text, text_rect)

    def move(self, step_distance):
        self.x_pos += step_distance
