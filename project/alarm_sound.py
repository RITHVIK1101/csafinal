import pygame
from threading import Thread, Event

pygame.mixer.init()
alarm_sound = pygame.mixer.Sound("alarm_sound.mp3")
alarm_thread = None
stop_event = Event()

def play_sound():
    global alarm_sound
    alarm_sound.play(-1)  # -1 means loop indefinitely
    while not stop_event.is_set():
        continue
    alarm_sound.stop()

def start_alarm_sound():
    global alarm_thread, stop_event
    print("Starting alarm sound...")
    stop_event.clear()
    alarm_thread = Thread(target=play_sound)
    alarm_thread.start()

def stop_alarm_sound():
    global alarm_thread, stop_event
    print("Stopping alarm sound...")
    if alarm_thread and alarm_thread.is_alive():
        stop_event.set()
        alarm_thread.join()
        print("Alarm sound stopped")
