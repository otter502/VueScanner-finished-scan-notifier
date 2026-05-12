print("Hello, World!")
# pip install playsound3
# pip install pywinauto
# pip install re
# somehow fixes issue?


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


from playsound3 import playsound

# notifSound = AudioSegment.from_mp3()
print('playing sound using playsound3')
playsound("./notifSound.mp3")
# (soundBite)

# stop


lastText = app.top_window().StatusBar.children()[0].window_text()
currText = ""

print("started monitoring @ ", time.asctime())

while(app.top_window().exists()):
    try:
        currText = app.top_window().StatusBar.children()[0].window_text()
    except:
        currText = lastText
        print("error pls fix!")
    
    # if last text contained "save" or "scan" and curr text does not?

    def isScanningStatus(s):
        return (s.lower().startswith("scan")) or ("save" in s.lower())

    if((not isScanningStatus(currText)) and (isScanningStatus(lastText))):
        playsound("./notifSound.mp3")
        print("finished scanning @ ", time.asctime())
    
    
    time.sleep(1)
