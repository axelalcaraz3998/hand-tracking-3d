import cv2 as cv

def color_switch(color: str) -> cv.typing.Scalar:
  if str.lower() == "red":
    return (0, 0, 255)
  elif str.lower() == "green":
    return (0, 255, 0)
  elif str.lower() == "blue":
    return (255, 0, 0)
  elif str.lower() == "white":
    return (255, 255, 255)
  elif str.lower() == "black":
    return (0, 0, 0)
  elif str.lower() == "yellow":
    return (0, 255, 255)
  elif str.lower() == "magenta":
    return (255, 0, 255)
  elif str.lower() == "cyan":
    return (255, 255, 0)
  else:
    return (0, 255, 0) # Default color is green