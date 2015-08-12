#!/Python27/python.exe -u
import numpy as np
import cv2
import ctypes
from ctypes import wintypes
import datetime
import time
displayOn = True

import win32gui
import win32con

def monitorOn() :
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,
                         win32con.SC_MONITORPOWER, -1)

def monitorOff() :
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,
                       win32con.SC_MONITORPOWER, 2)

def monitorSleep() :
    win32gui.SendMessage(win32con.HWND_BROADCAST, win32con.WM_SYSCOMMAND,
                       win32con.SC_MONITORPOWER, 1)   

def downtime() :
    global displayOn
    n = time.localtime()
    h = n.tm_hour - 5
    m = n.tm_min
    if  h >= 17 or h < 9 :
        if (displayOn):
            displayOn = False
            monitorOff()
    else :
        if (displayOn == False):
            displayOn = True
            monitorOn()

FindWindow = ctypes.windll.user32.FindWindowA
FindWindow.restype = wintypes.HWND
FindWindow.argtypes = [
    wintypes.LPCSTR, #lpClassName
    wintypes.LPCSTR, #lpWindowName
]

SetWindowPos = ctypes.windll.user32.SetWindowPos
SetWindowPos.restype = wintypes.BOOL
SetWindowPos.argtypes = [
    wintypes.HWND, #hWnd
    wintypes.HWND, #hWndInsertAfter
    ctypes.c_int,  #X
    ctypes.c_int,  #Y
    ctypes.c_int,  #cx
    ctypes.c_int,  #cy
    ctypes.c_uint, #uFlags
] 

TOGGLE_HIDEWINDOW = 0x80
TOGGLE_UNHIDEWINDOW = 0x40

def hide_taskbar():
    handleW1 = FindWindow(b"Shell_traywnd", b"")
    SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_HIDEWINDOW)

def unhide_taskbar():
    handleW1 = FindWindow(b"Shell_traywnd", b"")
    SetWindowPos(handleW1, 0, 0, 0, 0, 0, TOGGLE_UNHIDEWINDOW)

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame', cv2.WND_PROP_FULLSCREEN)          
cv2.setWindowProperty('frame', cv2.WND_PROP_FULLSCREEN, cv2.cv.CV_WINDOW_FULLSCREEN)
hide_taskbar()
ctypes.windll.user32.ShowCursor(False)
count = 0;
while(True):
    count = count + 1
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if (count % 100 == 0) :
        downtime()

cap.release()
cv2.destroyAllWindows()
ctypes.windll.user32.ShowCursor(True)
unhide_taskbar()

