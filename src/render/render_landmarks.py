import sys
import cv2 as cv

module_path = sys.path.append("../utils/draw_circle.py")

from sys.path.append("../utils/draw_circle.py") import draw_circle

def render_landmarks(frame: cv.typing.MatLike, width: float, height: float, landmarks):
  # Render circles
  for landmark in landmarks:
    landmark_x = int(landmark.x * width)
    landmark_y = int(landmark.y * height)
    draw_circle(frame, landmark_x, landmark_y, "white", "black")