#full rewrite

import pywinauto
import time
from playsound3 import playsound
import multiprocessing as mp

pwa_app = pywinauto.application.Application(backend="uia")


timeoutTime = 5 # 5 second timeout
debug = True

class CustomException(Exception):
    def __init__(self,msg):
        self.msg=msg
        print( 'custom exception occurred')

def getWindowText(queue):
    if debug: print("\tgetting text")
    w_handle = pywinauto.findwindows.find_windows(title_re=r'Vue.+')
    app = pwa_app.connect(handle = w_handle[0])
    statusBarText = app.top_window().StatusBar.children()[0]
    if debug: print("\tmade status bar")
    #clear error status

    if not app.top_window().exists():
        queue.put("!topWindow does not exist")
    elif not statusBarText:
        queue.put("!statusBar does not exist")
    else:
        if debug: print("\tgrabbing data")
        queue.put("#" + statusBarText.window_text().lower().strip())


# nothing = 0
# scan = 1
# preview = 2
def interpretText(text):
    if debug: print("\tinterpretting text: ", text)
    return (1 if (text.startswith("#scan") or ("save" in text)) else 0) + (2 if (text.startswith("#preview")) else 0)


def handleOutput(prevState, currState):
    if debug: print("\thandling output", prevState, ":", currState)

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
        while True:
            if debug: print("\n-----\n\n\tstart loop")
            
            p = mp.Process(target = getWindowText, args=(q,))
            p.start()
            if debug: print("\tp.start()")

            p.join(timeoutTime + 0.01)
            if debug: print("\tp.join()")

            if p.is_alive():
                p.terminate()
                p.join()
                print('process took too long')
                if(q.empty): 
                    if debug: print("\tqueue Empty, continue")
                    continue
                elif debug: print("\tqueue not empty")
                

            result = q.get(block=True, timeout=timeoutTime)
            if debug: print("\tresult: ", result)
            
            if (result.startswith("!")):
                raise CustomException(result)

            currentState = interpretText(result)

            handleOutput(previousState, currentState)

            previousState = currentState

            if debug: print("\tfinished loop ", previousState, currentState)
            time.sleep(1)
    except Exception as e:
        q.close()
        raise(e)
