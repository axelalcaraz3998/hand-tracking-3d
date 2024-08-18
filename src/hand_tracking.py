import os

import numpy as np
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Get model path relative to current directory
dirname = os.path.dirname(__file__)
model_path = os.path.join(dirname, "./models/hand_landmarker.task")

# MediaPipe hand landmarker variables
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Results dictionary
results = {
  "hand_orientation": None,
  "hand_landmarks": None,
}

# Callback function
def result_callback(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
  if (len(result.handedness) > 0):
    results["hand_orientation"] = result.handedness[0][0].display_name
  else:
    results["hand_orientation"] = None

  if (len(result.hand_landmarks) > 0):
    results["hand_landmarks"] = result.hand_landmarks[0]
  else:
    results["hand_landmarks"] = None

# Hand landmarker options
options = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  result_callback = result_callback  
)

# Create hand landmarker instance
timestamp = 0
with HandLandmarker.create_from_options(options) as landmarker:
  # Capture video from webcam using OpenCV
  capture = cv.VideoCapture(0, cv.CAP_DSHOW)
  width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
  height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

  # If camera is not detected, terminate program
  if not capture.isOpened():
    print("Can't open camera")
    exit()

  while True:
    # Capture frame
    ret, frame = capture.read()

    # If frame is not read correctly, exit loop
    if not ret:
      print("Can't receive frame, exiting")
      break

    # Convert frame to MediaPipe image object
    mp_image = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame)

    # Hand landmarker
    timestamp += 1
    landmarker.detect_async(mp_image, timestamp)

    if results["hand_landmarks"]:
      # Gets position of middle finger tip
      rect_upper_bound = int(results["hand_landmarks"][12].y * height)
      # Gets position of wrist
      rect_lower_bound = int(results["hand_landmarks"][0].y * height)
      # Gets position of thumb tip
      rect_left_bound = int(results["hand_landmarks"][4].x * width)
      # Gets position of pinky tip
      rect_right_bound = int(results["hand_landmarks"][20].x * width)

      # Get position of middle of palm using the avg of the x and y coordinates of wrist and middle finger mcp
      middle_of_palm_x = int((int(results["hand_landmarks"][0].x * width) + int(results["hand_landmarks"][9].x * width)) / 2)
      middle_of_palm_y = int((int(results["hand_landmarks"][0].y * height) + int(results["hand_landmarks"][9].y * height)) / 2)

      # Draw circle in middle of palm
      cv.circle(frame, (middle_of_palm_x, middle_of_palm_y), 6, (0, 0, 0), -1)
      cv.circle(frame, (middle_of_palm_x, middle_of_palm_y), 4, (0, 255, 0), -1)

      # Draw outer rectangle
      cv.rectangle(frame, (rect_left_bound, rect_upper_bound), (rect_right_bound, rect_lower_bound), (0, 255, 0), 2)

      # Write coordinates of center position
      coords = f"({(results["hand_landmarks"][0].x + results["hand_landmarks"][9].x) / 2}, {(results["hand_landmarks"][0].y + results["hand_landmarks"][9].y) / 2})"
      cv.putText(frame, coords, (0, 30), cv.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 1)

      if results["hand_orientation"]:
        # Write hand orientation
        cv.putText(frame, results["hand_orientation"], (rect_right_bound, (rect_upper_bound - 10)), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

      for landmark in results["hand_landmarks"]:
        # Convert normalized coordinates to pixels in frame
        x_pos = int(landmark.x * width)
        y_pos = int(landmark.y * height)
        # Draw landmarks in hand
        cv.circle(frame, (x_pos, y_pos), 6, (0, 0, 0), -1)
        cv.circle(frame, (x_pos, y_pos), 4, (255, 255, 255), -1)

    # Show image in a window
    cv.imshow("Webcam Capture", frame)      

    # Condition to exit loop
    if cv.waitKey(1) == (ord('q') or ord('Q')):
      break

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()