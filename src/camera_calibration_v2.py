import os

import dotenv
import cv2 as cv
import numpy as np

# Load .env file
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

# Load environment variables
CAMERA_0_ID = int(os.getenv("CAMERA_0_ID"))
CAMERA_1_ID = int(os.getenv("CAMERA_1_ID"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))
CHESSBOARD_ROWS = int(os.getenv("CHESSBOARD_ROWS"))
CHESSBOARD_COLUMNS = int(os.getenv("CHESSBOARD_COLUMNS"))
CHESSBOARD_SQUARE_SIZE = float(os.getenv("CHESSBOARD_SQUARE_SIZE"))

# Captured images lists
images_0 = []
images_1 = []

def camera_calibration():
  print("========== Running Camera Calibration ==========")
  capture_frames()
  stereo_calibration()
  print("========== Exiting Camera Calibration ==========")

def capture_frames():
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

  while True:
    # Capture frame
    ret_0, frame_0 = capture_0.read()
    ret_1, frame_1 = capture_1.read()

    # If a frame is not read correctly, terminate program
    if not ret_0:
      print("Can't receive frame from camera 0")
      break
    if not ret_1:
      print("Can't receive frame from camera 1")
      break

    # Show frames
    cv.imshow("Camera 0", frame_0)
    cv.imshow("Camera 1", frame_1)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop or save frame when SPACE is pressed
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      if len(images_0 < 10):
        print("To achieve proper calibration you must take at least 10 calibration images")
      else:
        break
    elif pressed_key == 32:
      # Save frames
      images_0.append(frame_0)
      images_1.append(frame_1)

      print("Image saved")

  # Release captures and destroy windows
  capture_0.release()
  capture_1.release()
  cv.destroyAllWindows()

def stereo_calibration():
  # Termination criteria
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)   
  # Stereo calibration criteria
  stereo_criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

  # Prepare object points
  obj_point = np.zeros((CHESSBOARD_ROWS * CHESSBOARD_COLUMNS, 3), np.float32)
  obj_point[:,:2] = np.mgrid[0:CHESSBOARD_ROWS, 0:CHESSBOARD_COLUMNS].T.reshape(-1, 2)
  # Multiply obj_point by chess board square size in mm
  obj_point = obj_point * CHESSBOARD_SQUARE_SIZE

  # Arrays to store object points and image points
  obj_points = [] # 3D points in real world space
  img_points_0 = [] # 2D points in image plane from camera 0
  img_points_1 = [] # 2D points in image plane from camera 1

  # Calibrated frames counter
  calibrated_frames_counter = 0

  # Iterate through each of the captured frames
  for frame_0, frame_1 in zip(images_0, images_1):
    # Convert frame to gray scale
    gray_0 = cv.cvtColor(frame_0, cv.COLOR_BGR2GRAY)
    gray_1 = cv.cvtColor(frame_1, cv.COLOR_BGR2GRAY)

    # Find chess board corners
    ret_0, corners_0 = cv.findChessboardCorners(gray_0, (CHESSBOARD_ROWS, CHESSBOARD_COLUMNS), None)
    ret_1, corners_1 = cv.findChessboardCorners(gray_1, (CHESSBOARD_ROWS, CHESSBOARD_COLUMNS), None)

    # If found, draw chess board corners into frame
    if ret_0 == True and ret_1 == True:
      # Increment counter
      calibrated_frames_counter += 1

      # Refine chessboard corners
      corners_r_0 = cv.cornerSubPix(gray_0, corners_0, (11, 11), (-1, -1), criteria)
      corners_r_1 = cv.cornerSubPix(gray_1, corners_1, (11, 11), (-1 ,-1), criteria)

      # Add object points and image points
      obj_points.append(obj_point)
      img_points_0.append(corners_r_0)
      img_points_1.append(corners_r_1)

      # Draw and display chess board corners
      cv.drawChessboardCorners(frame_0, (CHESSBOARD_ROWS, CHESSBOARD_COLUMNS), corners_r_0, ret_0)
      cv.drawChessboardCorners(frame_1, (CHESSBOARD_ROWS, CHESSBOARD_COLUMNS), corners_r_1, ret_1)

      cv.imshow("Chess Board 0", frame_0)
      cv.imshow("Chess Board 1", frame_1)

      cv.waitKey(1000)

      # Calibrate camera 0
      ret_0, mtx_0, dist_0, rvecs_0, tvecs_0 = cv.calibrateCamera(obj_points, img_points_0, gray_0.shape[::-1], None, None)
      # Calibrate camera 1
      ret_1, mtx_1, dist_1, rvecs_1, tvecs_1 = cv.calibrateCamera(obj_points, img_points_1, gray_1.shape[::-1], None, None)
      # Stereo calibration
      ret_stereo, CM_0, dist_0_stereo, CM_1, dist_1_stereo, R, T, E, F = cv.stereoCalibrate(obj_points, img_points_0, img_points_1, mtx_0, dist_0, mtx_1, dist_1, gray_0.shape[::-1], criteria=stereo_criteria, flags=cv.CALIB_FIX_INTRINSIC)

  if calibrated_frames_counter == len(images_0):
    print("Successfull calibration")
    print("RMSE: ", ret_stereo)
  else:
    print("Bad calibration, try again")

  cv.destroyAllWindows()