import os

from dotenv import load_dotenv
import numpy as np
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from render.render_landmarks import render_landmarks

# Load env variables
load_dotenv()
FRONT_CAMERA_ID = int(os.getenv("FRONT_CAMERA_ID"))
SIDE_CAMERA_ID = int(os.getenv("SIDE_CAMERA_ID"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))

# Get model path relative to current directory
dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "./models/hand_landmarker.task")

# MediaPipe hand landmarker objects
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Results dictionaries
results_front = {
  "handedness": None,
  "hand_landmarks": None,
  "hand_orientation": None,
}

results_side = {
  "handedness": None,
  "hand_landmarks": None,
  "hand_orientation": None,
}

# Callback function for front camera
def result_callback_front(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
  # If a hand is detected assing hand landmarker result to results dictionary
  if (len(result.handedness) > 0 and len(result.hand_landmarks) > 0):
    results_front["handedness"] = result.handedness[0][0].display_name
    results_front["hand_landmarks"] = result.hand_landmarks[0]
  else:
    results_front["handedness"] = None
    results_front["hand_landmarks"] = None
    results_front["hand_orientation"] = None

# Callback function for side camera
def result_callback_side(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
  # If a hand is detected assing hand landmarker result to results dictionary
  if (len(result.handedness) > 0 and len(result.hand_landmarks) > 0):
    results_side["handedness"] = result.handedness[0][0].display_name
    results_side["hand_landmarks"] = result.hand_landmarks[0]
  else:
    results_side["handedness"] = None
    results_side["hand_landmarks"] = None
    results_side["hand_orientation"] = None

# Hand landmarker options for front camera
options_front = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  result_callback = result_callback_front
)
# Hand landmarker options for side camera
options_side = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  result_callback = result_callback_side
)

# Create hand landmarker instance for front camera
landmarker_front = HandLandmarker.create_from_options(options_front)
# Create hand landmarker instance for side camera
landmarker_side = HandLandmarker.create_from_options(options_side)

# Capture video from webcam using OpenCV
capture_front = cv.VideoCapture(FRONT_CAMERA_ID, cv.CAP_DSHOW)
capture_side = cv.VideoCapture(SIDE_CAMERA_ID, cv.CAP_DSHOW)

capture_front.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture_front.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
capture_side.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
capture_side.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

# Get width and height of frame
width = FRAME_WIDTH
height = FRAME_HEIGHT

# Frame timestamp initialization
frame_timestamp_front = 0
frame_timestamp_side= 0

# If either camera is not detected, terminate program
if not capture_front.isOpened() or not capture_side.isOpened():
  print("Can't open either of the cameras")
  exit()

while True:
  # Capture frame
  ret_front, frame_front = capture_front.read()
  ret_side, frame_side = capture_side.read()

  frame_timestamp_front += 1
  frame_timestamp_side += 1

  # Empty canvas
  blank_image_front = np.zeros((int(height), int(width), 3), np.uint8)
  blank_image_side = np.zeros((int(height), int(width), 3), np.uint8)

  # If frame is not read correctly, exit loop
  if not ret_front or not ret_side:
    print("Can't receive frame, exiting loop")
    break

  # Convert frame to MediaPipe image object
  mp_image_front = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame_front)
  mp_image_side = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame_side)

  # Hand landmarker detection
  landmarker_front.detect_async(mp_image_front, frame_timestamp_front)
  landmarker_side.detect_async(mp_image_side, frame_timestamp_side)

  # If a hand is detected render information into frame
  if results_front["hand_landmarks"] and results_front["handedness"]:
    # Render landmarks in hand
    render_landmarks(blank_image_front, width, height, results_front["hand_landmarks"])
  
  if results_side["hand_landmarks"] and results_side["handedness"]:
    # Render landmarks in hand
    render_landmarks(blank_image_side, width, height, results_side["hand_landmarks"])

  # Show image in a window
  cv.imshow("Front Webcam Capture", frame_front)
  cv.imshow("Side Webcam Capture", frame_side)
  cv.imshow("Hand Tracking Front Camera", blank_image_front)
  cv.imshow("Hand Tracking Side Camera", blank_image_side)

  # Get pressed key
  pressed_key = cv.waitKey(1) & 0xFF

  # Condition to exit loop
  if pressed_key == ord('q') or pressed_key == ord('Q'):
    break

# Release capture and close windows
capture_front.release()
capture_side.release()
cv.destroyAllWindows()