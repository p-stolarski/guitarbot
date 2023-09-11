import pygetwindow as gw
import pyscreeze
import cv2
import numpy as np
import time
import pyautogui

# Specify the title of the game window
window_title = "Clone Hero"

# Define the note images and corresponding keys
note_images = {
    r"C:\Users\the rabbi\Desktop\guitarbot\green_note.png": ("a", "1"),
    r"C:\Users\the rabbi\Desktop\guitarbot\red_note.png": ("s", "1"),
    r"C:\Users\the rabbi\Desktop\guitarbot\yellow_note.png": ("j", "1"),
    r"C:\Users\the rabbi\Desktop\guitarbot\blue_note.png": ("k", "1"),
    r"C:\Users\the rabbi\Desktop\guitarbot\orange_note.png": ("l", "1"),
}

# Threshold for matching
threshold = 0.8

# Find the game window by title
game_window = gw.getWindowsWithTitle(window_title)[0]

while True:
    try:
        # Capture a screenshot of the game window
        screenshot = pyscreeze.screenshot(region=(
            game_window.left, game_window.top,
            game_window.width, game_window.height
        ))

        # Check if the screenshot is a valid image
        if isinstance(screenshot, np.ndarray):
            # Iterate through each note image and corresponding keys
            for note_image_path, (key1, key2) in note_images.items():
                # Load the note image with the cv2.IMREAD_COLOR flag
                note_image = cv2.imread(note_image_path, cv2.IMREAD_COLOR)

                # Check if image loading was successful
                if note_image is not None and isinstance(note_image, np.ndarray):
                    # Check if the image is a color image (not grayscale)
                    if len(note_image.shape) == 3:
                        # Convert the screenshot to grayscale for template matching
                        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                        # Perform template matching
                        result = cv2.matchTemplate(screenshot_gray, note_image, cv2.TM_CCOEFF_NORMED)
                        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                        # If a note is detected above a certain threshold, simulate keypresses
                        if max_val > threshold:
                            x, y = max_loc[0] + note_image.shape[1] // 2, max_loc[1] + note_image.shape[0] // 2
                            pyautogui.keyDown(key1)
                            pyautogui.keyDown(key2)
                            pyautogui.keyUp(key2)
                            pyautogui.keyUp(key1)
                    else:
                        print(f"Image '{note_image_path}' is not a color image.")
                else:
                    print(f"Error loading the image '{note_image_path}'.")
        else:
            print("Error capturing screenshot.")
            
    except Exception as e:
        print(f"Error: {e}")

    # Add synchronization logic based on the game's tempo
    # For example, calculate expected note timings and sleep accordingly

    time.sleep(0.01)  # Adjust sleep duration as needed

