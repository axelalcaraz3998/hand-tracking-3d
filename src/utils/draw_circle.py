import cv2 as cv

from utils.color_switch import color_switch

def draw_circle(frame: cv.typing.MatLike, point: cv.typing.Point, fill: str = "green", border: str = "red", radius: int = 4, thickness: int = -1):
  cv.circle(frame, point, (radius + 2), color_switch(border), thickness)
  cv.circle(frame, point, radius, color_switch(fill), thickness)