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
def result_callback(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
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
  # Get with and height of frame
  width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
  height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
  print(width, height)
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
      # # Gets position of middle finger tip
      # rect_upper_bound = int(results["hand_landmarks"][12].y * height)
      # # Gets position of wrist
      # rect_lower_bound = int(results["hand_landmarks"][0].y * height)
      # # Gets position of thumb tip
      # rect_left_bound = int(results["hand_landmarks"][4].x * width)
      # # Gets position of pinky tip
      # rect_right_bound = int(results["hand_landmarks"][20].x * width)

      # # Draw outer rectangle
      # cv.rectangle(frame, (rect_left_bound, rect_upper_bound), (rect_right_bound, rect_lower_bound), (0, 255, 0), 2)

      # # Write coordinates of center position
      # coords = f"({(results["hand_landmarks"][0].x + results["hand_landmarks"][9].x) / 2}, {(results["hand_landmarks"][0].y + results["hand_landmarks"][9].y) / 2})"
      # cv.putText(frame, coords, (0, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1)

      # # Write handedness
      # cv.putText(frame, results["handedness"], (rect_right_bound, (rect_upper_bound - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

      # Render landmarks in hand
      render_landmarks(blank_image, width, height, results["hand_landmarks"])

    # Show image in a window
    cv.imshow("Webcam capture", frame)
    cv.imshow("Hand tracking", blank_image)      

    # Condition to exit loop
    if cv.waitKey(1) == (ord('q') or ord('Q')):
      break

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()