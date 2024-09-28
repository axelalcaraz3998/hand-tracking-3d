import os

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
        img_name = f"{front_camera_path}/frame_{frame_count}.jpg"
        cv.imwrite(img_name, frame)
      else:
        img_name = f"{side_camera_path}/frame_{frame_count}.jpg"
        cv.imwrite(img_name, frame)

      frame_count += 1

  # Release capture and close windows
  capture.release()
  cv.destroyAllWindows()

capture_test_patterns()