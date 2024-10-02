import os
import glob

import numpy as np
import cv2 as cv

# Get relative path to images folder
dirname = os.path.dirname(__file__)
front_camera_path = os.path.join(dirname, "images/front_camera")
side_camera_path = os.path.join(dirname, "images/side_camera")
synced_camera_path = os.path.join(dirname, "images/synced")

# Camera matrices and distortion coefficients
mtx_0 = None
mtx_1 = None
dist_0 = None
dist_1 = None
rotation_matrix = None
translation_vector = None

def capture_test_patterns(camera_id: int = 0, camera_type: str = "front"):
  # Capture video from webcam using OpenCV
  capture = cv.VideoCapture(camera_id, cv.CAP_DSHOW)
  capture.set(cv.CAP_PROP_FRAME_WIDTH, 640)
  capture.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

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
      if camera_type == "front":
        img_name = f"{front_camera_path}/capture/frame_{frame_count}.jpg"
      else:
        img_name = f"{side_camera_path}/capture/frame_{frame_count}.jpg"

      cv.imwrite(img_name, frame)
      frame_count += 1

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()

  # Calibrate camera
  if camera_type == "front":
    mtx_0, dist_0 = calibrate_single_camera(camera_type)
  else:
    mtx_1, dist_1 = calibrate_single_camera(camera_type)

def calibrate_single_camera(camera_type: str = "front"):
  # Termination criteria
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

  rows = 4 # Number of checkboard row corners
  columns = 7 # Number of checkboard row corners
  world_scaling = 1 # Real world square size (Or not)

  # Prepare object points
  obj_point = np.zeros((rows * columns, 3), np.float32)
  obj_point[:,:2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
  obj_point = world_scaling * obj_point

  # Arrays to store object points and image points
  obj_points = [] # 3D points in real world space
  img_points = [] # 2D points in image plane

  # Load images
  if camera_type == "front":
    images_path = f"{front_camera_path}/capture/*.jpg"
    images = sorted(glob.glob(images_path))
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

    # Find chess board corners
    ret, corners = cv.findChessboardCorners(gray, (rows, columns), None)

    # If found, append object point and image point
    if ret == True:
      obj_points.append(obj_point)
      
      # Refine checkboard coordinates
      corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
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
  ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)
  # print("RMSE: ", ret)
  # print("Camera matrix:\n", mtx)
  # print("Distortion coefficients: ", dist)
  # print("Rs:\n", rvecs)
  # print("Ts:\n", tvecs)
  
  return mtx, dist

def capture_synced_test_patterns():
  # Capture video from webcams using OpenCV
  cam_0 = cv.VideoCapture(0, cv.CAP_DSHOW)
  cam_1 = cv.VideoCapture(1, cv.CAP_DSHOW)

  cam_0.set(cv.CAP_PROP_FRAME_WIDTH, 640)
  cam_0.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
  cam_1.set(cv.CAP_PROP_FRAME_WIDTH, 640)
  cam_1.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

  # Initialize image_count
  cam_0_count = 1
  cam_1_count = 2

  # If either of the cameras is not detected, terminate program
  if not cam_0.isOpened() or not cam_1.isOpened():
    print("Can't open either of the two cameras")
    exit()

  while True:
    # Capture frame
    ret_0, frame_0 = cam_0.read()
    ret_1, frame_1 = cam_1.read()

    # If either frame is not read correctly, exit loop
    if not ret_0 or not ret_1:
      print("Can't receive frame, exiting loop")
      break

    # Show image in a window
    cv.imshow("Webcam 0 Capture", frame_0)
    cv.imshow("Webcam 1 Capture", frame_1)

    # Get pressed key
    pressed_key = cv.waitKey(1) & 0xFF

    # Condition to exit loop
    if pressed_key == ord('q') or pressed_key == ord('Q'):
      break
    # Save frame when the SPACE key is pressed
    elif pressed_key == 32:
      cam_0_img_name = f"{synced_camera_path}/capture/frame_{cam_0_count}.jpg"
      cam_1_img_name = f"{synced_camera_path}/capture/frame_{cam_1_count}.jpg"
      cv.imwrite(cam_0_img_name, frame_0)
      cv.imwrite(cam_1_img_name, frame_1)
      cam_0_count += 2
      cam_1_count += 2

  # Release capture and close windows
  cam_0.release()
  cam_1.release()
  cv.destroyAllWindows()

  # Calibrate cameras
  rotation_matrix, translation_vector = calibrate_synced_cameras()

def calibrate_synced_cameras():
  # Termination criteria
  criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 100, 0.0001)

  rows = 4 # Number of checkboard row corners
  columns = 7 # Number of checkboard row corners
  world_scaling = 1 # Real world square size (Or not)

  # Prepare object points
  obj_point = np.zeros((rows * columns, 3), np.float32)
  obj_point[:, :2] = np.mgrid[0:rows, 0:columns].T.reshape(-1, 2)
  obj_point = world_scaling * obj_point

  # Arrays to store object points and image points
  obj_points = [] # 3D points in real world space
  img_points_cam_0 = [] # 2D points in image plane
  img_points_cam_1 = [] # 2D points in image plane

  # Load images
  images_path = f"{synced_camera_path}/capture/*.jpg"
  images = sorted(glob.glob(images_path))

  # Initialize image count
  img_count = 1

  # Images list
  cam_0_images = []
  cam_1_images = []

  # Iterate through each image in directory
  for file_name in images:
    # Ignore example image
    if file_name == "example.jpg":
      continue

    # Add images to its respective list
    img = cv.imread(file_name, 1)
    if img_count % 2 != 0:
      cam_0_images.append(img)
    else:
      cam_1_images.append(img)

    img_count += 1

  # Initialize camera image count
  cam_0_count = 1
  cam_1_count = 2

  # Iterate through each list
  for cam_0_img, cam_1_img in zip(cam_0_images, cam_1_images):
    # Read image and convert it to gray scale
    gray_0 = cv.cvtColor(cam_0_img, cv.COLOR_BGR2GRAY)
    gray_1 = cv.cvtColor(cam_1_img, cv.COLOR_BGR2GRAY)

    # Find chess board corners
    ret_0, corners_0 = cv.findChessboardCorners(gray_0, (rows, columns), None)
    ret_1, corners_1 = cv.findChessboardCorners(gray_1, (rows, columns), None)

    # If found, append object point and image point
    if ret_0 == True and ret_1 == True:
      obj_points.append(obj_point)
      
      # Refine checkboard coordinates
      corners0 = cv.cornerSubPix(gray_0, corners_0, (11, 11), (-1, -1), criteria)
      corners1 = cv.cornerSubPix(gray_1, corners_1, (11, 11), (-1, -1), criteria)
      img_points_cam_0.append(corners0)
      img_points_cam_1.append(corners1)

      # Draw and display corners
      cv.drawChessboardCorners(cam_0_img, (rows, columns), corners0, ret_0)
      cv.imshow("Checkboard Pattern Cam 0", cam_0_img)
    
      cv.drawChessboardCorners(cam_1_img, (rows, columns), corners1, ret_1)
      cv.imshow("Checkboard Pattern Cam 1", cam_1_img)

      # Write pattern image
      cam_0_img_name = f"{synced_camera_path}/calibration/frame_{cam_0_count}.jpg"
      cv.imwrite(cam_0_img_name, cam_0_img)
      cam_1_img_name = f"{synced_camera_path}/calibration/frame_{cam_1_count}.jpg"
      cv.imwrite(cam_1_img_name, cam_1_img)

      cam_0_count += 2
      cam_1_count += 2

      cv.waitKey(500)
    else:
      print("No image found")

  cv.destroyAllWindows()

  # Find stereo calibration parameters
  ret, CM1, dist1, CM2, dist2, R, T, E, F = cv.stereoCalibrate(obj_points, img_points_cam_0, img_points_cam_1, mtx_0, dist_0, mtx_1, dist_1, (640, 480), criteria = criteria, flags = cv.CALIB_FIX_INTRINSIC)
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

mtx_0, dist_0 = calibrate_single_camera("front")
mtx_1, dist_1 = calibrate_single_camera("side")

rotation_matrix, translation_vector = calibrate_synced_cameras()

# RT matrix for Camera 1
RT1 = np.concatenate([np.eye(3), [[0], [0], [0]]], axis = -1)
# Projection matrix for camera 1
P1 = mtx_0 @ RT1

# RT matrix for Camera 2
RT2 = np.concatenate([rotation_matrix, translation_vector], axis = -1)
# Projection matrix for camera 2
P2 = mtx_1 @ RT2

print("P1: ", P1)
print("P2: ", P2)