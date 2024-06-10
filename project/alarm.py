import time
from pushup_counter import start_pushup_counter
from alarm_sound import start_alarm_sound, stop_alarm_sound
import tkinter as tk
from tkinter import messagebox

def set_alarm(alarm_time, pushup_goal):
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            print("Alarm ringing!")
            start_alarm_sound()
            show_pushup_message(pushup_goal)
            start_pushup_counter(pushup_goal)
            break
        time.sleep(1)

def show_pushup_message(pushup_goal):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    messagebox.showinfo("Pushup Time", f"Do {pushup_goal} pushups to stop the alarm!")
    root.destroy()
