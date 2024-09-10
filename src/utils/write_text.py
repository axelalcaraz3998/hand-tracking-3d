import cv2 as cv

from utils.color_switch import color_switch

def write_text(frame: cv.typing.MatLike, text: str, point: cv.typing.Point, color: str = "green", fontScale: float = 1.0, thickness: int = 1):
  cv.putText(frame, text, point, cv.FONT_HERSHEY_COMPLEX, fontScale, color_switch(color), thickness)