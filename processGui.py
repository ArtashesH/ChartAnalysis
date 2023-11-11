import pyautogui
import time

pyautogui.moveTo(500, 500)


pyautogui.click()   

while 1:
   # with pyautogui.hold('shift'):  # Press the Shift key down and hold it.
     #   pyautogui.press(['right', 'right', 'right', 'right','right', 'right', 'right', 'right', 'right', 'right', 'right', 'right' ]) 
       # pyautogui.press(['right', 'right', 'right', 'right','right', 'right', 'right', 'right', 'right', 'right', 'right', 'right','right', 'right', 'right', 'right','right', 'right', 'right', 'right', 'right', 'right', 'right', 'right'  ]) 
    pyautogui.press(['right'],presses=10)   
    time.sleep(20)
