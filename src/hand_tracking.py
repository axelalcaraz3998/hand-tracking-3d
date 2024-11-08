import os

import dotenv
import cv2 as cv
import mediapipe as mp

def hand_tracking():
  # Import utility functions
  from utils.draw_landmarks import draw_landmarks
  from utils.write_gesture import write_gesture
  from utils.hand_orientation import hand_orientation
  from utils.inverse_kinematics import inverse_kinematics
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
  model_path = os.path.join(dirname, "./models/gesture_recognizer.task")

  # MediaPipe hand landmarker objects
  BaseOptions = mp.tasks.BaseOptions
  GestureRecognizer = mp.tasks.vision.GestureRecognizer
  GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
  GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
  VisionRunningMode = mp.tasks.vision.RunningMode

  # Results dictionaries
  results_0 = {
    "hand_landmarks": None,
    "gesture": None,
  }

  results_1 = {
    "hand_landmarks": None,
    "gesture": None
  }

  # Callback functions
  def result_callback_0(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    # If a hand is detected assing hand landmarker result to results dictionary
    if len(result.hand_landmarks) > 0 and len(result.gestures) > 0:
      results_0["hand_landmarks"] = result.hand_landmarks[0]
      results_0["gesture"] = result.gestures[0]
    else:
      results_0["hand_landmarks"] = None
      results_0["gesture"] = None

  def result_callback_1(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    # If a hand is detected assing hand landmarker result to results dictionary
    if len(result.hand_landmarks) > 0 and len(result.gestures) > 0:
      results_1["hand_landmarks"] = result.hand_landmarks[0]
      results_1["gesture"] = result.gestures[0]
    else:
      results_1["hand_landmarks"] = None
      results_1["gesture"] = None

  # Hand landmarker options
  options_0 = GestureRecognizerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
    min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
    min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
    result_callback = result_callback_0
  )

  options_1 = GestureRecognizerOptions(
    base_options = BaseOptions(model_asset_path = model_path),
    running_mode = VisionRunningMode.LIVE_STREAM,
    num_hands = 1,
    min_hand_detection_confidence = MIN_HAND_DETECTION_CONFIDENCE,
    min_hand_presence_confidence = MIN_HAND_PRESENCE_CONFIDENCE,
    min_tracking_confidence = MIN_TRACKING_CONFIDENCE,
    result_callback = result_callback_1
  )

  print("========== Running Hand Tracking ==========")
  
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
  landmarker_0 = GestureRecognizer.create_from_options(options_0)
  landmarker_1 = GestureRecognizer.create_from_options(options_1)

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
    landmarker_0.recognize_async(mp_image_0, frame_timestamp_0)
    landmarker_1.recognize_async(mp_image_1, frame_timestamp_1)

    # If landmarks are detected, draw them into frame
    if results_0["hand_landmarks"] and results_0["gesture"]:
      draw_landmarks(frame_0, FRAME_WIDTH, FRAME_HEIGHT, results_0["hand_landmarks"])
      write_gesture(frame_0, results_0["gesture"])

    if results_1["hand_landmarks"] and results_1["gesture"]:
      draw_landmarks(frame_1, FRAME_WIDTH, FRAME_HEIGHT, results_1["hand_landmarks"])
      write_gesture(frame_1, results_1["gesture"])

    # If both landmarks are detected, triangulate position of center point
    if results_0["hand_landmarks"] and results_1["hand_landmarks"]:
      center_0_x = int(((results_0["hand_landmarks"][0].x + results_0["hand_landmarks"][9].x) / 2) * FRAME_WIDTH)
      center_0_y = int(((results_0["hand_landmarks"][0].y + results_0["hand_landmarks"][9].y) / 2) * FRAME_HEIGHT)
      center_0 = [center_0_x, center_0_y]

      center_1_x = int(((results_1["hand_landmarks"][0].x + results_1["hand_landmarks"][9].x) / 2) * FRAME_WIDTH)
      center_1_y = int(((results_1["hand_landmarks"][0].y + results_1["hand_landmarks"][9].y) / 2) * FRAME_HEIGHT)
      center_1 = [center_1_x, center_1_y]

      # Get rotation of hand in Z coordinate
      point_0 = [int(results_0["hand_landmarks"][0].x * FRAME_WIDTH), int(results_0["hand_landmarks"][0].y * FRAME_HEIGHT)]
      point_9 = [int(results_0["hand_landmarks"][9].x * FRAME_WIDTH), int(results_0["hand_landmarks"][9].y * FRAME_HEIGHT)]
      z_rotation = hand_orientation(point_0, point_9)

      # Get rotation of hand in Y coordinate
      point_5_0 = [int(results_0["hand_landmarks"][5].x * FRAME_WIDTH), int(results_0["hand_landmarks"][5].y * FRAME_HEIGHT)]
      point_5_1 = [int(results_1["hand_landmarks"][5].x * FRAME_WIDTH), int(results_1["hand_landmarks"][5].y * FRAME_HEIGHT)]

      point_17_0 = [int(results_0["hand_landmarks"][17].x * FRAME_WIDTH), int(results_0["hand_landmarks"][17].y * FRAME_HEIGHT)]
      point_17_1 = [int(results_1["hand_landmarks"][17].x * FRAME_WIDTH), int(results_1["hand_landmarks"][17].y * FRAME_HEIGHT)]

      point_5_coords = DLT(point_5_0, point_5_1)
      point_17_coords = DLT(point_17_0, point_17_1)
      y_rotation = hand_orientation([point_5_coords[2], point_5_coords[0]], [point_17_coords[2], point_17_coords[0]]) # atan2(Z, X)

      # Get rotation of hand in X coordinate
      point_0_0 = [int(results_0["hand_landmarks"][0].x * FRAME_WIDTH), int(results_0["hand_landmarks"][0].y * FRAME_HEIGHT)]
      point_0_1 = [int(results_1["hand_landmarks"][0].x * FRAME_WIDTH), int(results_1["hand_landmarks"][0].y * FRAME_HEIGHT)]

      point_9_0 = [int(results_0["hand_landmarks"][9].x * FRAME_WIDTH), int(results_0["hand_landmarks"][9].y * FRAME_HEIGHT)]
      point_9_1 = [int(results_1["hand_landmarks"][9].x * FRAME_WIDTH), int(results_1["hand_landmarks"][9].y * FRAME_HEIGHT)]
      
      point_0_coords = DLT(point_0_0, point_0_1)
      point_9_coords = DLT(point_9_0, point_9_1) 
      x_rotation = hand_orientation([point_0_coords[2], point_0_coords[1]], [point_9_coords[2], point_9_coords[1]]) # atan2(Z, Y)

      # Inverse kinematics
      hand_coords = DLT(center_0, center_1)
      inverse_kinematics(hand_coords, [x_rotation, y_rotation, z_rotation])

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