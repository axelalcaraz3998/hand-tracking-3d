import os

import numpy as np
import scipy.linalg

dirname = os.path.dirname(__file__)
camera_parameters_path = os.path.join(dirname, "../camera_parameters")

P1 = np.load(f"{camera_parameters_path}/P1.npy")
P2 = np.load(f"{camera_parameters_path}/P2.npy")

def DLT(point_1, point_2):
  A = [point_1[1] * P1[2, :] - P1[1, :],
  P1[0, :] - point_1[0] * P1[2, :],
  point_2[1] * P2[2, :] - P2[1, :],
  P2[0, :] - point_2[0] * P2[2, :]]

  A = np.array(A).reshape((4,4))
  B = A.transpose() @ A

  U, s, Vh = scipy.linalg.svd(B, full_matrices = False)

  return Vh[3, 0:3] / Vh[3, 3]