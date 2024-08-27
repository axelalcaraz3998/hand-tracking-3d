import cv2 as cv

from color_switch import color_switch

def draw_rectangle(frame: cv.typing.MatLike, point_1: cv.typing.MatLike, point_2: cv.typing.Point, color: str = "green", thickness: int = 2):
  cv.rectangle(frame, point_1, point_2, color_switch(color), thickness)