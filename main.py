import time
import threading
import queue
from whisper_mic.whisper_mic import WhisperMic
import vision
from vimbot import Vimbot

# Queue for thread-safe communication
objectives_queue = queue.Queue()

def listen_for_voice(mic, objectives_queue):
    while True:
        try:
            print("Listening for voice input...")
            objective = mic.listen()
            if objective:
                objectives_queue.put(objective)
                print(f"Voice command received: {objective}")
        except Exception as e:
            print(f"Error during listening: {e}")

def main():
    print("Initializing the Vimbot driver...")
    driver = Vimbot()

    print("Navigating to Google...")
    driver.navigate("https://www.google.com")

    # Ask user if they want to enable voice mode
    voice_mode = input("Would you like to enable voice mode? (yes/no): ")
    if voice_mode.lower() == 'yes':
        mic = WhisperMic()
        print("Voice mode enabled. Please speak your objective.")
        listening_thread = threading.Thread(target=listen_for_voice, args=(mic, objectives_queue))
        listening_thread.daemon = True
        listening_thread.start()
    else:
        objective = input("Please enter your objective: ")
        objectives_queue.put(objective)

    while True:
        if not objectives_queue.empty():
            objective = objectives_queue.get()
            print(f"Working on the objective: {objective}")

            time.sleep(1)
            print("Capturing the screen...")
            screenshot = driver.capture()

            print("Getting actions for the given objective...")
            action = vision.get_actions(screenshot, objective)
            print(f"Action determined: {action}")
            if driver.perform_action(action):
                print("Objective completed. Awaiting next command.")
                if voice_mode.lower() != 'yes':
                    # If not in voice mode, break after each action
                    break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
    except Exception as e:
        print(f"Unhandled exception: {e}")
