import pygame
import random
import cv2
import mediapipe as mp
import math
from threading import Lock
from config import *
from webcam.processor import start_webcam, stop_webcam

data_lock = Lock()
coin_x, coin_y = 0.5, 0.5
coins_collected = 0
webcam_active = False

def generate_edge_coin_position():
    edge = random.choice(["left", "center", "right"])
    return COIN_EDGE_POSITIONS[edge]

def get_current_edge(x, y):
    if abs(x - 0.5) < 0.1 and y <= 0.1:
        return "center"
    elif x <= 0.1:
        return "left"
    elif x >= 0.9:
        return "right"
    return "center"

def hand_exercise_game(screen, user_data, current_user):
    global coin_x, coin_y, coins_collected, webcam_active
    
    coin_x, coin_y = generate_edge_coin_position()
    coins_collected = 0
    current_edge = get_current_edge(coin_x, coin_y)
    
    webcam_active = True
    start_webcam("hand")
    
    game_running = True
    start_time = pygame.time.get_ticks()
    
    while game_running and webcam_active:
        current_time = pygame.time.get_ticks()
        time_left = max(0, HAND_EXERCISE_DURATION - (current_time - start_time))
        
        screen.fill(WHITE)
        
        # UI elements
        time_text = FONT_REGULAR.render(f"Time: {time_left // 1000}s", True, BLACK)
        screen.blit(time_text, (650, 50))
        
        coins_text = FONT_REGULAR.render(f"Coins: {coins_collected}/15", True, BLACK)
        screen.blit(coins_text, (50, 50))
        
        instruction = FONT_SMALL.render(f"Stretch {current_edge.upper()} to collect the coin", True, BLACK)
        screen.blit(instruction, (250, 520))
        
        pygame.display.flip()
        
        if time_left <= 0 or coins_collected >= 15:
            game_running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
    
    webcam_active = False
    stop_webcam()
    
    return coins_collected