import cv2 as cv

from color_switch import color_switch

def write_text(frame: cv.typing.MatLike, text: str, point: cv.typing.Point, fontScale: float = 1.0, color: str = "green", thickness: int = 1):
  cv.putText(frame, text, point, cv.FONT_HERSHEY_COMPLEX, fontScale, color_switch(color), thickness)