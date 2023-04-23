from win32gui import GetClientRect, ClientToScreen, FindWindow, GetCursorPos, GetForegroundWindow, GetDC, GetPixel
from pymem import Pymem
import numpy as np
from transparent_window import TransparentWindow
import cv2 as cv
from time import sleep, time
from PyQt5.QtWidgets import QApplication
import sys

RADIUS = 17

class GunboundProcess:
    def __init__(self, process):
        self.process = process

def determine_client_area_rect(hwnd):
    left, top, right, bottom = GetClientRect(hwnd)
    left2, top2 = ClientToScreen(hwnd, (left, top))
    right2, bottom2 = ClientToScreen(hwnd, (right, bottom))
    client_area_rect = {
        'left': left2,
        'top': top2,
        'width': right2 - left2,
        'height': bottom2 - top2
    }
    return client_area_rect

def create_image_with_size(width, height):
    #retorna array
    image = np.full((height, width, 4), (0, 0, 0, 0), dtype=np.uint8)
    return image

def drawCircle(image):
	x, y = GetCursorPos()
	print(x, y)
	cv.circle(image, (x, y), RADIUS, (0, 0, 255, 255), thickness=1)
	

def main () :
	window = FindWindow(None, 'GunBound')
	print("aaaaaaa",window)
	process = GunboundProcess(Pymem('gitzgame.gme'))
	print("bbbbbbb",process)

	application = QApplication(sys.argv)
	transparent_window = TransparentWindow()
	transparent_window.show()

	while True:
		if window != GetForegroundWindow():
				client_area_rect = determine_client_area_rect(window)
				image = create_image_with_size(client_area_rect['width'], client_area_rect['height'])
				image[0, 0] = (0, 0, 255, 255)
				transparent_window.show_image(image)
				while window != GetForegroundWindow():
						sleep(1 / 60)
		client_area_rect = determine_client_area_rect(window)
                
		transparent_window.setGeometry(
		client_area_rect['left'],
		client_area_rect['top'],
		client_area_rect['width'],
		client_area_rect['height']
		)
        
		image = create_image_with_size(client_area_rect['width'], client_area_rect['height'])

		drawCircle(image)
			    
		image[0, 0] = (0, 0, 255, 255)

		transparent_window.show_image(image)
		cv.waitKey(1)

main()