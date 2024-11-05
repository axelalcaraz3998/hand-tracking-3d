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
  # Joint 0
  theta[0] = np.atan2(coords[1], coords[0])
  # Joint 2
  theta[2] = -np.arccos(((np.sqrt(coords[0]**2 + coords[1]**2))**2 + (coords[2] - d_1)**2 - a_2**2 - d_4**2) / (2*a_2 * d_4))
  # Joint 1
  theta[1] = np.atan2((coords[2] - d_1), (np.sqrt(coords[0]**2 + coords[1]**2))) - np.atan2((d_4*np.sin(theta[2])), (a_2 + d_4*np.cos(theta[2])))

  # Convert from rad to deg and add offset
  angles[0] = np.rad2deg(theta[0]) + 0
  angles[1] = np.rad2deg(theta[1]) + 0
  angles[2] = np.rad2deg(theta[2]) + 0
  print(angles)

  sim.setJointTargetPosition(joint_2_obj, angles[2])
  sim.setJointTargetPosition(joint_1_obj, angles[1])
  sim.setJointTargetPosition(joint_0_obj, angles[0])

coords = np.array([0, 0, 0])
inverse_kinematics(coords)