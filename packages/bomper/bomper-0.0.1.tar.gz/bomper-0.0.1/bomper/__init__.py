def spam(Text,Number,Time):
    import pyautogui as gui
    import time

    time.sleep(Time)

    for i in range(0,Number):
        gui.typewrite(Text)
        gui.press("Enter")

    print("Done!")