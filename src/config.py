import pygame
import os

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GOLD = (255, 215, 0)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (0, 180, 255)

# Fonts
FONT_REGULAR = pygame.font.Font(None, 36)
FONT_SMALL = pygame.font.Font(None, 24)
FONT_LARGE = pygame.font.Font(None, 200)

# Game settings
GOAL_SQUATS = 20
USER_DATA_FILE = "user_data.json"
MUSIC_FILE = os.path.join("assets", "background_music.mp3")

# Webcam settings
WEBCAM_WIDTH, WEBCAM_HEIGHT = 640, 480
CENTER_MOVE_THRESHOLD = 20
SMOOTH_FRAMES = 5
STILL_FRAMES_THRESHOLD = 10

# Exercise thresholds
SQUAT_ANGLE_THRESHOLD = 120
HAND_PROXIMITY_THRESHOLD = 100
HAND_ANGLE_THRESHOLD = 30

# Avatar assets
AVATAR_BASE = {
    "head": pygame.Rect(100, 100, 50, 50),
    "body": pygame.Rect(120, 150, 10, 50),
    "arms": pygame.Rect(100, 150, 50, 10),
    "legs": pygame.Rect(120, 200, 10, 50),
}

AVATAR_ITEMS = {
    "hat": pygame.Rect(90, 80, 70, 20),
    "glasses": pygame.Rect(110, 120, 30, 10),
    "shirt": pygame.Rect(100, 140, 50, 30),
    "shoes": pygame.Rect(110, 250, 30, 10),
}

# Marketplace items
MARKET_ITEMS = [
    {"name": "Hat", "price": 50, "description": "A stylish hat for your avatar"},
    {"name": "Glasses", "price": 30, "description": "Cool glasses for your avatar"},
    {"name": "Shirt", "price": 70, "description": "A trendy shirt for your avatar"},
    {"name": "Shoes", "price": 40, "description": "Comfortable shoes for your avatar"},
]

# Game durations (ms)
HAND_EXERCISE_DURATION = 120000
SQUAT_EXERCISE_DURATION = 120000
WALKING_EXERCISE_DURATION = 60000

# Coin settings
COIN_RADIUS = 15
COIN_EDGE_POSITIONS = {
    "left": (0.05, 0.5),
    "center": (0.5, 0.05),
    "right": (0.95, 0.5)
}

# Rewards
SQUAT_COIN_MULTIPLIER = 5
WALKING_COIN_MULTIPLIER = 10
HAND_COIN_VALUE = 1

# Progress
PROGRESS_REDUCTION_PER_DAY = 10
MAX_PROGRESS_REDUCTION = 100