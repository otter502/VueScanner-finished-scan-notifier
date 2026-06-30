'''
# install tesseract https://github.com/UB-Mannheim/tesseract/wiki
pip install pyscreenshot
pip install pyautogui
pip install keyboard
pip install pytesseract
pip install playsound3
pip install PIL # just in case!
'''

import time
from PIL import Image
import pyscreenshot
import pyautogui
import keyboard
import pytesseract
from playsound3 import playsound

loopDelay = 3 # 3 seconds
filename = "screenshot.png"

def handleOutput(prevState, currState):
    currTime = time.asctime()

    if prevState == currState:
        return False # nothing happened!
    if (prevState == 0):
        print("Started ", "scanning" if currState == 1 else "previewing", " @ ", currTime)
        return True
    elif (currState == 0):
        playsound("./notifSound.mp3")
        print("Finished ", "scanning" if prevState == 1 else "previewing", " @ ", currTime)
        return True
    else:
        playsound("./errorSound.mp3")
        print("Went from ", "scanning" if prevState == 1 else "previewing", " to ", "scanning" if currState == 1 else "previewing", " @ ", currTime)
        return True

def interpretText(text: str):
    text = text.strip().lower()
    text = text.replace("'", "")
    text = text.replace("\"", "")
    text = text.replace("|", "")

    if (text.startswith("scan") or "save" in text):
        return 1 # actively scanning
    elif (text.startswith("preview")):
        return 2 # actively previewing
    else:
        return 0
    # return (1 if (text.startswith("#scan") or ("save" in text)) else 0) + (2 if (text.startswith("#preview")) else 0)



if __name__ == '__main__':
    print("waiting for alt+1")
    keyboard.wait("alt+1")
    pos1 = pyautogui.position()

    print("waiting for alt+2")
    keyboard.wait("alt+2")
    pos2 = pyautogui.position()

    def takeScreenshot():
        image = pyscreenshot.grab(bbox=(pos1.x, pos1.y, pos2.x, pos2.y))
        image.save(filename)
        return image

    image = takeScreenshot()
    image.show()

    data = (pytesseract.image_to_string(filename))
    print("text read from image: " + data)

    print("waiting for alt+3 to confirm placement & text")
    keyboard.wait("alt+3")
    print("starting watching")

    previousState = 0

    while (True):
        takeScreenshot()
        data = (pytesseract.image_to_string(filename))
        currentState = interpretText(data)
        # print("text in image:" + data)

        if handleOutput(previousState, currentState):
            print("text: " + data)

        previousState = currentState
        time.sleep(loopDelay)