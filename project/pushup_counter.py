import cv2
import mediapipe as mp
import numpy as np
from alarm_sound import stop_alarm_sound
import tkinter as tk
from tkinter import messagebox

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle 

def start_pushup_counter(goal):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video device.")
        return

    counter = 0 
    position = None

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Ignoring empty camera frame.")
                continue
            
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = pose.process(image)
        
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            try:
                if results.pose_landmarks:
                    landmarks = results.pose_landmarks.landmark
                    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                    
                    angle = (calculate_angle(left_shoulder, left_elbow, left_wrist) + calculate_angle(right_shoulder, right_elbow, right_wrist)) / 2
                    
                    if angle > 160:
                        position = "UP"
                    if angle < 70 and position == 'UP':
                        position = "DOWN"
                        counter += 1
                        print(counter)
                        if counter >= goal:
                            stop_alarm_sound()
                            show_goal_reached_message()
                            break
                else:
                    print("No landmarks detected.")
                           
            except Exception as e:
                print(f"Error: {e}")
                pass

            cv2.rectangle(image, (0, 0), (250, 73), (245, 110, 16), -1)
            
            cv2.putText(image, 'REPS', (15, 12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, str(counter), 
                        (10, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            
            cv2.putText(image, 'STAGE', (65, 12), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, position, 
                        (60, 60), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
            
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(245, 114, 67), thickness=2, circle_radius=2), 
                                      mp_drawing.DrawingSpec(color=(245, 69, 222), thickness=2, circle_radius=2))               
            
            cv2.imshow('Mediapipe Feed', image)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    print("Pushup goal reached. Alarm stopped.")

def show_goal_reached_message():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Goal Reached", "Pushup goal reached successfully!")
    root.destroy()
