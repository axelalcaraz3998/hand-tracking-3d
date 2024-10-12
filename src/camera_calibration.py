import os
import glob

import dotenv
import numpy as np
import cv2 as cv

# Get relative path to images folder
dirname = os.path.dirname(__file__)
front_camera_path = os.path.join(dirname, "images/front_camera")
side_camera_path = os.path.join(dirname, "images/side_camera")
synced_camera_path = os.path.join(dirname, "images/synced")

# Get relative path to camera parameters folder
camera_parameters_path = os.path.join(dirname, "camera_parameters")

# Load env variables
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

CAMERA_0_ID = int(os.getenv("CAMERA_0_ID"))
CAMERA_1_ID = int(os.getenv("CAMERA_1_ID"))
FRAME_WIDTH = int(os.getenv("FRAME_WIDTH"))
FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT"))
CHESSBOARD_ROWS = int(os.getenv("CHESSBOARD_ROWS"))
CHESSBOARD_COLUMNS = int(os.getenv("CHESSBOARD_COLUMNS"))
CHESSBOARD_SQUARE_SIZE = float(os.getenv("CHESSBOARD_SQUARE_SIZE"))

# Camera matrices and distortion coefficients
mtx_front = None
mtx_side = None
dist_front = None
dist_side = None

# Rotation matrix and translation vector
R = None
T = None

def capture_test_patterns(camera_type: str = "front"):
  # Capture video from webcam using OpenCV
  if camera_type.lower() == "front":
    capture = cv.VideoCapture(CAMERA_0_ID, cv.CAP_DSHOW)
  elif camera_type.lower() == "side":
    capture = cv.VideoCapture(CAMERA_1_ID, cv.CAP_DSHOW)    
  else:
    print("No such camera position")
    exit()

  # Set frame width and height
  capture.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  capture.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

  # Initialize frame count
  frame_count = 1

  # If camera is not detected, terminate program
  if not capture.isOpened():
    print("Can't open camera")
    exit()

  while True:
    # Capture frame
    ret, frame = capture.read()

    # If frame is not read correctly, exit loop
    if not ret:
      print("Can't receive frame, exiting loop")
      break

    # Show image in a window
    cv.imshow("Webcam Capture", frame)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      break
    # Save frame when the SPACE key is pressed    
    elif pressed_key == 32:
      if camera_type.lower() == "front":
        img_name = f"{front_camera_path}/capture/frame_{frame_count}.jpg"
      else:
        img_name = f"{side_camera_path}/capture/frame_{frame_count}.jpg"

      cv.imwrite(img_name, frame)
      frame_count += 1

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()

  # Calibrate camera
  if camera_type.lower() == "front":
    mtx_front, dist_front = calibrate_single_camera(camera_type)
    np.save(f"{camera_parameters_path}/mtx_front.npy", mtx_front)
    np.save(f"{camera_parameters_path}/dist_front.npy", dist_front)
  else:
    mtx_side, dist_side = calibrate_single_camera(camera_type)
    np.save(f"{camera_parameters_path}/mtx_side.npy", mtx_side)
    np.save(f"{camera_parameters_path}/dist_side.npy", dist_side)

def calibrate_single_camera(camera_type: str = "front"):
  # Termination criteria
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  rows = CHESSBOARD_ROWS # Number of checkboard row corners
  columns = CHESSBOARD_COLUMNS # Number of checkboard row corners
  world_scaling = CHESSBOARD_SQUARE_SIZE # Real world square size

  # Prepare object points
  obj_point = np.zeros((rows * columns, 3), np.float32)
  obj_point[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
  obj_point = world_scaling * obj_point

  # Arrays to store object points and image points
  obj_points = [] # 3D points in real world space
  img_points = [] # 2D points in image plane

  # Load images
  if camera_type.lower() == "front":
    images_path = f"{front_camera_path}/capture/*.jpg"
  else:
    images_path = f"{side_camera_path}/capture/*.jpg"

  images = sorted(glob.glob(images_path))

  # Initialize image count
  img_count = 1

  # Iterate through each image
  for file_name in images:
    # Ignore example image
    if file_name == "example.jpg":
      continue

    # Read image and convert it to gray scale
    img = cv.imread(file_name)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # Find chessboard corners
    ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

    # If found, append object point and image point
    if ret == True:
      # Refine checkboard coordinates
      corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

      obj_points.append(obj_point)
      img_points.append(corners2)

      # Draw and display corners
      cv.drawChessboardCorners(img, (rows, columns), corners, ret)
      cv.imshow("Checkboard Pattern", img)

      # Write pattern image
      if camera_type == "front":
        img_name = f"{front_camera_path}/calibration/frame_{img_count}.jpg"
      else:
        img_name = f"{side_camera_path}/calibration/frame_{img_count}.jpg"

      cv.imwrite(img_name, img)
      img_count += 1

      cv.waitKey(500)

  cv.destroyAllWindows()

  # Find calibration parameters
  ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, (int(FRAME_WIDTH), int(FRAME_HEIGHT)), None, None)
  print("RMSE: ", ret)
  print("Camera matrix:\n", mtx)
  print("Distortion coefficients: ", dist)
  print("Rs:\n", rvecs)
  print("Ts:\n", tvecs)
  
  return mtx, dist

def capture_synced_test_patterns():
  # Capture video from webcams using OpenCV
  front_cam = cv.VideoCapture(CAMERA_0_ID, cv.CAP_DSHOW)
  side_cam = cv.VideoCapture(CAMERA_1_ID, cv.CAP_DSHOW)

  # Set frames resolution
  front_cam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  front_cam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
  side_cam.set(cv.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
  side_cam.set(cv.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

  # Initialize image_count
  front_cam_count = 1
  side_cam_count = 2

  # If either of the cameras is not detected, terminate program
  if not front_cam.isOpened() or not side_cam.isOpened():
    print("Can't open either of the two cameras")
    exit()

  while True:
    # Capture frame
    ret_front, frame_front = front_cam.read()
    ret_side, frame_side = side_cam.read()

    # If either frame is not read correctly, exit loop
    if not ret_front or not ret_side:
      print("Can't receive frame, exiting loop")
      break

    # Show image in a window
    cv.imshow("Front Webcam Capture", frame_front)
    cv.imshow("Side Webcam Capture", frame_side)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      break
    # Save frame when the SPACE key is pressed
    elif pressed_key == 32:
      front_cam_img_name = f"{synced_camera_path}/capture/frame_{front_cam_count}.jpg"
      side_cam_img_name = f"{synced_camera_path}/capture/frame_{side_cam_count}.jpg"

      cv.imwrite(front_cam_img_name, frame_front)
      cv.imwrite(side_cam_img_name, frame_side)

      front_cam_count += 2
      side_cam_count += 2

  # Release capture and close windows
  front_cam.release()
  side_cam.release()
  cv.destroyAllWindows()

  # Calibrate cameras
  R, T = calibrate_synced_cameras()
  np.save(f"{camera_parameters_path}/R.npy", R)
  np.save(f"{camera_parameters_path}/T.npy", T)  

  # Obtain projection matrices
  find_projection_matrices()

def calibrate_synced_cameras():
  # Termination criteria
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.001)

  rows = CHESSBOARD_ROWS # Number of checkboard row corners
  columns = CHESSBOARD_COLUMNS # Number of checkboard row corners
  world_scaling = CHESSBOARD_SQUARE_SIZE # Real world square size (Or not)

  # Prepare object points
  obj_point = np.zeros((rows * columns, 3), np.float32)
  obj_point[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
  obj_point = world_scaling * obj_point

  # Arrays to store object points and image points
  obj_points = [] # 3D points in real world space
  img_points_front_cam = [] # 2D points in image plane
  img_points_side_cam = [] # 2D points in image plane

  # Load images
  images_path = f"{synced_camera_path}/capture/*.jpg"
  images = sorted(glob.glob(images_path))

  # Initialize image count
  img_count = 1

  # Images list
  front_cam_images = []
  side_cam_images = []

  # Iterate through each image in directory
  for file_name in images:
    # Ignore example image
    if file_name == "example.jpg":
      continue

    # Add images to its respective list
    img = cv.imread(file_name, 1)
    if img_count % 2 != 0:
      front_cam_images.append(img)
    else:
      side_cam_images.append(img)

    img_count += 1

  # Initialize camera image count
  front_cam_count = 1
  side_cam_count = 2

  # Iterate through each list
  for frame_front, frame_side in zip(front_cam_images, side_cam_images):
    # Read image and convert it to gray scale
    gray_front = cv.cvtColor(frame_front, cv.COLOR_BGR2GRAY)
    gray_side = cv.cvtColor(frame_side, cv.COLOR_BGR2GRAY)

    # Find chess board corners
    ret_front, corners_front = cv.findChessboardCorners(gray_front, (rows, columns), None)
    ret_side, corners_side = cv.findChessboardCorners(gray_side, (rows, columns), None)

    # If found, append object point and image point
    if ret_front == True and ret_side == True:
      # Refine checkboard coordinates
      cornersFront = cv.cornerSubPix(gray_front, corners_front, (11, 11), (-1, -1), criteria)
      cornersSide = cv.cornerSubPix(gray_side, corners_side, (11, 11), (-1, -1), criteria)

      obj_points.append(obj_point)
      img_points_front_cam.append(cornersFront)
      img_points_side_cam.append(cornersSide)

      # Draw and display corners
      cv.drawChessboardCorners(frame_front, (rows, columns), cornersFront, ret_front)
      cv.imshow("Front Webcam Checkboard Pattern", frame_front)
    
      cv.drawChessboardCorners(frame_side, (rows, columns), cornersSide, ret_side)
      cv.imshow("Side Webcam Checkboard Pattern", frame_side)

      # Write pattern image
      front_cam_img_name = f"{synced_camera_path}/calibration/frame_{front_cam_count}.jpg"
      cv.imwrite(front_cam_img_name, frame_front)
      side_cam_img_name = f"{synced_camera_path}/calibration/frame_{side_cam_count}.jpg"
      cv.imwrite(side_cam_img_name, frame_side)

      front_cam_count += 2
      side_cam_count += 2

      cv.waitKey(500)

  cv.destroyAllWindows()

  # Find stereo calibration parameters
  ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(obj_points, img_points_front_cam, img_points_side_cam, mtx_front, dist_front, mtx_side, dist_side, (int(FRAME_WIDTH), int(FRAME_HEIGHT)), criteria, cv.CALIB_FIX_INTRINSIC)
  print("RMSE: ", ret)
  print("Camera matrix 1:\n", CM1)
  print("Distortion coefficients 1: ", dist1)
  print("Camera matrix 2:\n", CM2)
  print("Distortion coefficients 2: ", dist2)
  print("Rotation matrix: ", R)
  print("Translation vector: ", T)
  print("Essential matrix: ", E)
  print("Fundamental matrix: ", F)

  return R, T

def find_projection_matrices():
  # RT matrix for Camera 1
  RT1 = np.concatenate([np.eye(3), [[0], [0], [0]]], axis = -1)
  # Projection matrix for camera 1
  P1 = mtx_front @ RT1

  # RT matrix for Camera 2
  RT2 = np.concatenate([R, T], axis = -1)
  # Projection matrix for camera 2
  P2 = mtx_side @ RT2

  np.save(f"{camera_parameters_path}/P1.npy", P1)  
  np.save(f"{camera_parameters_path}/P2.npy", P2)  

  print("P1:\n", P1)
  print("P2:\n", P2)

# capture_test_patterns("front")
# capture_test_patterns("side")
# capture_synced_test_patterns()

mtx_front, dist_front = calibrate_single_camera("front")
mtx_side, dist_side = calibrate_single_camera("side")
R, T = calibrate_synced_cameras()
find_projection_matrices()