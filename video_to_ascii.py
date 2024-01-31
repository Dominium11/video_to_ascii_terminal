import cv2
from PIL import Image
from os import system
import ctypes
from sys import argv

LF_FACESIZE = 32
STD_OUTPUT_HANDLE = -11

class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class CONSOLE_FONT_INFOEX(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_ulong),
                ("nFont", ctypes.c_ulong),
                ("dwFontSize", COORD),
                ("FontFamily", ctypes.c_uint),
                ("FontWeight", ctypes.c_uint),
                ("FaceName", ctypes.c_wchar * LF_FACESIZE)]

captureFile = argv[1]

vidcap = cv2.VideoCapture(captureFile)
count = 0
success = True
fps = int(vidcap.get(cv2.CAP_PROP_FPS))
width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(width)
#print(height)
resMod = 4
width = width//resMod
height = height//resMod

font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
font.dwFontSize.X = 16-2*resMod
font.dwFontSize.Y = 16-2*resMod
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Lucida Sans Typewriter"

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))

system(f'mode con: cols={width} lines={height}')

while success:
     success,image = vidcap.read()
     frame = ''
     for cols in range(0,height):
          for rows in range(0,width):
               x = image[cols*resMod][rows*resMod][0]      
               if(x<25): frame += "$"
               elif(x>225): frame += " "
               elif(x<75): frame += "F"
               elif(x<125): frame += "l"
               elif(x<175): frame += "!"
               elif(x<225): frame += "."
          frame += "\n"
     system('cls')
     print(frame)
     