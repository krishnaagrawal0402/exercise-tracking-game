import pygame
from config import *

def draw_button(screen, text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))
    
    text_surf = FONT_REGULAR.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    screen.blit(text_surf, text_rect)
    return None

def draw_text(screen, text, size, x, y, color=BLACK):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_music_button(screen, music_playing):
    icon_color = GREEN if music_playing else RED
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 50, 10, 40, 40), 2)
    
    if music_playing:
        pygame.draw.polygon(screen, icon_color, [
            (SCREEN_WIDTH - 40, 20), 
            (SCREEN_WIDTH - 40, 40), 
            (SCREEN_WIDTH - 30, 40), 
            (SCREEN_WIDTH - 20, 50), 
            (SCREEN_WIDTH - 20, 10), 
            (SCREEN_WIDTH - 30, 20)
        ])
    else:
        pygame.draw.line(screen, RED, (SCREEN_WIDTH - 45, 15), (SCREEN_WIDTH - 15, 45), 2)
    
    music_text = FONT_SMALL.render("Music", True, BLACK)
    screen.blit(music_text, (SCREEN_WIDTH - 45, 55))