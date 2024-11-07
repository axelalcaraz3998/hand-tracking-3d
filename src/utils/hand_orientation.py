import numpy as np

def hand_orientation(point_0, point_1):
  orientation_deg = np.rad2deg(np.atan2(point_1[1] - point_0[1], point_1[0] - point_0[0]))
  # print(orientation_deg)