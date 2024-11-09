import cv2 as cv

def write_gesture(frame: cv.typing.MatLike, gesture):
  if not gesture == None: # Program sometimes crashes when receiving null value
    cv.putText(frame, gesture[0].category_name, (0, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)