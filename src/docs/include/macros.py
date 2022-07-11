
def define_env(env):
    variables = {'INIT_SIMU': '```cpp\n// choose time step of 0.001 seconds\nrobot_dart::RobotDARTSimu simu(0.001);\n```', 'MODIFY_SIMU_DT': '```cpp\n// set timestep to 0.005 and update control frequency(bool)\nsimu.set_timestep(0.005, true);\n```', 'SIMU_GRAVITY': '```cpp\n// Set gravitational force of mars\nEigen::Vector3d mars_gravity = {0., 0., -3.721};\nsimu.set_gravity(mars_gravity);\n```', 'SHADOWS_GRAPHICS': '```cpp\n// Disable shadows\ngraphics->enable_shadows(false, false);\nsimu.run(1.);\n// Enable non-transparent shadows\ngraphics->enable_shadows(true, false);\nsimu.run(1.);\n// Enable transparent shadows\ngraphics->enable_shadows(true, true);\nsimu.run(1.);\n```', 'CLR_LIGHT': '```cpp\n// Clear Lights\ngraphics->clear_lights();\n```', 'LIGHT_MATERIAL': '```cpp\n// Create Light material\nMagnum::Float shininess = 1000.f;\nMagnum::Color4 white = {1.f, 1.f, 1.f, 1.f};\n\n// ambient, diffuse, specular\nauto custom_material = robot_dart::gui::magnum::gs::Material(white, white, white, shininess);\n```', 'POINT_LIGHT': '```cpp\n// Create point light\nMagnum::Vector3 position = {0.f, 0.f, 2.f};\nMagnum::Float intensity = 1.f;\nMagnum::Vector3 attenuation_terms = {1.f, 0.f, 0.f};\nauto point_light = robot_dart::gui::magnum::gs::create_point_light(position, custom_material, intensity, attenuation_terms);\ngraphics->add_light(point_light);\n```', 'DIRECTIONAL_LIGHT': '```cpp\n// Create directional light\nMagnum::Vector3 direction = {-1.f, -1.f, -1.f};\nauto directional_light = robot_dart::gui::magnum::gs::create_directional_light(direction, custom_material);\ngraphics->add_light(directional_light);\n```', 'SPOT_LIGHT': '```cpp\n// Create spot light\nMagnum::Vector3 position = {0.f, 0.f, 1.f};\nMagnum::Vector3 direction = {-1.f, -1.f, -1.f};\nMagnum::Float intensity = 1.f;\nMagnum::Vector3 attenuation_terms = {1.f, 0.f, 0.f};\nMagnum::Float spot_exponent = M_PI;\nMagnum::Float spot_cut_off = M_PI / 8;\nauto spot_light = robot_dart::gui::magnum::gs::create_spot_light(position, custom_material, direction, spot_exponent, spot_cut_off, intensity, attenuation_terms);\n```', 'RECORD_VIDEO_ROBOT_GRAPHICS_PARAMS': '```cpp\nrobot_dart::gui::magnum::GraphicsConfiguration configuration;\nconfiguration.width = 1280;\nconfiguration.height = 960;\nconfiguration.bg_color = Eigen::Vector4d{1.0, 1.0, 1.0, 1.0};\nauto graphics = std::make_shared<robot_dart::gui::magnum::Graphics>(configuration);\nsimu.set_graphics(graphics);\ngraphics->look_at({0., 3.5, 2.}, {0., 0., 0.25});\ngraphics->record_video("talos_dancing.mp4");\n```', 'SET_COLLISION_DETECTOR': '```cpp\nsimu.set_collision_detector("fcl"); // collision_detector can be "dart", "fcl", "ode" or "bullet" (case does not matter)\n```', 'SELF_COLLISIONS': '```cpp\nif (!robot->self_colliding()) {\n    std::cout << "Self collision is not enabled" << std::endl;\n    // set self collisions to true and adjacent collisions to false\n    robot->set_self_collision(true, false);\n}\n```', 'ROBOT_POOL_INCLUDE': '```cpp\n#include <robot_dart/robot_pool.hpp>\n```', 'ROBOT_POOL_GLOBAL_NAMESPACE': '```cpp\nnamespace pool {\n    // This function should load one robot: here we load Talos\n    inline std::shared_ptr<robot_dart::Robot> robot_creator()\n    {\n        return std::make_shared<robot_dart::robots::Talos>();\n    }\n\n    // To create the object we need to pass the robot_creator function and the number of maximum parallel threads\n    robot_dart::RobotPool robot_pool(robot_creator, NUM_THREADS);\n} // namespace pool\n```', 'ROBOT_POOL_EVAL': '```cpp\ninline void eval_robot(int i)\n{\n    // We get one available robot\n    auto robot = pool::robot_pool.get_robot();\n    std::cout << "Robot " << i << " got [" << robot->skeleton() << "]" << std::endl;\n\n    /// --- some robot_dart code ---\n    simulate_robot(robot);\n    // --- do something with the result\n\n    std::cout << "End of simulation " << i << std::endl;\n\n    // CRITICAL : free your robot !\n    pool::robot_pool.free_robot(robot);\n\n    std::cout << "Robot " << i << " freed!" << std::endl;\n}\n```', 'ROBOT_POOL_CREATE_THREADS': '```cpp\n// for the example, we run NUM_THREADS threads of eval_robot()\nstd::vector<std::thread> threads(NUM_THREADS * 2); // *2 to see some reuse\nfor (size_t i = 0; i < threads.size(); ++i)\n    threads[i] = std::thread(eval_robot, i); // eval_robot is the function that uses the robot\n```', 'ROBOT_GHOST': '```cpp\n// Add a ghost robot; only visuals, no dynamics, no collision\nauto ghost = robot->clone_ghost();\nsimu.add_robot(ghost);\n```', 'ADD_NEW_CAMERA': '```cpp\n// Add camera\nauto camera = std::make_shared<robot_dart::sensor::Camera>(graphics->magnum_app(), 256, 256);\n```', 'MANIPULATE_CAM_SEP': '```cpp\ncamera->camera().set_far_plane(5.f);\ncamera->camera().set_near_plane(0.01f);\ncamera->camera().set_fov(60.0f);\n```', 'MANIPULATE_CAM': '```cpp\ncamera->camera().set_camera_params(5., // far plane\n    0.01f, // near plane\n    60.0f, // field of view\n    600, // width\n    400 // height\n);\n```', 'CAM_POSITION': '```cpp\n// set the position of the camera, and the position where the main camera is looking at\nEigen::Vector3d cam_pos = {-0.5, -3., 0.75};\nEigen::Vector3d cam_looks_at = {0.5, 0., 0.2};\ncamera->look_at(cam_pos, cam_looks_at);\n```', 'CAM_ATTACH': '```cpp\nEigen::Isometry3d tf;\ntf = Eigen::AngleAxisd(3.14, Eigen::Vector3d{1., 0., 0.});\ntf *= Eigen::AngleAxisd(1.57, Eigen::Vector3d{0., 0., 1.});\ntf.translation() = Eigen::Vector3d(0., 0., 0.1);\ncamera->attach_to_body(robot->body_node("iiwa_link_ee"), tf); // cameras are looking towards -z by default\n```', 'HELLO_WORLD_INCLUDE': '```cpp\n#include <robot_dart/robot_dart_simu.hpp>\n\n#ifdef GRAPHIC\n#include <robot_dart/gui/magnum/graphics.hpp>\n#endif\n```', 'HELLO_WORLD_ROBOT_CREATION': '```cpp\nauto robot = std::make_shared<robot_dart::Robot>("pexod.urdf");\n```', 'HELLO_WORLD_ROBOT_PLACING': '```cpp\nrobot->set_base_pose(robot_dart::make_tf({0., 0., 0.2}));\n```', 'HELLO_WORLD_ROBOT_SIMU': '```cpp\nrobot_dart::RobotDARTSimu simu(0.001); // dt=0.001, 1KHz simulation\nsimu.add_floor();\nsimu.add_robot(robot);\n```', 'HELLO_WORLD_ROBOT_GRAPHIC': '```cpp\n#ifdef GRAPHIC\n    auto graphics = std::make_shared<robot_dart::gui::magnum::Graphics>();\n    simu.set_graphics(graphics);\n    graphics->look_at({0.5, 3., 0.75}, {0.5, 0., 0.2});\n#endif\n```', 'HELLO_WORLD_ROBOT_RUN': '```cpp\nsimu.run(10.);\n```', 'CAMERAS_PARALLEL': '```cpp\n// Load robot from URDF\nauto global_robot = std::make_shared<robot_dart::robots::Iiwa>();\n\nstd::vector<std::thread> workers;\n\n// Set maximum number of parallel GL contexts (this is GPU-dependent)\nrobot_dart::gui::magnum::GlobalData::instance()->set_max_contexts(4);\n\n// We want 15 parallel simulations with different GL context each\nsize_t N_workers = 15;\nstd::mutex mutex;\nsize_t id = 0;\n// Launch the workers\nfor (size_t i = 0; i < N_workers; i++) {\n    workers.push_back(std::thread([&] {\n        mutex.lock();\n        size_t index = id++;\n        mutex.unlock();\n\n        // Get the GL context -- this is a blocking call\n        // will wait until one GL context is available\n        // get_gl_context(gl_context); // this call will not sleep between failed queries\n        get_gl_context_with_sleep(gl_context, 20); // this call will sleep 20ms between each failed query\n\n        // Do the simulation\n        auto robot = global_robot->clone();\n\n        robot_dart::RobotDARTSimu simu(0.001);\n\n        Eigen::VectorXd ctrl = robot_dart::make_vector({0., M_PI / 3., 0., -M_PI / 4., 0., 0., 0.});\n\n        auto controller = std::make_shared<robot_dart::control::PDControl>(ctrl);\n        robot->add_controller(controller);\n        controller->set_pd(300., 50.);\n\n        // Magnum graphics\n        robot_dart::gui::magnum::GraphicsConfiguration configuration = robot_dart::gui::magnum::WindowlessGraphics::default_configuration();\n\n        configuration.width = 1024;\n        configuration.height = 768;\n        auto graphics = std::make_shared<robot_dart::gui::magnum::WindowlessGraphics>(configuration);\n        simu.set_graphics(graphics);\n        // Position the camera differently for each thread to visualize the difference\n        graphics->look_at({0.4 * index, 3.5 - index * 0.1, 2.}, {0., 0., 0.25});\n        // record images from main camera/graphics\n        // graphics->set_recording(true); // WindowlessGLApplication records images by default\n\n        simu.add_robot(robot);\n        simu.run(6);\n\n        // Save the image for verification\n        robot_dart::gui::save_png_image("camera_" + std::to_string(index) + ".png",\n            graphics->image());\n\n        // Release the GL context for another thread to use\n        release_gl_context(gl_context);\n    }));\n}\n\n// Wait for all the workers\nfor (size_t i = 0; i < workers.size(); i++) {\n    workers[i].join();\n}\n```', 'SET_ACTUATOR': '```cpp\n// Set all DoFs to same actuator\nrobot->set_actuator_types("servo"); // actuator types can be "servo", "torque", "velocity", "passive", "locked", "mimic"\n// You can also set actuator types separately\nrobot->set_actuator_type("torque", "iiwa_joint_5");\n```', 'POSITIONS_ENFORCED': '```cpp\n// Εnforce joint position and velocity limits\nrobot->set_position_enforced(true);\n```', 'MODIFY_LIMITS': '```cpp\n// Modify Position Limits\nEigen::VectorXd pos_upper_lims(7);\npos_upper_lims << 2.096, 2.096, 2.096, 2.096, 2.096, 2.096, 2.096;\nrobot->set_position_upper_limits(pos_upper_lims, dof_names);\nrobot->set_position_lower_limits(-pos_upper_lims, dof_names);\n\n// Modify Velocity Limits\n\nEigen::VectorXd vel_upper_lims(7);\nvel_upper_lims << 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5;\nrobot->set_velocity_upper_limits(vel_upper_lims, dof_names);\nrobot->set_velocity_lower_limits(-vel_upper_lims, dof_names);\n\n// Modify Force Limits\n\nEigen::VectorXd force_upper_lims(7);\nforce_upper_lims << 150, 150, 150, 150, 150, 150, 150;\nrobot->set_force_upper_limits(force_upper_lims, dof_names);\nrobot->set_force_lower_limits(-force_upper_lims, dof_names);\n\n// Modify Acceleration Limits\nEigen::VectorXd acc_upper_lims(7);\nacc_upper_lims << 1500, 1500, 1500, 1500, 1500, 1500, 1500;\nrobot->set_acceleration_upper_limits(acc_upper_lims, dof_names);\nrobot->set_acceleration_lower_limits(-acc_upper_lims, dof_names);\n```', 'MODIFY_COEFFS': '```cpp\n// Modify Damping Coefficients\nstd::vector<double> damps = {0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4};\nrobot->set_damping_coeffs(damps, dof_names);\n\n// Modify Coulomb Frictions\nstd::vector<double> cfrictions = {0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001};\nrobot->set_coulomb_coeffs(cfrictions, dof_names);\n\n// Modify  Spring Stiffness\nstd::vector<double> stiffnesses = {0.001, 0.001, 0.001, 0.001, 0.001, 0.001, 0.001};\nrobot->set_spring_stiffnesses(stiffnesses, dof_names);\n```', 'KINEMATICS': '```cpp\n// Get Joint Positions(Angles)\nauto joint_positions = robot->positions();\n\n// Get Joint Velocities\nauto joint_vels = robot->velocities();\n\n// Get Joint Accelerations\nauto joint_accs = robot->accelerations();\n\n// Get link_name(str) Transformation matrix with respect to the world frame.\nauto eef_tf = robot->body_pose(link_name);\n\n// Get translation vector from transformation matrix\nauto eef_pos = eef_tf.translation();\n\n// Get rotation matrix from tranformation matrix\nauto eef_rot = eef_tf.rotation();\n\n// Get link_name 6d pose vector [logmap(eef_tf.linear()), eef_tf.translation()]\nauto eef_pose_vec = robot->body_pose_vec(link_name);\n\n// Get link_name 6d velocity vector [angular, cartesian]\nauto eef_vel = robot->body_velocity(link_name);\n\n// Get link_name 6d acceleration vector [angular, cartesian]\nauto eef_acc = robot->body_acceleration(link_name);\n\n// Jacobian targeting the origin of link_name(str)\nauto jacobian = robot->jacobian(link_name);\n\n// Jacobian time derivative\nauto jacobian_deriv = robot->jacobian_deriv(link_name);\n\n// Center of Mass Jacobian\nauto com_jacobian = robot->com_jacobian(robot->dof_names());\n\n// Center of Mass Jacobian Time Derivative\nauto com_jacobian_deriv = robot->com_jacobian_deriv(robot->dof_names());\n```', 'DYNAMICS': "```cpp\n// Get Joint Forces\nauto joint_forces = robot->forces();\n\n// Get link's mass\nauto eef_mass = robot->body_mass(link_name);\n\n// Mass Matrix of robot\nauto mass_matrix = robot->mass_matrix();\n\n// Inverse of Mass Matrix\nauto inv_mass_matrix = robot->inv_mass_matrix();\n\n// Augmented Mass matrix\nauto aug_mass_matrix = robot->aug_mass_matrix();\n\n// Inverse of Augmented Mass matrix\nauto inv_aug_mass_matrix = robot->inv_aug_mass_matrix();\n\n// Coriolis Force vector\nauto coriolis = robot->coriolis_forces();\n\n// Gravity Force vector\nauto gravity = robot->gravity_forces();\n\n// Combined vector of Coriolis Force and Gravity Force\nauto coriolis_gravity = robot->coriolis_gravity_forces();\n\n// Constraint Force Vector\nauto constraint_forces = robot->constraint_forces(robot->dof_names());\n```"}
    for v in variables.items():
        env.variables[v[0]] = variables[v[0]]
