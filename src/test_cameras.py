import os

import numpy as np
import cv2 as cv
import dotenv

# Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CAMERA_0_ID = int(os.getenv("CAMERA_0_ID"))
CAMERA_1_ID = int(os.getenv("CAMERA_1_ID"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))

is_currently_active = True

def test_cameras():
  # Set webcam capture
  capture_0 = cv.VideoCapture(CAMERA_0_ID, cv.CAP_DSHOW)
  capture_1 = cv.VideoCapture(CAMERA_1_ID, cv.CAP_DSHOW)

  # Set frame width and height
  capture_0.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  capture_0.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
  capture_1.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  capture_1.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

  # If either of the cameras is not detected, terminate program
  if not capture_0.isOpened() or not capture_1.isOpened():
    print("Can't open either of the cameras")
    exit()

  while True:
    # Capture frame
    ret_0, frame_0 = capture_0.read()
    ret_1, frame_1 = capture_1.read()

    # If frame is not read correctly, terminate program
    if not ret_0 or not ret_1:
      print("Can't receive frame")
      break
      
    cv.imshow("Camera 0", frame_0)
    cv.imshow("Camera 1", frame_1)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      break    

  # Release captures and destroy windows
  capture_0.release()
  capture_1.release()
  cv.destroyAllWindows()