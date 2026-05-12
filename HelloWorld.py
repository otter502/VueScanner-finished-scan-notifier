print("Hello, World!")
# pip install playsound
# pip install pywinauto
# pip install re
# somehow fixes issue?
# pip install simpleaudio 

import pywinauto
import time

# app = Application(backend="uia").connect()

pwa_app = pywinauto.application.Application(backend="uia")
w_handle = pywinauto.findwindows.find_windows(title_re=r'Vue.+')
app = pwa_app.connect(handle = w_handle[0])

# topWindow = app.top_window()
# print(app.top_window().StatusBar)
# app.top_window().dump_tree()
# app.top_window().StatusBar.dump_tree()
# print(app.top_window().StatusBar._ctrl_identifiers().values())
# print(app.top_window().StatusBar.Static.dump_tree())
# print(app.top_window().StatusBar.Static.exists())
# print(app.top_window().StatusBar.Static.window_text())
# print(app.top_window().StatusBar.children()[0].window_text())

"Scan ..."

from pydub import AudioSegment
from pydub import playback;

notifSound = AudioSegment.from_mp3("./notifSound.mp3")
print('playing sound using pydub')
playback.play(notifSound)
# (soundBite)

# stop

lastText = app.top_window().StatusBar.children()[0].window_text()
currText = ""

while(app.top_window().exists()):
    try:
        currText = app.top_window().StatusBar.children()[0].window_text()
    except:
        currText = lastText
        print("error pls fix!")
    
    # if last text contained "save" or "scan" and curr text does not?

    def isScanningStatus(s):
        return ("save" in s) or ("scan" in s)

    if((not isScanningStatus(currText)) and (isScanningStatus(lastText))):
        playback.play(notifSound)
        print("finished scanning @ " + time.asctime)
    
    
    time.sleep(1)
