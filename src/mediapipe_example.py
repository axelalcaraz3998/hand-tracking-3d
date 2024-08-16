import os

import numpy as np
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Get model path relative to current directory
dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "./models/hand_landmarker.task")

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create hand landmarker instance
def print_result(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
  print(f"Hand landmarker result: {result}")

options = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  result_callback = print_result  
)

with HandLandmarker.create_from_options(options) as landmarker:
  # Capture video from webcam using OpenCV
  capture = cv.VideoCapture(0, cv.CAP_ANY)

  # If camera is not detected, terminate program
  if not capture.isOpened():
    print("Can't open camera")
    exit()

  while True:
    # Capture frame
    ret, frame = capture.read()
    # Get frame timestamp in milliseconds and parse it to an integer
    frame_timestamp_ms = int(capture.get(cv.CAP_PROP_POS_MSEC))

    # If frame is not read correctly, exit loop
    if not ret:
      print("Can't receive frame, exiting")
      break

    # Convert frame to MediaPipe image object
    image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = image_rgb)

    # Hand landmarker
    landmarker.detect_async(mp_image, frame_timestamp_ms)

    # Show image in a window
    cv.imshow("Webcam", frame)

    # Condition to exit loop
    if cv.waitKey(1) == (ord('q') or ord('Q')):
      break

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()