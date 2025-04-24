import json
from datetime import datetime
from config import *

def load_user_data():
    try:
        with open(USER_DATA_FILE, "r") as file:
            data = json.load(file)
            for user in data:
                if 'squats_history' not in data[user]:
                    data[user]['squats_history'] = {}
                if 'walking_history' not in data[user]:
                    data[user]['walking_history'] = {}
            return data
    except FileNotFoundError:
        return {}

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def register_user(user_data, name, age):
    if not name:
        return False, "Name cannot be empty."
    
    try:
        age = int(age)
        if age <= 0:
            return False, "Age must be a positive number."
    except ValueError:
        return False, "Age must be a number."
    
    if name in user_data:
        return True, f"Welcome back, {name}!"
    else:
        user_data[name] = {
            "age": age,
            "coins": 0,
            "progress": 0,
            "squats_history": {},
            "walking_history": {},
            "last_exercise_date": None,
            "inventory": []
        }
        save_user_data(user_data)
        return True, f"Welcome, {name}! You've been registered."

def update_user_progress(user_data, username, exercise_type, count):
    today = datetime.now().strftime("%Y-%m-%d")
    
    if username not in user_data:
        return False
    
    if exercise_type == "squat":
        user_data[username]['squats_history'][today] = count
        progress = min(100, (count / GOAL_SQUATS) * 100)
        user_data[username]['progress'] = progress
        coins_earned = min(count, GOAL_SQUATS) * SQUAT_COIN_MULTIPLIER
    elif exercise_type == "walking":
        user_data[username]['walking_history'][today] = count
        coins_earned = count * WALKING_COIN_MULTIPLIER
    elif exercise_type == "hand":
        coins_earned = count * HAND_COIN_VALUE
    
    user_data[username]['coins'] += coins_earned
    user_data[username]['last_exercise_date'] = today
    save_user_data(user_data)
    
    return coins_earned