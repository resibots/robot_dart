#ifndef ROBOT_DART_GUI_MAGNUM_WINDOWLESS_GRAPHICS_HPP
#define ROBOT_DART_GUI_MAGNUM_WINDOWLESS_GRAPHICS_HPP

#include <robot_dart/gui/magnum/base_graphics.hpp>
#include <robot_dart/gui/magnum/windowless_gl_application.hpp>

namespace robot_dart {
    namespace gui {
        namespace magnum {
            class WindowlessGraphics : public BaseGraphics<WindowlessGLApplication> {
            public:
                WindowlessGraphics(const GraphicsConfiguration& configuration = default_configuration()) : BaseGraphics<WindowlessGLApplication>(configuration) {}
                ~WindowlessGraphics() {}

                void set_simu(RobotDARTSimu* simu) override;

                static GraphicsConfiguration default_configuration();
            };
        } // namespace magnum
    } // namespace gui
} // namespace robot_dart

#endif