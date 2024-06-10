import tkinter as tk
from alarm import set_alarm
from threading import Thread
from tkinter import messagebox

def start_alarm():
    alarm_time = alarm_entry.get()
    pushup_goal = int(goal_var.get())
    set_alarm(alarm_time, pushup_goal)
    messagebox.showinfo("Alarm Set", "Alarm set successfully!")

root = tk.Tk()
root.title("Pushup Counter Alarm")

tk.Label(root, text="Set Alarm (HH:MM)").pack()
alarm_entry = tk.Entry(root)
alarm_entry.pack()

tk.Label(root, text="Set Pushup Goal").pack()
goal_var = tk.StringVar(value="10")
tk.Radiobutton(root, text="10", variable=goal_var, value="10").pack()
tk.Radiobutton(root, text="15", variable=goal_var, value="15").pack()
tk.Radiobutton(root, text="20", variable=goal_var, value="20").pack()

tk.Button(root, text="Set Alarm", command=start_alarm).pack()

root.mainloop()
