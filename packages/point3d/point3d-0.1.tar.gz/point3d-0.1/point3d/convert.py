import math
import numpy as np

def convert(ax:float, ay:float, az:float, camera_position:tuple, camera_rotation:tuple):
    ex, ey, ez = (camera_position[0] - ax,
                  camera_position[1] - ay, camera_position[2] - az)
    ox, oy, oz = camera_rotation
    cx, cy, cz = camera_position
    m_1 = np.array([[1, 0, 0], 
                  [0, -math.cos(ox), math.sin(ox)],
                  [0, -math.sin(ox), math.cos(ox)]])
    m_2 = np.array([[math.cos(oy), 0, -math.sin(oy)],
                  [0, 1, 0], 
                  [math.sin(oy), 0, math.cos(oy)]])
    m_3 = np.array([[math.cos(oz), math.sin(oz), 0],
                  [-math.sin(oz), math.cos(oz), 0],
                  [0, 0, 1]])
    m_4 = np.array([ax - cx, ay - cy, az - cz])
    d = m_4.dot(m_3.dot(m_2.dot(m_1)))
    x = (ez/d[2])*d[0]+ex
    y = (ez/d[2])*d[1]+ey
    return x, y