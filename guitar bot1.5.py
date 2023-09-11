import pygetwindow as gw
import pyscreeze
import cv2
import numpy as np
import time
import pyautogui
from matplotlib import pyplot as plt

# Specify the title of the game window
window_title = "Clone Hero"

# Define the note images and corresponding keys
note_images = {
    r"green_note.jpg": ("a", "1"),
    r"red_note.jpg": ("s", "1"),
    r"yellow_note.png": ("j", "1"),
    r"blue_note.png": ("k", "1"),
    r"orange_note.png": ("l", "1"),
}

# Threshold for matching
threshold = 0.6

# Find the game window by title
game_window = gw.getWindowsWithTitle(window_title)[0]

while True:
    # Capture a screenshot of the game window
    screenshot = pyscreeze.screenshot(region=(
        game_window.left, game_window.top,
        game_window.width, game_window.height
    ))

    screenshot = np.array(screenshot)

    # Iterate through each note image and corresponding keys
    for note_image_path, (key1, key2) in note_images.items():
        # Load the note image with the cv2.IMREAD_COLOR flag
        note_image = cv2.imread(note_image_path, cv2.IMREAD_GRAYSCALE)

        # Check if image loading was successful
        if note_image is not None and isinstance(note_image, np.ndarray):
            # Check if the image is a color image (not grayscale)
            # if len(note_image.shape) == 3:
                # Convert the screenshot to grayscale for template matching
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)

                # Perform template matching
                result = cv2.matchTemplate(screenshot_gray, note_image, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

                top_left = max_loc
                bottom_right = (top_left[0] + 48, top_left[1] + 36)

                # If a note is detected above a certain threshold, simulate keypresses
                if max_val > threshold:
                    cv2.rectangle(screenshot, top_left, bottom_right, 255, 2)
                    plt.subplot(121),plt.imshow(result,cmap = 'gray')
                    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                    plt.subplot(122),plt.imshow(screenshot,cmap = 'gray')
                    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                    plt.suptitle("cv.TM_CCOEFF")
                    plt.show()
                    # exit(0)
                    x, y = max_loc[0] + note_image.shape[1] // 2, max_loc[1] + note_image.shape[0] // 2
                    pyautogui.keyDown(key1)
                    pyautogui.keyDown(key2)
                    pyautogui.keyUp(key2)
                    pyautogui.keyUp(key1)
            # else:
            #     print(f"Image '{note_image_path}' is not a color image.")
        else:
            print(f"Error loading the image '{note_image_path}'.")

    # Add synchronization logic based on the game's tempo
    # For example, calculate expected note timings and sleep accordingly

    time.sleep(0.5)  # Adjust sleep duration as needed

