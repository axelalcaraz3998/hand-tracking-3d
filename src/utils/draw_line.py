import cv2 as cv

from utils.color_switch import color_switch

def draw_line(frame: cv.typing.MatLike, point_1: cv.typing.Point, point_2: cv.typing.Point, color: str = "green", thickness: int = 2):
  cv.line(frame, point_1, point_2, color_switch(color), thickness)