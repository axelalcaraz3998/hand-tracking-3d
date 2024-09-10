import sys
sys.path.append("..")

import cv2 as cv

from utils.draw_circle import draw_circle
from utils.draw_line import draw_line

def render_landmarks(frame: cv.typing.MatLike, width: float, height: float, landmarks):
  # Render landmark connections
  draw_line(frame, (int(landmarks[0].x * width), int(landmarks[0].y * height)), (int(landmarks[1].x * width), int(landmarks[1].y * height)), "white") # 0 - 1
  draw_line(frame, (int(landmarks[1].x * width), int(landmarks[1].y * height)), (int(landmarks[2].x * width), int(landmarks[2].y * height)), "white") # 1 - 2
  draw_line(frame, (int(landmarks[2].x * width), int(landmarks[2].y * height)), (int(landmarks[3].x * width), int(landmarks[3].y * height)), "white") # 2 - 3
  draw_line(frame, (int(landmarks[3].x * width), int(landmarks[3].y * height)), (int(landmarks[4].x * width), int(landmarks[4].y * height)), "white") # 3 - 4
  draw_line(frame, (int(landmarks[0].x * width), int(landmarks[0].y * height)), (int(landmarks[5].x * width), int(landmarks[5].y * height)), "white") # 0 - 5
  draw_line(frame, (int(landmarks[5].x * width), int(landmarks[5].y * height)), (int(landmarks[6].x * width), int(landmarks[6].y * height)), "white") # 5 - 6
  draw_line(frame, (int(landmarks[6].x * width), int(landmarks[6].y * height)), (int(landmarks[7].x * width), int(landmarks[7].y * height)), "white") # 6 - 7
  draw_line(frame, (int(landmarks[7].x * width), int(landmarks[7].y * height)), (int(landmarks[8].x * width), int(landmarks[8].y * height)), "white") # 7 - 8
  draw_line(frame, (int(landmarks[5].x * width), int(landmarks[5].y * height)), (int(landmarks[9].x * width), int(landmarks[9].y * height)), "white") # 5 - 9
  draw_line(frame, (int(landmarks[9].x * width), int(landmarks[9].y * height)), (int(landmarks[10].x * width), int(landmarks[10].y * height)), "white") # 9 - 10
  draw_line(frame, (int(landmarks[10].x * width), int(landmarks[10].y * height)), (int(landmarks[11].x * width), int(landmarks[11].y * height)), "white") # 10 - 11
  draw_line(frame, (int(landmarks[11].x * width), int(landmarks[11].y * height)), (int(landmarks[12].x * width), int(landmarks[12].y * height)), "white") # 11 - 12
  draw_line(frame, (int(landmarks[9].x * width), int(landmarks[9].y * height)), (int(landmarks[13].x * width), int(landmarks[13].y * height)), "white") # 9 - 13
  draw_line(frame, (int(landmarks[13].x * width), int(landmarks[13].y * height)), (int(landmarks[14].x * width), int(landmarks[14].y * height)), "white") # 13 - 14
  draw_line(frame, (int(landmarks[14].x * width), int(landmarks[14].y * height)), (int(landmarks[15].x * width), int(landmarks[15].y * height)), "white") # 14 - 15
  draw_line(frame, (int(landmarks[15].x * width), int(landmarks[15].y * height)), (int(landmarks[16].x * width), int(landmarks[16].y * height)), "white") # 15 - 16
  draw_line(frame, (int(landmarks[13].x * width), int(landmarks[13].y * height)), (int(landmarks[17].x * width), int(landmarks[17].y * height)), "white") # 13 - 17
  draw_line(frame, (int(landmarks[17].x * width), int(landmarks[17].y * height)), (int(landmarks[18].x * width), int(landmarks[18].y * height)), "white") # 17 - 18
  draw_line(frame, (int(landmarks[18].x * width), int(landmarks[18].y * height)), (int(landmarks[19].x * width), int(landmarks[19].y * height)), "white") # 18 - 19
  draw_line(frame, (int(landmarks[19].x * width), int(landmarks[19].y * height)), (int(landmarks[20].x * width), int(landmarks[20].y * height)), "white") # 19 - 20
  draw_line(frame, (int(landmarks[17].x * width), int(landmarks[17].y * height)), (int(landmarks[0].x * width), int(landmarks[0].y * height)), "white") # 17 - 0

  # Render center of hand landmark
  palm_x = int((int(landmarks[0].x * width) + int(landmarks[9].x * width)) / 2)
  palm_y = int((int(landmarks[0].y * height) + int(landmarks[9].y * height)) / 2)
  draw_circle(frame, (palm_x, palm_y), "green", "black")  

  # Render landmarks
  for landmark in landmarks:
    # Get landmark and convert it to pixels
    landmark_x = int(landmark.x * width)
    landmark_y = int(landmark.y * height)
    draw_circle(frame, (landmark_x, landmark_y), "white", "black")