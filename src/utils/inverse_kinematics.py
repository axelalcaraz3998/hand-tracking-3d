from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np

# Robot constants
d_1 = 20
d_4 = 20
a_2 = 20

# Theta and angles array
theta = np.empty(6)

# Coppeliasim Remote API
client = RemoteAPIClient()
sim = client.require("sim")

# Robot joints
joint_0_obj = sim.getObject("./joint_0")
joint_1_obj = sim.getObject("./joint_1")
joint_2_obj = sim.getObject("./joint_2")
joint_3_obj = sim.getObject("./joint_3")
joint_4_obj = sim.getObject("./joint_4")
joint_5_obj = sim.getObject("./joint_5")

def inverse_kinematics(coords, orientation):
  # Get coordinates
  x = coords[1]
  y = coords[0]
  z = coords[2]

  # Get hand orientation
  alpha = orientation[1]
  miu = orientation[0]
  phi = orientation[2]
  
  # Normalize coordinates
  x = -x
  x += 25
  if x > 25:
    x = 25
  elif x < 0:
    x = 0

  if y > 25:
    y = 25
  elif y < -25:
    y = -25

  z -= 30
  if z > 25:
    z = 25
  elif z < 0:
    z = 0

  # Joint 0
  theta[0] = np.atan2(y, x)
  # Joint 2
  theta[2] = -np.arccos(((np.sqrt(x**2 + y**2))**2 + (z - d_1)**2 - a_2**2 - d_4**2) / (2*a_2 * d_4))
  # Joint 1
  theta[1] = np.atan2((z - d_1), (np.sqrt(x**2 + y**2))) - np.atan2((d_4*np.sin(theta[2])), (a_2 + d_4*np.cos(theta[2])))

  # Rotation matrices
  R1 = [[np.cos(theta[0]), 0, np.sin(theta[0])], [np.sin(theta[0]), 0, -np.cos(theta[0])], [0, 1, 0]]
  R2 = [[np.cos(theta[1]), -np.sin(theta[1]), 0], [np.sin(theta[1]), np.cos(theta[1]), 0], [0, 0, 1]]
  R3 = [[np.cos(theta[2]), 0, np.sin(theta[2])], [np.sin(theta[2]), 0, -np.cos(theta[2])], [0, 1, 0]]
  R03 = np.matmul(R1, np.matmul(R2, R3))

  alpha = alpha + (np.pi * 0.5)

  # Orientation matrices
  RA = [[np.cos(phi), 0, -np.sin(phi)], [np.sin(phi), 0, np.cos(phi)], [0, -1, 0]]
  RB = [[np.cos(alpha), 0, np.sin(alpha)], [np.sin(alpha), 0, -np.cos(alpha)], [0, 1, 0]]
  RC = [[np.cos(miu), -np.sin(miu), 0], [np.sin(miu), np.cos(miu), 0], [0, 0, 1]]
  RT = np.matmul(RA, np.matmul(RB, RC))
  R36 = np.matmul(np.transpose(R03), RT)

  # Joint 3
  theta[3] = np.atan2(R36[1, 2], R36[0, 2])
  # Joint 4
  theta[4] = np.atan2(np.sqrt(R36[0, 2]**2 + R36[1, 2]**2), R36[2, 2])
  # Joint 5
  theta[5] = np.atan2(R36[2, 1], -R36[2, 0])

  sim.setJointTargetPosition(joint_5_obj, theta[5] + 0)
  sim.setJointTargetPosition(joint_4_obj, theta[4] + 0)
  sim.setJointTargetPosition(joint_3_obj, theta[3] + 0)
  sim.setJointTargetPosition(joint_2_obj, theta[2] + 3*(np.pi * 0.25))
  sim.setJointTargetPosition(joint_1_obj, theta[1] - 3*(np.pi * 0.25))
  sim.setJointTargetPosition(joint_0_obj, theta[0] + 0)