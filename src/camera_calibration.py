import os
import glob

import numpy as np
import cv2 as cv

# Get relative path to images folder
dirname = os.path.dirname(__file__)
front_camera_path = os.path.join(dirname, "images/front_camera")
side_camera_path = os.path.join(dirname, "images/side_camera")

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

  # Find checkboard pattern
  find_checkboard_pattern(camera_type)

def find_checkboard_pattern(camera_type: str = "front"):
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
        img_name = f"{front_camera_path}/patterns/frame_{img_count}.jpg"
      else:
        img_name = f"{side_camera_path}/patterns/frame_{img_count}.jpg"

      cv.imwrite(img_name, img)
      img_count += 1

      cv.waitKey(500)

  cv.destroyAllWindows()