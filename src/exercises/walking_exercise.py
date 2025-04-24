import pygame
from datetime import datetime
from config import *
from webcam.processor import start_webcam, stop_webcam

data_lock = Lock()
walking_bursts = 0
walking_state = "Standing"
last_walking_state = "Standing"
center_history = []
still_counter = 0
webcam_active = False

def walking_exercise_game(screen, user_data, current_user):
    global walking_bursts, walking_state, last_walking_state, center_history, still_counter, webcam_active
    
    with data_lock:
        walking_bursts = 0
        walking_state = "Standing"
        last_walking_state = "Standing"
        center_history = []
        still_counter = 0
        
        today = datetime.now().strftime("%Y-%m-%d")
        user_data[current_user]['last_exercise_date'] = today
    
    # Countdown
    for countdown in range(5, 0, -1):
        screen.fill(WHITE)
        countdown_text = FONT_LARGE.render(str(countdown), True, RED)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(countdown_text, countdown_rect)
        
        ready_instruction = FONT_REGULAR.render("Get Ready for Walking!", True, BLACK)
        instruction_rect = ready_instruction.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200))
        screen.blit(ready_instruction, instruction_rect)
        
        pygame.display.flip()
        pygame.time.delay(1000)
    
    webcam_active = True
    start_webcam("walking")
    
    game_running = True
    start_time = pygame.time.get_ticks()
    
    while game_running and webcam_active:
        current_time = pygame.time.get_ticks()
        time_left = max(0, WALKING_EXERCISE_DURATION - (current_time - start_time))
        
        screen.fill(WHITE)
        
        status_text = FONT_REGULAR.render(f"Status: {walking_state}", True, GREEN if walking_state == "Walking" else BLACK)
        screen.blit(status_text, (50, 150))
        
        bursts_text = FONT_REGULAR.render(f"Walking Bursts: {walking_bursts}", True, BLUE)
        screen.blit(bursts_text, (50, 200))
        
        time_text = FONT_REGULAR.render(f"Time Left: {time_left // 1000}s", True, BLACK)
        screen.blit(time_text, (650, 50))
        
        pygame.draw.rect(screen, BLACK, (150, 450, 500, 20), 2)
        progress_width = int((time_left / WALKING_EXERCISE_DURATION) * 500)
        pygame.draw.rect(screen, (0, 180, 255), (150, 450, 500 - progress_width, 20))
        
        instruction = FONT_SMALL.render("Walk in place to register walking bursts. Press ESC to exit.", True, BLACK)
        screen.blit(instruction, (200, 520))
        
        pygame.display.flip()
        
        if time_left <= 0:
            game_running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_running = False
    
    webcam_active = False
    stop_webcam()
    
    return walking_bursts