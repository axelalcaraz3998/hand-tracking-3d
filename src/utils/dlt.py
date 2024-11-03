import os

import numpy as np
import scipy.linalg

def DLT(point_0, point_1):
  # Load camera parameters
  dirname = os.path.dirname(__file__)
  camera_parameters_path = os.path.join(dirname, "../camera_parameters")

  if not os.path.exists(camera_parameters_path):
    print("Could not find camera parameters, make sure to calibrate the camera first")
    return

  P_0 = np.load(f"{camera_parameters_path}/P_0.npy")
  P_1 = np.load(f"{camera_parameters_path}/P_1.npy")

  A = [point_0[1] * P_0[2, :] - P_0[1, :],
        P_0[0, :] - point_0[0] * P_0[2, :],
        point_1[1] * P_1[2, :] - P_1[1, :],
        P_1[0, :] - point_1[0] * P_1[2, :]
      ]
  
  A = np.array(A).reshape((4,4))
  B = A.transpose() @ A

  U, s, Vh = scipy.linalg.svd(B, full_matrices = False)

  print(Vh[3, 0:3] / Vh[3, 3])