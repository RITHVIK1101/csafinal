from playsound import playsound
from threading import Thread, Event

alarm_thread = None
stop_event = Event()

def play_sound():
    while not stop_event.is_set():
        playsound('alarm_sound.mp3')

def start_alarm_sound():
    global alarm_thread, stop_event
    stop_event.clear()
    alarm_thread = Thread(target=play_sound)
    alarm_thread.start()

def stop_alarm_sound():
    global alarm_thread, stop_event
    if alarm_thread and alarm_thread.is_alive():
        stop_event.set()
        alarm_thread.join()
        print("Stopping alarm sound")
