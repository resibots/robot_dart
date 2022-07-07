#include <robot_dart/control/pd_control.hpp>
#include <robot_dart/robot_dart_simu.hpp>
#include <robot_dart/robots/iiwa.hpp>

#ifdef GRAPHIC
#include <robot_dart/gui/magnum/graphics.hpp>
#endif

int main()
{
    robot_dart::RobotDARTSimu simu(0.001);
    auto robot = std::make_shared<robot_dart::robots::Iiwa>();
    robot->set_actuator_types("servo");
    simu.add_robot(robot);
    // check if self-collision is enabled
    // @SELF_COLL@
    if (!robot->self_colliding()) {
        std::cout << "Self collision is not enabled" << std::endl;
        // set self collisions to true and adjacent collisions to false
        robot->set_self_collision(true, false);
    }
    // @SELF_COLL_END@

    return 0;
}