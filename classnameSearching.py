import pywinauto

# app = Application(backend="uia").connect()

pwa_app = pywinauto.application.Application(backend="uia")
w_handle = pywinauto.findwindows.find_windows(class_name_re=r'.+')

for i in w_handle:
    print(i, "\t",end="")
    try:
        pwa_app.connect(handle = i)
        print(pwa_app.top_window().class_name(), "\t", pwa_app.top_window().window_text())
    except:
        print("welp shoot")
# app = pwa_app.connect(handle = w_handle[0])