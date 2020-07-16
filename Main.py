import threading
from time import sleep

import pyautogui as auto
from PIL import ImageGrab
from pynput import keyboard


def check_fishing():  # Captures Image, Returns True If Fishing Box Found
    capture = ImageGrab.grab(bbox=(938, 450, 980, 475))  # Left, Upper, Right, Lower

    # Grabs the RGB Codes For the 2 Most Prevalent Colors Within The Screen Clip
    # As the Correct Screen Clip Should Only Contain 2 Colors, This Seems to Work Decently Well
    colors = capture.quantize(colors=2, method=2).getpalette()[:6]

    # Compare Them To The Fishing Box Colors
    return colors == [228, 210, 178, 95, 56, 34]


def fish():  # Run The Auto Fisher - This Will Be Run as A Thread
    while True:
        global stop_thread
        while stop_thread:

            if check_fishing():
                # Catch Fish
                auto.click()
                sleep(0.5)

                # Full Cast
                auto.mouseDown()
                sleep(1.7)
                auto.mouseUp()
            sleep(0.5)
        sleep(1)


print("Auto Fisher Starting, Press Right Alt To Toggle On/Off")
stop_thread = True
fisher = threading.Thread(target=fish)
fisher.start()


# Callback Function To Toggle Fisher
def toggle(key):
    if key == keyboard.Key.alt_r:
        global stop_thread
        print("callback triggered, Fishing is now: ", stop_thread)
        stop_thread = not stop_thread


# Blocking Keyboard Listener
with keyboard.Listener(on_press=toggle) as listener:
    listener.join()
