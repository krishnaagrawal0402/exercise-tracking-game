import pygame
import sys
import os
from config import *
from user_manager import load_user_data, save_user_data
from exercises.hand_exercise import hand_exercise_game
from exercises.squat_exercise import squat_exercise_game
from exercises.walking_exercise import walking_exercise_game
from ui.menus import main_menu, select_exercise, select_existing_user, register_user, show_message, get_text_input
from ui.avatar import view_avatar
from ui.marketplace import marketplace

def setup_game():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Exercise Tracker Game")
    
    # Initialize music
    try:
        pygame.mixer.init()
        if os.path.exists(MUSIC_FILE):
            pygame.mixer.music.load(MUSIC_FILE)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Error initializing music: {e}")
    
    return screen

def main():
    screen = setup_game()
    user_data = load_user_data()
    current_user = None
    running = True
    
    while running:
        choice, current_user = main_menu(screen, current_user)
        
        if choice == "quit":
            running = False
        elif choice == "new_user":
            name = get_text_input(screen, "Enter Name")
            if name is None:
                continue
            age = get_text_input(screen, "Enter Age")
            if age is None:
                continue
            success, message = register_user(user_data, name, age)
            show_message(screen, message)
            if success:
                current_user = name
        elif choice == "existing_user":
            current_user = select_existing_user(screen, user_data)
        elif choice == "marketplace":
            marketplace(screen, user_data, current_user)
        elif choice == "view_graphs":
            show_message(screen, "Graph viewing feature coming soon!")
        elif choice == "view_avatar":
            view_avatar(screen, user_data, current_user)
        elif choice == "delete_user":
            show_message(screen, "User deletion feature coming soon!")
        else:
            if current_user is None:
                show_message(screen, "Please login first!")
                continue
            
            exercise_type = select_exercise(screen, current_user)
            if exercise_type is None:
                continue
            
            if exercise_type == "hand":
                coins = hand_exercise_game(screen, user_data, current_user)
                user_data[current_user]['coins'] += coins
                save_user_data(user_data)
                show_message(screen, f"Exercise Complete! You collected {coins} coins.", 3000)
            elif exercise_type == "squatting":
                squats = squat_exercise_game(screen, user_data, current_user)
                coins_earned = min(squats, GOAL_SQUATS) * SQUAT_COIN_MULTIPLIER
                user_data[current_user]['coins'] += coins_earned
                save_user_data(user_data)
                show_message(screen, f"Exercise Complete! You did {squats} squats and earned {coins_earned} coins.", 3000)
            elif exercise_type == "walking":
                bursts = walking_exercise_game(screen, user_data, current_user)
                coins_earned = bursts * WALKING_COIN_MULTIPLIER
                user_data[current_user]['coins'] += coins_earned
                save_user_data(user_data)
                show_message(screen, f"Exercise Complete! You achieved {bursts} walking bursts and earned {coins_earned} coins.", 3000)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()