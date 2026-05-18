#full rewrite

import pywinauto
import time
from playsound3 import playsound
import multiprocessing as mp

pwa_app = pywinauto.application.Application(backend="uia")
w_handle = pywinauto.findwindows.find_windows(title_re=r'Vue.+')
app = pwa_app.connect(handle = w_handle[0])
statusBarText = app.top_window().StatusBar.children()[0]

timeoutTime = 5 # 5 second timeout

class CustomException(Exception):
    def __init__(self,msg):
        self.msg=msg
        print( 'custom exception occurred')

def getWindowText(queue):
    #clear error status

    if not app.top_window().exists():
        queue.put("!topWindow does not exist")
    elif not statusBarText:
        queue.put("!statusBar does not exist")
    else:
        queue.put("#" + statusBarText.window_text().lower().strip())


# nothing = 0
# scan = 1
# preview = 2
def interpretText(text):
    return (1 if (text.startswith("#scan") or ("save" in text)) else 0) + (2 if (text.startswith("#preview")) else 0)


def handleOutput(prevState, currState):
    currTime = time.asctime()

    if prevState == currState:
        return # nothing happened!
    if (prevState == 0):
        print("Started ", "scanning" if currState == 1 else "previewing", " @ ", currTime)
    elif (currState == 0):
        playsound("./notifSound.mp3")
        print("Finished ", "scanning" if prevState == 1 else "previewing", " @ ", currTime)
    else:
        playsound("./errorSound.mp3")
        print("Went from ", "scanning" if prevState == 1 else "previewing", " to ", "scanning" if currState == 1 else "previewing", " @ ", currTime)


if __name__ == '__main__':
    previousState = 0
    q = mp.Queue()

    print("Starting monitoring @ ", time.asctime())

    try: 
        while app.top_window().exists():
            p = mp.Process(target = getWindowText, args=(q,))
            p.start()

            p.join(timeoutTime + 0.01)

            if p.is_alive():
                p.terminate()
                p.join()
                print('process took too long')
                if(q.empty): q.put("none!") # let's see what this does!

            result = q.get(block=True, timeout=timeoutTime)
            
            if (result.startswith("!")):
                raise CustomException(result)

            currentState = interpretText(result)

            handleOutput(previousState, currentState)

            previousState = currentState
            time.sleep(1)
    except Exception as e:
        q.close()
        raise(e)
