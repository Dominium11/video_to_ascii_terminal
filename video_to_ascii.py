import cv2
from PIL import Image
from os import system
import ctypes
from sys import argv, stdout
import time 

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
try:
     captureFile = argv[1]
     resMod = int(argv[2])
except:
     captureFile = "bad_apple.mp4"
     resMod = 3

vidcap = cv2.VideoCapture(captureFile)
count = 0
success = True
targetFramerate = int(vidcap.get(cv2.CAP_PROP_FPS))
width  = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

#print(width)
#print(height)
width = width//resMod
height = height//resMod

font = CONSOLE_FONT_INFOEX()
font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
font.nFont = 12
match resMod:
     case 1:
          fontSize = 2
     case 2:
          fontSize = 6
     case 3:
          fontSize = 11
     case 4:
          fontSize = 15
     case 5:
          fontSize = 19
font.dwFontSize.X = fontSize
font.dwFontSize.Y = fontSize
font.FontFamily = 54
font.FontWeight = 400
font.FaceName = "Lucida Sans Typewriter"

handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
ctypes.windll.kernel32.SetCurrentConsoleFontEx(
        handle, ctypes.c_long(False), ctypes.pointer(font))

system(f'mode con: cols={width} lines={height}')

class bcolors:
     BWHITE = '\033[97m'
     WHITE = '\033[37m'
     BGREY = '\033[90m'
while success:
     start = time.time()
     success,image = vidcap.read()
     frame = ''
     frameX = []
     for cols in range(0,height):
          buffer = []
          for rows in range(0,width):
               x = image[cols*resMod][rows*resMod]
               x = x.tolist()      

               if(x[0]<25): buffer.append("$")
               elif(x[0]>225): buffer.append(" ")
               elif(x[0]<75): buffer.append("F")
               elif(x[0]<125): buffer.append("l")
               elif(x[0]<175): buffer.append("!")
               elif(x[0]<225): buffer.append(".")
          buffer.append("\n")
          frameX.append(''.join(buffer))
     frame = ''.join(frameX)
     system('cls')
     stdout.write(frame)
     end = time.time()
     elapsed = end-start
     if(elapsed<1/targetFramerate):
          time.sleep((1/targetFramerate)-elapsed)
     