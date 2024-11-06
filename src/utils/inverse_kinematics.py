from coppeliasim_zmqremoteapi_client import RemoteAPIClient
import numpy as np

# Robot constants
d_1 = 20
d_4 = 20
a_2 = 20

# Theta and angles array
theta = np.empty(3)
angles = np.empty(3)

# Coppeliasim Remote API
client = RemoteAPIClient()
sim = client.require("sim")

joint_0_obj = sim.getObject("./joint_0")
joint_1_obj = sim.getObject("./joint_1")
joint_2_obj = sim.getObject("./joint_2")

def inverse_kinematics(coords):
  # Get coordinates
  x = coords[1]
  y = coords[0]
  z = coords[2]
  
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

  sim.setJointTargetPosition(joint_2_obj, theta[2] + (np.pi * 0.5))
  sim.setJointTargetPosition(joint_1_obj, theta[1] + 0)
  sim.setJointTargetPosition(joint_0_obj, theta[0] + 0)

# coords = np.array([25, -25, 25])
# inverse_kinematics(coords)