import pygame
from datetime import datetime
from config import *
from webcam.processor import start_webcam, stop_webcam

data_lock = Lock()
squats_count = 0
is_squatting = False
squat_state = "standing"
webcam_active = False

def squat_exercise_game(screen, user_data, current_user):
    global squats_count, is_squatting, squat_state, webcam_active
    
    with data_lock:
        squats_count = 0
        is_squatting = False
        squat_state = "standing"
        
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = user_data[current_user].get('last_exercise_date')
        
        if last_date:
            last_date = datetime.strptime(last_date, "%Y-%m-%d")
            today_date = datetime.strptime(today, "%Y-%m-%d")
            days_missed = (today_date - last_date).days - 1
            
            if days_missed > 0:
                reduction = min(MAX_PROGRESS_REDUCTION, PROGRESS_REDUCTION_PER_DAY * days_missed)
                user_data[current_user]['progress'] = max(0, user_data[current_user]['progress'] - reduction)
        
        user_data[current_user]['last_exercise_date'] = today
        if 'squats_history' not in user_data[current_user]:
            user_data[current_user]['squats_history'] = {}
        if today not in user_data[current_user]['squats_history']:
            user_data[current_user]['squats_history'][today] = 0
    
    # Countdown
    for countdown in range(5, 0, -1):
        screen.fill(WHITE)
        countdown_text = FONT_LARGE.render(str(countdown), True, RED)
        countdown_rect = countdown_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        screen.blit(countdown_text, countdown_rect)
        
        ready_instruction = FONT_REGULAR.render("Get Ready for Squats!", True, BLACK)
        instruction_rect = ready_instruction.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 200))
        screen.blit(ready_instruction, instruction_rect)
        
        pygame.display.flip()
        pygame.time.delay(1000)
    
    webcam_active = True
    start_webcam("squat")
    
    game_running = True
    start_time = pygame.time.get_ticks()
    
    while game_running and webcam_active:
        current_time = pygame.time.get_ticks()
        time_left = max(0, SQUAT_EXERCISE_DURATION - (current_time - start_time))
        
        screen.fill(WHITE)
        
        squats_text = FONT_REGULAR.render(f"Squats: {squats_count}", True, BLACK)
        screen.blit(squats_text, (50, 480))
        
        time_text = FONT_REGULAR.render(f"Time: {time_left // 1000}s", True, BLACK)
        screen.blit(time_text, (650, 480))
        
        progress = user_data[current_user]['progress']
        pygame.draw.rect(screen, BLACK, (200, 480, 300, 30), 2)
        pygame.draw.rect(screen, GREEN, (200, 480, int(3 * progress), 30))
        progress_text = FONT_SMALL.render(f"Progress: {progress}%", True, BLACK)
        screen.blit(progress_text, (320, 485))
        
        instruction = FONT_SMALL.render("Do squats to increase progress. Press ESC to exit.", True, BLACK)
        screen.blit(instruction, (250, 520))
        
        squat_status = FONT_REGULAR.render("Squatting" if is_squatting else "Stand Straight", True, RED if is_squatting else BLACK)
        screen.blit(squat_status, (350, 450))
        
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
    
    return squats_count