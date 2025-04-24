import pygame
import matplotlib.pyplot as plt
from config import *
from user_manager import load_user_data, save_user_data

def show_message(screen, message, duration=2000):
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        screen.fill(WHITE)
        text_surface = FONT_REGULAR.render(message, True, BLACK)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
    return True

def get_text_input(screen, prompt):
    input_text = ""
    input_active = True
    
    while input_active:
        screen.fill(WHITE)
        prompt_surface = FONT_REGULAR.render(prompt, True, BLACK)
        screen.blit(prompt_surface, (50, 150))
        
        pygame.draw.rect(screen, BLACK, (50, 200, 700, 50), 2)
        text_surface = FONT_REGULAR.render(input_text, True, BLACK)
        screen.blit(text_surface, (60, 210))
        
        instruction = FONT_SMALL.render("Press ENTER to confirm", True, BLACK)
        screen.blit(instruction, (50, 270))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    
    return input_text

def select_existing_user(screen, user_data):
    if not user_data:
        show_message(screen, "No existing users found. Please register first.")
        return None
    
    selected_index = 0
    users_list = list(user_data.keys())
    selecting = True
    
    while selecting:
        screen.fill(WHITE)
        title = FONT_REGULAR.render("Select User", True, BLACK)
        screen.blit(title, (320, 50))
        
        for i, user in enumerate(users_list):
            color = BLUE if i == selected_index else BLACK
            user_text = FONT_REGULAR.render(f"{user} (Age: {user_data[user]['age']})", True, color)
            screen.blit(user_text, (150, 150 + i * 50))
        
        back_text = FONT_REGULAR.render("Back", True, BLUE if selected_index == len(users_list) else BLACK)
        screen.blit(back_text, (150, 150 + len(users_list) * 50))
        
        instruction = FONT_SMALL.render("UP/DOWN to navigate, ENTER to select, ESC to go back", True, BLACK)
        screen.blit(instruction, (250, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(users_list), selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    if selected_index == len(users_list):
                        return None
                    else:
                        return users_list[selected_index]
                elif event.key == pygame.K_ESCAPE:
                    return None
    
    return None

def select_exercise(screen, current_user):
    selected_index = 0
    options = ["Hand Exercise", "Squatting", "Walking", "Back"]
    selecting = True
    
    while selecting:
        screen.fill(WHITE)
        title = FONT_REGULAR.render(f"Welcome, {current_user}! Select Exercise Type", True, BLACK)
        screen.blit(title, (200, 100))
        
        for i, option in enumerate(options):
            color = BLUE if i == selected_index else BLACK
            option_text = FONT_REGULAR.render(option, True, color)
            screen.blit(option_text, (320, 200 + i * 50))
        
        instruction = FONT_SMALL.render("UP/DOWN to navigate, ENTER to select", True, BLACK)
        screen.blit(instruction, (250, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(options) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    if options[selected_index] == "Back":
                        return None
                    else:
                        return options[selected_index].lower().split()[0]
    
    return None

def main_menu(screen, current_user):
    selected_index = 0
    options = ["New User", "Existing User", "Marketplace", "View Graphs", "View Avatar", "Delete User", "Quit"]
    menu_active = True
    
    while menu_active:
        screen.fill(WHITE)
        title = FONT_REGULAR.render("Exercise Tracker Game", True, BLUE)
        screen.blit(title, (280, 50))
        
        if current_user:
            user_text = FONT_REGULAR.render(f"Current User: {current_user}", True, GREEN)
            screen.blit(user_text, (280, 100))
        
        for i, option in enumerate(options):
            color = BLUE if i == selected_index else BLACK
            option_text = FONT_REGULAR.render(option, True, color)
            screen.blit(option_text, (350, 200 + i * 50))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", current_user
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_index = max(0, selected_index - 1)
                elif event.key == pygame.K_DOWN:
                    selected_index = min(len(options) - 1, selected_index + 1)
                elif event.key == pygame.K_RETURN:
                    choice = options[selected_index]
                    if choice == "Quit":
                        return "quit", current_user
                    else:
                        return choice.lower().replace(" ", "_"), current_user
    
    return "quit", current_user

def generate_hand_exercise_graph(user_data):
    users = list(user_data.keys())
    coins = [user_data[user]['coins'] for user in users]
    plt.bar(users, coins, color='blue')
    plt.title("Hand Exercise Performance (Coins Collected)")
    plt.xlabel("Users")
    plt.ylabel("Coins Collected")
    plt.show()

def generate_squatting_graph(user_data):
    users = list(user_data.keys())
    squats = [sum(user_data[user]['squats_history'].values()) for user in users]
    plt.bar(users, squats, color='green')
    plt.title("Squatting Performance (Total Squats)")
    plt.xlabel("Users")
    plt.ylabel("Total Squats")
    plt.show()

def generate_walking_graph(user_data):
    users = list(user_data.keys())
    walking_data = [sum(user_data[user]['walking_history'].values()) for user in users]
    plt.bar(users, walking_data, color='orange')
    plt.title("Walking Performance (Total Walking Bursts)")
    plt.xlabel("Users")
    plt.ylabel("Total Walking Bursts")
    plt.show()