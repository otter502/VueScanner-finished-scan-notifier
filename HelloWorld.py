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


lastText = ""
currText = ""
scanStatus = 0

print("started monitoring @ ", time.asctime())

try:
    while(app.top_window().exists()):
        try:
            currText = app.top_window().StatusBar.children()[0].window_text()
        except:
            currText = lastText
            print("error pls fix! @ ", time.asctime(), "\n", currText, " : ", lastText, " : ", scanStatus)
        
        # if last text contained "save" or "scan" and curr text does not?

        # neither = 0
        # scanning = 1
        # previewing = 2
        def isScanningStatus(s):
            return (1 if (s.lower().startswith("scan") or ("save" in s.lower())) else 0) + (2 if (s.lower().startswith("preview")) else 0)

        if (isScanningStatus(currText) == 0 and scanStatus != 0): # something finished!
                playsound("./notifSound.mp3")
                if (scanStatus == 2):
                    print("finished previewing @ ", time.asctime())
                if (scanStatus == 1):
                    print("finished scanning @ ", time.asctime())
                scanStatus = 0



        if (isScanningStatus(currText)!= 0 and scanStatus == 0): # something started!
            if (isScanningStatus(currText) == 2):
                print("started previewing @ ", time.asctime())
            if (isScanningStatus(currText) == 1):
                print("started scanning @ ", time.asctime())
            scanStatus = isScanningStatus(currText)
            



        lastText = currText
        time.sleep(1)
except:
    print("fatal error pls fix! @ ", time.asctime(), "\n", currText, " : ", lastText, " : ", scanStatus)

