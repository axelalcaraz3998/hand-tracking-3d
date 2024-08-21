import numpy as np
import cv2 as cv

from src.utils.color_switch import color_switch

def draw_circle(frame: cv.typing.MatLike, point: cv.typing.Point, radius: int = -1, fill: str = "green", border: str = "red", thickness: int = 2):
  cv.circle(frame, point, radius, color_switch(border), (thickness + 2))
  cv.circle(frame, point, radius, color_switch(fill), thickness)