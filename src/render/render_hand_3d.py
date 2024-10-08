import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_hand(keypoints_3d, figure):
  # Rotation matrices
  Rz = np.array(([[0., -1., 0.],
                  [1.,  0., 0.],
                  [0.,  0., 1.]]))

  Rx = np.array(([[1.,  0.,  0.],
                  [0., -1.,  0.],
                  [0.,  0., -1.]]))
  
  # Rotate frames
  keypoints_3d_rotated = []
  for frame in keypoints_3d:
    frame_keypoints_rotated = []

    for keypoint in frame:
      keypoint_rotated = Rz @ Rx @ keypoint
      frame_keypoints_rotated.append(keypoint_rotated)
    
    keypoints_3d_rotated.append(frame_keypoints_rotated)

  # Convert rotated frames to numpy array
  keypoints_3d_rotated = np.array(keypoints_3d_rotated)

  # Define fingers
  thumb = [[0, 1], [1, 2], [2, 3], [3, 4]]
  index = [[0, 5], [5, 6], [6, 7], [7, 8]]
  middle = [[0, 9], [9, 10], [10, 11], [11, 12]]
  ring = [[0, 13], [13, 14], [14, 15], [15, 16]]
  pinkie = [[0, 17], [17, 18], [18, 19], [19, 20]]
  fingers = [pinkie, ring, middle, index, thumb]

  for i, keypoints_3d in enumerate(keypoints_3d_rotated):
    # Skip every second frame
    if i % 2 == 0:
      continue
    
    # Plot each finger
    for finger in fingers:
      for col in finger:
        figure.plot(xs = [keypoints_3d[col[0], 0], keypoints_3d[col[1], 0]], ys = [keypoints_3d[col[0], 1], keypoints_3d[col[1], 1]], zs = [keypoints_3d[col[0], 2], keypoints_3d[col[1], 2]], linewidth = 4, c = "black")

    # Draw axes
    figure.plot(xs = [0,5], ys = [0,0], zs = [0,0], linewidth = 2, color = 'red')
    figure.plot(xs = [0,0], ys = [0,5], zs = [0,0], linewidth = 2, color = 'blue')
    figure.plot(xs = [0,0], ys = [0,0], zs = [0,5], linewidth = 2, color = 'black')

    #ax.set_axis_off()
    figure.set_xticks([])
    figure.set_yticks([])
    figure.set_zticks([])

    figure.set_xlim3d(-7, 8)
    figure.set_xlabel('x')
    figure.set_ylim3d(-7, 8)
    figure.set_ylabel('y')
    figure.set_zlim3d(0, 15)
    figure.set_zlabel('z')
    figure.elev = 0.2*i
    figure.azim = 0.2*i
    figure.cla()