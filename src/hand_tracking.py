import os

import numpy as np
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from render.render_landmarks import render_landmarks

# Get model path relative to current directory
dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "./models/hand_landmarker.task")

# MediaPipe hand landmarker objects
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Results dictionary
results = {
  "handedness": None,
  "hand_landmarks": None,
  "hand_orientation": None,
}

# Callback function
def result_callback(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
  # If a hand is detected assing hand landmarker result to results dictionary
  if (len(result.handedness) > 0 and len(result.hand_landmarks) > 0):
    results["handedness"] = result.handedness[0][0].display_name
    results["hand_landmarks"] = result.hand_landmarks[0]
  else:
    results["handedness"] = None
    results["hand_landmarks"] = None
    results["hand_orientation"] = None

# Hand landmarker options
options = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  result_callback = result_callback  
)

# Create hand landmarker instance
with HandLandmarker.create_from_options(options) as landmarker:
  # Capture video from webcam using OpenCV
  capture = cv.VideoCapture(0, cv.CAP_DSHOW)
  capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
  capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

  # Get width and height of frame
  width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
  height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

  # Frame timestamp initialization
  frame_timestamp = 0

  # If camera is not detected, terminate program
  if not capture.isOpened():
    print("Can't open camera")
    exit()

  while True:
    # Capture frame
    ret, frame = capture.read()
    frame_timestamp += 1

    # Empty canvas
    blank_image = np.zeros((int(height), int(width), 3), np.uint8)

    # If frame is not read correctly, exit loop
    if not ret:
      print("Can't receive frame, exiting loop")
      break

    # Convert frame to MediaPipe image object
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)

    # Hand landmarker detection
    landmarker.detect_async(mp_image, frame_timestamp)

    # If a hand is detected render information into frame
    if results["hand_landmarks"] and results["handedness"]:
      # Render landmarks in hand
      render_landmarks(blank_image, width, height, results["hand_landmarks"])

    # Show image in a window
    cv.imshow("Webcam Capture", frame)
    cv.imshow("Hand Tracking", blank_image)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      break

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()