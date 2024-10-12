import os

import dotenv
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from render.render_landmarks import render_landmarks
from render.render_hand_3d import plot_hand
from utils.dlt import DLT

# Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CAMERA_0_ID = int(os.getenv("CAMERA_0_ID"))
CAMERA_1_ID = int(os.getenv("CAMERA_1_ID"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))
MIN_HAND_DETECTION_CONFIDENCE = float(os.getenv("MIN_HAND_DETECTION_CONFIDENCE"))
MIN_HAND_PRESENCE_CONFIDENCE = float(os.getenv("MIN_HAND_PRESENCE_CONFIDENCE"))
MIN_TRACKING_CONFIDENCE = float(os.getenv("MIN_TRACKING_CONFIDENCE"))

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
}

results_side = {
  "handedness": None,
  "hand_landmarks": None,
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
  num_hands = 1,
  min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
  min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
  min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
  result_callback = result_callback_front
)

# Hand landmarker options for side camera
options_side = HandLandmarkerOptions(
  base_options = BaseOptions(model_asset_path = model_path),
  running_mode = VisionRunningMode.LIVE_STREAM,
  num_hands = 1,
  min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
  min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
  min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
  result_callback = result_callback_side
)

# Create hand landmarker instance for front camera
landmarker_front = HandLandmarker.create_from_options(options_front)
# Create hand landmarker instance for side camera
landmarker_side = HandLandmarker.create_from_options(options_side)

# Capture video from webcam using OpenCV
capture_front = cv.VideoCapture(CAMERA_0_ID, cv.CAP_DSHOW)
capture_side = cv.VideoCapture(CAMERA_1_ID, cv.CAP_DSHOW)

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

# Last valid 3D estimation
last_3d_estimation = None

# Create hand plots
# fig = plt.figure()
# ax = fig.add_subplot(111, projection = "3d")
# plt.show()

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
  if results_front["hand_landmarks"]:
    # Render landmarks in hand
    render_landmarks(blank_image_front, width, height, results_front["hand_landmarks"])
  
  if results_side["hand_landmarks"]:
    # Render landmarks in hand
    render_landmarks(blank_image_side, width, height, results_side["hand_landmarks"])

  # Keypoints
  keypoints_front = []
  keypoints_side = []
  keypoints_3d = []
  world_3d = []

  # Get 3D estimation of keypoints
  if results_front["hand_landmarks"] and results_side["hand_landmarks"]:
    for landmark_front in results_front["hand_landmarks"]:
      point_x = int(round(FRAME_WIDTH * landmark_front.x))
      point_y = int(round(FRAME_HEIGHT * landmark_front.y))
      keypoints = [point_x, point_y]
      keypoints_front.append(keypoints)

    for landmark_side in results_side["hand_landmarks"]:
      point_x = int(round(FRAME_WIDTH * landmark_side.x))
      point_y = int(round(FRAME_HEIGHT * landmark_side.y))
      keypoints = [point_x, point_y]
      keypoints_side.append(keypoints)

    for uv1, uv2 in zip(keypoints_front, keypoints_side):
      keypoints = DLT(uv1, uv2)
      keypoints_3d.append(keypoints)

    keypoints_3d = np.array(keypoints_3d).reshape((21, 3))
    world_3d.append(keypoints_3d)
    last_3d_estimation = world_3d
  else:
    world_3d = last_3d_estimation

  # Show image in a window
  # cv.imshow("Front Webcam Capture", frame_front)
  # cv.imshow("Side Webcam Capture", frame_side)
  cv.imshow("Hand Tracking Front Camera", blank_image_front)
  cv.imshow("Hand Tracking Side Camera", blank_image_side)

  # Plot hand in 3D space
  if last_3d_estimation:
    # plot_hand(world_3d, ax)
    if frame_timestamp_front % 10 == 0:
      print(world_3d)

  # Get pressed key
  pressed_key = cv.waitKey(1) & 0xFF

  # Condition to exit loop
  if pressed_key == ord('q') or pressed_key == ord('Q'):
    break

# Release capture and close windows
capture_front.release()
capture_side.release()
cv.destroyAllWindows()