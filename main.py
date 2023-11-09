import time

import vision
from vimbot import Vimbot


def main():
    print("Initializing the Vimbot driver...")
    driver = Vimbot()

    print("Navigating to Google...")
    driver.navigate("https://www.google.com")

    # Check if the user wants to use voice mode
    voice_mode = input("Would you like to enable voice mode? (yes/no): ")
    if voice_mode.lower() == 'yes':
        # Initialize the whisper mic
        mic = WhisperMic()
        print("Voice mode enabled. Please speak your objective.")
        # Use whisper_mic to get the objective via voice
        objective = mic.listen()
    else:
        objective = input("Please enter your objective: ")
    
    # The rest of your main function...
    while True:
        time.sleep(1)
        print("Capturing the screen...")
        screenshot = driver.capture()

        print("Getting actions for the given objective...")
        action = vision.get_actions(screenshot, objective)
        if driver.perform_action(action):  # returns True if done
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
