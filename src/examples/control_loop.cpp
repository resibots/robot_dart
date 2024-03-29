#include <robot_dart/robot_dart_simu.hpp>
#include <robot_dart/robots/pendulum.hpp>

#ifdef GRAPHIC
#include <robot_dart/gui/magnum/graphics.hpp>
#endif

int main()
{
    auto robot = std::make_shared<robot_dart::robots::Pendulum>();

    robot_dart::RobotDARTSimu simu(0.001);
#ifdef GRAPHIC
    simu.set_graphics(std::make_shared<robot_dart::gui::magnum::Graphics>());
#endif

    simu.add_robot(robot);
    simu.set_control_freq(100); // 100 Hz

    std::vector<std::string> dofs = {"pendulum_joint_1"};
    while (simu.scheduler().next_time() < 10 && !simu.graphics()->done()) { // simulate 10 seconds
        if (simu.schedule(simu.control_freq())) {
            Eigen::VectorXd commands = Eigen::VectorXd::Random(1) * 100;
            robot->set_commands(commands, dofs);
        }
        simu.step_world();
    }
    return 0;
}
