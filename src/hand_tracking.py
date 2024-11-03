import os

import dotenv
import cv2 as cv
import mediapipe as mp

def hand_tracking():
  print("========== Running Hand Tracking ==========")

  # Import utility functions
  from utils.draw_landmarks import draw_landmarks
  from utils.dlt import DLT

  # Load .env file
  dotenv_file = dotenv.find_dotenv()
  dotenv.load_dotenv(dotenv_file)

  # Load environment variables
  CAMERA_0_ID = int(os.getenv("CAMERA_0_ID"))
  CAMERA_1_ID = int(os.getenv("CAMERA_1_ID"))
  FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
  FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))
  MIN_HAND_DETECTION_CONFIDENCE = float(os.getenv("MIN_HAND_DETECTION_CONFIDENCE"))
  MIN_HAND_PRESENCE_CONFIDENCE = float(os.getenv("MIN_HAND_PRESENCE_CONFIDENCE"))
  MIN_TRACKING_CONFIDENCE = float(os.getenv("MIN_TRACKING_CONFIDENCE"))

  # Model path
  dirname = os.path.dirname(__file__)
  model_path = os.path.join(dirname, "./models/hand_landmarker.task")

  # MediaPipe hand landmarker objects
  BaseOptions = mp.tasks.BaseOptions
  BaseOptions = mp.tasks.BaseOptions
  HandLandmarker = mp.tasks.vision.HandLandmarker
  HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
  HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult
  VisionRunningMode = mp.tasks.vision.RunningMode

  # Results dictionaries
  results_0 = {
    "hand_landmarks": None,
  }

  results_1 = {
    "hand_landmarks": None,
  }

  # Callback functions
  def result_callback_0(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    # If a hand is detected assing hand landmarker result to results dictionary
    if len(result.hand_landmarks) > 0:
      results_0["hand_landmarks"] = result.hand_landmarks[0]
    else:
      results_0["hand_landmarks"] = None

  def result_callback_1(result: HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    # If a hand is detected assing hand landmarker result to results dictionary
    if len(result.hand_landmarks) > 0:
      results_1["hand_landmarks"] = result.hand_landmarks[0]
    else:
      results_1["hand_landmarks"] = None

  # Hand landmarker options
  options_0 = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
    min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
    min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
    result_callback = result_callback_0
  )

  options_1 = HandLandmarkerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
    min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
    min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
    result_callback = result_callback_1
  )
  
  # Set webcam capture
  capture_0 = cv.VideoCapture(CAMERA_0_ID, cv.CAP_DSHOW)
  capture_1 = cv.VideoCapture(CAMERA_1_ID, cv.CAP_DSHOW)

  # Set frame width and height
  capture_0.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  capture_0.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
  capture_1.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  capture_1.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

  # If either of the cameras is not detected, terminate program
  if not capture_0.isOpened():
    print("Can't open camera 0")
    exit()
  if not capture_1.isOpened():
    print("Can't open camera 1")
    exit()

  print("Camera 0 is working")
  print("Camera 1 is working")

  # Create hand landmarker instances
  landmarker_0 = HandLandmarker.create_from_options(options_0)
  landmarker_1 = HandLandmarker.create_from_options(options_1)

  # Frame timestamps initialization
  frame_timestamp_0 = 0
  frame_timestamp_1= 0

  while True:
    # Capture frame
    ret_0, frame_0 = capture_0.read()
    ret_1, frame_1 = capture_1.read()

    # Update timestamp
    frame_timestamp_0 += 1
    frame_timestamp_1 += 1    

    # If a frame is not read correctly, terminate program
    if not ret_0:
      print("Can't receive frame from camera 0")
      break
    if not ret_1:
      print("Can't receive frame from camera 1")
      break

    # Convert frames to MediaPipe image object    
    mp_image_0 = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame_0)
    mp_image_1 = mp.Image(image_format = mp.ImageFormat.SRGB, data = frame_1)

    # Detect hand ladmarks
    landmarker_0.detect_async(mp_image_0, frame_timestamp_0)
    landmarker_1.detect_async(mp_image_1, frame_timestamp_1)

    # If landmarks are detected, draw them into frame
    if results_0["hand_landmarks"]:
      draw_landmarks(frame_0, FRAME_WIDTH, FRAME_HEIGHT, results_0["hand_landmarks"])

    if results_1["hand_landmarks"]:
      draw_landmarks(frame_1, FRAME_WIDTH, FRAME_HEIGHT, results_1["hand_landmarks"])

    # If both landmarks are detected, triangulate position of center point
    if results_0["hand_landmarks"] and results_1["hand_landmarks"]:
      center_0_x = int(((results_0["hand_landmarks"][0].x + results_0["hand_landmarks"][9].x) / 2) * FRAME_WIDTH)
      center_0_y = int(((results_0["hand_landmarks"][0].y + results_0["hand_landmarks"][9].y) / 2) * FRAME_HEIGHT)
      center_0 = [center_0_x, center_0_y]

      center_1_x = int(((results_1["hand_landmarks"][0].x + results_1["hand_landmarks"][9].x) / 2) * FRAME_WIDTH)
      center_1_y = int(((results_1["hand_landmarks"][0].y + results_1["hand_landmarks"][9].y) / 2) * FRAME_HEIGHT)
      center_1 = [center_1_x, center_1_y]

      DLT(center_0, center_1)

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

  print("========== Exiting Hand Tracking ==========")  