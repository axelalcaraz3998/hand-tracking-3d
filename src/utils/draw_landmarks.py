import cv2 as cv

def draw_landmarks(frame: cv.typing.MatLike, frame_width: int, frame_height: int, landmarks):
  # Draw landmark connections
  cv.line(frame, (int(landmarks[0].x * frame_width), int(landmarks[0].y * frame_height)), (int(landmarks[1].x * frame_width), int(landmarks[1].y * frame_height)), (0, 0, 0), 2) # 0 - 1
  cv.line(frame, (int(landmarks[1].x * frame_width), int(landmarks[1].y * frame_height)), (int(landmarks[2].x * frame_width), int(landmarks[2].y * frame_height)), (0, 0, 0), 2) # 1 - 2
  cv.line(frame, (int(landmarks[2].x * frame_width), int(landmarks[2].y * frame_height)), (int(landmarks[3].x * frame_width), int(landmarks[3].y * frame_height)), (0, 0, 0), 2) # 2 - 3
  cv.line(frame, (int(landmarks[3].x * frame_width), int(landmarks[3].y * frame_height)), (int(landmarks[4].x * frame_width), int(landmarks[4].y * frame_height)), (0, 0, 0), 2) # 3 - 4
  cv.line(frame, (int(landmarks[0].x * frame_width), int(landmarks[0].y * frame_height)), (int(landmarks[5].x * frame_width), int(landmarks[5].y * frame_height)), (0, 0, 0), 2) # 0 - 5
  cv.line(frame, (int(landmarks[5].x * frame_width), int(landmarks[5].y * frame_height)), (int(landmarks[6].x * frame_width), int(landmarks[6].y * frame_height)), (0, 0, 0), 2) # 5 - 6
  cv.line(frame, (int(landmarks[6].x * frame_width), int(landmarks[6].y * frame_height)), (int(landmarks[7].x * frame_width), int(landmarks[7].y * frame_height)), (0, 0, 0), 2) # 6 - 7
  cv.line(frame, (int(landmarks[7].x * frame_width), int(landmarks[7].y * frame_height)), (int(landmarks[8].x * frame_width), int(landmarks[8].y * frame_height)), (0, 0, 0), 2) # 7 - 8
  cv.line(frame, (int(landmarks[5].x * frame_width), int(landmarks[5].y * frame_height)), (int(landmarks[9].x * frame_width), int(landmarks[9].y * frame_height)), (0, 0, 0), 2) # 5 - 9
  cv.line(frame, (int(landmarks[9].x * frame_width), int(landmarks[9].y * frame_height)), (int(landmarks[10].x * frame_width), int(landmarks[10].y * frame_height)), (0, 0, 0), 2) # 9 - 10
  cv.line(frame, (int(landmarks[10].x * frame_width), int(landmarks[10].y * frame_height)), (int(landmarks[11].x * frame_width), int(landmarks[11].y * frame_height)), (0, 0, 0), 2) # 10 - 11
  cv.line(frame, (int(landmarks[11].x * frame_width), int(landmarks[11].y * frame_height)), (int(landmarks[12].x * frame_width), int(landmarks[12].y * frame_height)), (0, 0, 0), 2) # 11 - 12
  cv.line(frame, (int(landmarks[9].x * frame_width), int(landmarks[9].y * frame_height)), (int(landmarks[13].x * frame_width), int(landmarks[13].y * frame_height)), (0, 0, 0), 2) # 9 - 13
  cv.line(frame, (int(landmarks[13].x * frame_width), int(landmarks[13].y * frame_height)), (int(landmarks[14].x * frame_width), int(landmarks[14].y * frame_height)), (0, 0, 0), 2) # 13 - 14
  cv.line(frame, (int(landmarks[14].x * frame_width), int(landmarks[14].y * frame_height)), (int(landmarks[15].x * frame_width), int(landmarks[15].y * frame_height)), (0, 0, 0), 2) # 14 - 15
  cv.line(frame, (int(landmarks[15].x * frame_width), int(landmarks[15].y * frame_height)), (int(landmarks[16].x * frame_width), int(landmarks[16].y * frame_height)), (0, 0, 0), 2) # 15 - 16
  cv.line(frame, (int(landmarks[13].x * frame_width), int(landmarks[13].y * frame_height)), (int(landmarks[17].x * frame_width), int(landmarks[17].y * frame_height)), (0, 0, 0), 2) # 13 - 17
  cv.line(frame, (int(landmarks[17].x * frame_width), int(landmarks[17].y * frame_height)), (int(landmarks[18].x * frame_width), int(landmarks[18].y * frame_height)), (0, 0, 0), 2) # 17 - 18
  cv.line(frame, (int(landmarks[18].x * frame_width), int(landmarks[18].y * frame_height)), (int(landmarks[19].x * frame_width), int(landmarks[19].y * frame_height)), (0, 0, 0), 2) # 18 - 19
  cv.line(frame, (int(landmarks[19].x * frame_width), int(landmarks[19].y * frame_height)), (int(landmarks[20].x * frame_width), int(landmarks[20].y * frame_height)), (0, 0, 0), 2) # 19 - 20
  cv.line(frame, (int(landmarks[17].x * frame_width), int(landmarks[17].y * frame_height)), (int(landmarks[0].x * frame_width), int(landmarks[0].y * frame_height)), (0, 0, 0), 2) # 17 - 0

  # Draw center of hand
  center_x = int(((landmarks[0].x + landmarks[9].x) / 2) * frame_width)
  center_y = int(((landmarks[0].y + landmarks[9].y) / 2) * frame_height)
  cv.circle(frame, (center_x, center_y), 6, (255, 255, 255), -1)
  cv.circle(frame, (center_x, center_y), 4, (0, 0, 0), -1)

  # Draw landmark points
  for landmark in landmarks:
    cv.circle(frame, (int(landmark.x * frame_width), int(landmark.y * frame_height)), 6, (255, 255, 255), -1)
    cv.circle(frame, (int(landmark.x * frame_width), int(landmark.y * frame_height)), 4, (0, 0, 0), -1)