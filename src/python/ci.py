import numpy as np
import dartpy
import RobotDART as rd

# Create custom controller
class MyController(rd.RobotControl):
    def __init__(self, ctrl, full_control):
        rd.RobotControl.__init__(self, ctrl, full_control)

    def configure(self):
        self._active = True

    def calculate(self, t):
        target = np.array([self._ctrl])
        cmd = 100*(target-self.get_positions())
        return cmd[0]

    # TO-DO: This is NOT working at the moment!
    def clone(self):
        return MyController(self._ctrl, self._full_control)

# Load robot from URDF
robot = rd.Robot("res/models/arm.urdf", "arm", False)
robot.fix_to_world()

# Initiate custom controller
control = MyController([0.0, 2, -0.5, 0.7], False)
# Add it to the robot
robot.add_controller(control, 1.)

# Print initial positions of the robot
print(control.get_positions())

# Create simulator object
simu = rd.RobotDARTSimu(0.001)

# Add robot and floor to the simulation
simu.add_robot(robot)
simu.add_checkerboard_floor(10., 0.1, 1., np.zeros((6,1)), "floor")

simu.run(5.)

print(control.get_positions())