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

# Helper function to normalize coordinates
def clamp(value, min_val, max_val):
  return max(min_val, min(value, max_val))

def inverse_kinematics(coords, orientation):
  # Get coordinates
  x = coords[1]
  y = coords[0]
  z = coords[2]

  # Get hand orientation
  alpha = orientation[0]
  miu = orientation[1]
  phi = orientation[2]
  
  # Normalize coordinates
  x = -x + 25
  x = clamp(x, 0, 25)

  y = clamp(y, -25, 25)

  z -= 50
  z = clamp(z, 0, 25)

  # Joint 0
  theta[0] = np.atan2(y, x)
  # Joint 2
  theta[2] = -np.arccos(((np.sqrt(x**2 + y**2))**2 + (z - d_1)**2 - a_2**2 - d_4**2) / (2*a_2 * d_4))
  # Joint 1
  theta[1] = np.atan2((z - d_1), (np.sqrt(x**2 + y**2))) - np.atan2((d_4*np.sin(theta[2])), (a_2 + d_4*np.cos(theta[2])))

  # Normalize angles
  theta[1] = clamp(theta[1], -3*(np.pi * 0.25), 3*(np.pi * 0.25))
  theta[2] = clamp(theta[2], -3*(np.pi * 0.25), 3*(np.pi * 0.25))

  # Orientation offsets
  alpha = alpha - (theta[1] + theta[3])
  phi = phi - theta[0]

  # Rotation coordinates
  x2 = np.cos(alpha) * np.cos(phi)
  y2 = np.sin(alpha) * np.cos(phi)
  z2 = np.sin(phi)

  # Joint 3
  theta[3] = np.atan(y2 / z2)
  # Joint 4
  theta[4] = -np.atan(z2 / (np.sqrt(x2/y2)))
  # Joint 5
  theta[5] = -theta[3] + miu

  sim.setJointTargetPosition(joint_5_obj, theta[5] + (np.pi * 0.5))
  sim.setJointTargetPosition(joint_4_obj, theta[4] + 0)
  sim.setJointTargetPosition(joint_3_obj, theta[3] + 0)
  sim.setJointTargetPosition(joint_2_obj, theta[2] + 3*(np.pi * 0.25))
  sim.setJointTargetPosition(joint_1_obj, theta[1] - 3*(np.pi * 0.25))
  sim.setJointTargetPosition(joint_0_obj, theta[0] + 0)