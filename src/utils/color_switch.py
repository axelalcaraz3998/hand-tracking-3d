import cv2 as cv

def color_switch(color: str) -> cv.typing.Scalar:
  if color.lower() == "red":
    return (0, 0, 255)
  elif color.lower() == "green":
    return (0, 255, 0)
  elif color.lower() == "blue":
    return (255, 0, 0)
  elif color.lower() == "white":
    return (255, 255, 255)
  elif color.lower() == "black":
    return (0, 0, 0)
  elif color.lower() == "yellow":
    return (0, 255, 255)
  elif color.lower() == "magenta":
    return (255, 0, 255)
  elif color.lower() == "cyan":
    return (255, 255, 0)
  else:
    return (0, 255, 0) # Default color is green