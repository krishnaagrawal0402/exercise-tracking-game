import cv2
import mediapipe as mp
import math
import threading
from config import *
from threading import Lock

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = None
webcam_active = False
exercise_type = None

# Shared variables
coin_x, coin_y = 0.5, 0.5
coins_collected = 0
squats_count = 0
is_squatting = False
squat_state = "standing"
walking_bursts = 0
walking_state = "Standing"
last_walking_state = "Standing"
center_history = []
still_counter = 0

data_lock = Lock()

def calculate_angle(x1, y1, x2, y2, x3, y3):
    angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
    return abs(angle) if abs(angle) <= 180 else 360 - abs(angle)

def calculate_arm_angle(shoulder_x, shoulder_y, wrist_x, wrist_y):
    return math.degrees(math.atan2(wrist_y - shoulder_y, wrist_x - shoulder_x))

def start_webcam(ex_type):
    global cap, webcam_active, exercise_type
    exercise_type = ex_type
    cap = cv2.VideoCapture(0)
    webcam_active = True
    threading.Thread(target=process_webcam, daemon=True).start()

def stop_webcam():
    global cap, webcam_active
    webcam_active = False
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()

def process_webcam():
    global coin_x, coin_y, coins_collected, squats_count, is_squatting, squat_state
    global walking_bursts, walking_state, last_walking_state, center_history, still_counter
    
    while webcam_active and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            landmarks = results.pose_landmarks.landmark
            
            with data_lock:
                if exercise_type == "hand":
                    cv2.circle(frame, (int(coin_x * frame_width), int(coin_y * frame_height)), 
                              20, GOLD, -1)
                    
                    left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
                    right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
                    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
                    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
                    
                    left_wrist_pixel_x = int(left_wrist.x * frame_width)
                    left_wrist_pixel_y = int(left_wrist.y * frame_height)
                    right_wrist_pixel_x = int(right_wrist.x * frame_width)
                    right_wrist_pixel_y = int(right_wrist.y * frame_height)
                    coin_pixel_x = int(coin_x * frame_width)
                    coin_pixel_y = int(coin_y * frame_height)
                    
                    current_edge = get_current_edge(coin_x, coin_y)
                    collected = False
                    
                    left_arm_angle = calculate_arm_angle(
                        left_shoulder.x * frame_width, 
                        left_shoulder.y * frame_height, 
                        left_wrist_pixel_x, 
                        left_wrist_pixel_y
                    )
                    
                    right_arm_angle = calculate_arm_angle(
                        right_shoulder.x * frame_width, 
                        right_shoulder.y * frame_height, 
                        right_wrist_pixel_x, 
                        right_wrist_pixel_y
                    )
                    
                    left_hand_distance = math.hypot(
                        left_wrist_pixel_x - coin_pixel_x, 
                        left_wrist_pixel_y - coin_pixel_y
                    )
                    
                    right_hand_distance = math.hypot(
                        right_wrist_pixel_x - coin_pixel_x, 
                        right_wrist_pixel_y - coin_pixel_y
                    )
                    
                    if current_edge == "center":
                        left_stretched_up = (
                            left_hand_distance < HAND_PROXIMITY_THRESHOLD and
                            abs(left_arm_angle) > 70 and abs(left_arm_angle) < 110
                        )
                        right_stretched_up = (
                            right_hand_distance < HAND_PROXIMITY_THRESHOLD and
                            abs(right_arm_angle) > 70 and abs(right_arm_angle) < 110
                        )
                        collected = left_stretched_up or right_stretched_up
                    
                    elif current_edge == "left":
                        right_stretched_left = (
                            right_hand_distance < HAND_PROXIMITY_THRESHOLD and
                            right_arm_angle > 160 or right_arm_angle < -160
                        )
                        collected = right_stretched_left
                    
                    elif current_edge == "right":
                        left_stretched_right = (
                            left_hand_distance < HAND_PROXIMITY_THRESHOLD and
                            abs(left_arm_angle) < 20 or abs(left_arm_angle) > 340
                        )
                        collected = left_stretched_right
                    
                    if collected:
                        coins_collected += 1
                        cv2.circle(frame, (coin_pixel_x, coin_pixel_y), 30, (0, 255, 0), -1)
                        coin_x, coin_y = generate_edge_coin_position()
                
                elif exercise_type == "squat":
                    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
                    right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
                    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
                    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
                    
                    left_knee_angle = calculate_angle(
                        left_hip.x, left_hip.y,
                        left_knee.x, left_knee.y,
                        left_ankle.x, left_ankle.y
                    )
                    
                    right_knee_angle = calculate_angle(
                        right_hip.x, right_hip.y,
                        right_knee.x, right_knee.y,
                        right_ankle.x, right_ankle.y
                    )
                    
                    is_squatting = left_knee_angle < SQUAT_ANGLE_THRESHOLD and right_knee_angle < SQUAT_ANGLE_THRESHOLD
                    
                    if squat_state == "standing" and is_squatting:
                        squat_state = "squatting"
                    elif squat_state == "squatting" and not is_squatting:
                        squat_state = "standing"
                        squats_count += 1
                
                elif exercise_type == "walking":
                    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
                    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
                    
                    if left_hip.visibility > 0.5 and right_hip.visibility > 0.5:
                        center_x = int(((left_hip.x + right_hip.x) / 2) * frame_width)
                        center_history.append(center_x)
                        
                        if len(center_history) > SMOOTH_FRAMES:
                            center_history.pop(0)
                        
                        if len(center_history) > 1:
                            movement = max(center_history) - min(center_history)
                            
                            if movement > CENTER_MOVE_THRESHOLD:
                                walking_state = "Walking"
                                still_counter = 0
                                if last_walking_state == "Standing":
                                    walking_bursts += 1
                            else:
                                still_counter += 1
                                if still_counter > STILL_FRAMES_THRESHOLD:
                                    walking_state = "Standing"
                            
                            last_walking_state = walking_state
        
        cv2.imshow("Exercise Tracker", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    if cap is not None:
        cap.release()
    cv2.destroyAllWindows()