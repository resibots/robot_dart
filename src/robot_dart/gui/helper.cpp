#include "helper.hpp"

#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"

namespace robot_dart {
    namespace gui {
        void save_png_image(const std::string& filename, const Image& rgb)
        {
            auto ends_with = [](const std::string& value, const std::string& ending) {
                if (ending.size() > value.size())
                    return false;
                return std::equal(ending.rbegin(), ending.rend(), value.rbegin());
            };

            std::string png = ".png";
            if (ends_with(filename, png))
                png = "";

            stbi_write_png((filename + png).c_str(), rgb.width, rgb.height, rgb.channels, rgb.data.data(), rgb.width * rgb.channels);
        }

        void save_png_image(const std::string& filename, const GrayscaleImage& gray)
        {
            auto ends_with = [](const std::string& value, const std::string& ending) {
                if (ending.size() > value.size())
                    return false;
                return std::equal(ending.rbegin(), ending.rend(), value.rbegin());
            };

            std::string png = ".png";
            if (ends_with(filename, png))
                png = "";

            stbi_write_png((filename + png).c_str(), gray.width, gray.height, 1, gray.data.data(), gray.width);
        }

        GrayscaleImage convert_rgb_to_grayscale(const Image& rgb)
        {
            assert(rgb.channels == 3);
            size_t width = rgb.width;
            size_t height = rgb.height;

            GrayscaleImage gray;
            gray.width = width;
            gray.height = height;
            gray.data.resize(width * height);

            for (size_t h = 0; h < height; h++) {
                for (size_t w = 0; w < width; w++) {
                    int id = w + h * width;
                    int id_rgb = w * rgb.channels + h * (width * rgb.channels);
                    uint8_t color = 0.3 * rgb.data[id_rgb + 0] + 0.59 * rgb.data[id_rgb + 1] + 0.11 * rgb.data[id_rgb + 2];
                    gray.data[id] = color;
                }
            }

            return gray;
        }

        std::vector<double> point_cloud_from_depth_array_vector(const DepthImage& depth_image, const Eigen::Matrix3d& intrinsic_matrix, const Eigen::Matrix4d& tf, double far_plane)
        {
            // This is assuming that K is normal intrisinc matrix (i.e., camera pointing to +Z),
            // but an OpenGL camera (i.e., pointing to -Z). Thus it transforms the points accordingly
            // TO-DO: Format the intrinsic matrix correctly, and take as an argument the camera orientation
            // with respect to the normal cameras. See http://ksimek.github.io/2013/06/03/calibrated_cameras_in_opengl/.
            auto point_3d = [](const Eigen::Matrix3d& K, size_t u, size_t v, double depth) {
                double fx = K(0, 0);
                double fy = K(1, 1);
                double cx = K(0, 2);
                double cy = K(1, 2);
                double gamma = K(0, 1);

                Eigen::Vector3d p;
                p << 0., 0., -depth;

                p(1) = (cy - v) * depth / fy;
                p(0) = -((cx - u) * depth - gamma * p(1)) / fx;

                return p;
            };

            size_t height = depth_image.height;
            size_t width = depth_image.width;

            std::vector<double> point_cloud;
            point_cloud.reserve(height * width * 3);

            Eigen::Matrix3d R_inv = tf.block<3, 3>(0, 0).transpose();
            Eigen::Vector3d t_inv = -R_inv * tf.block<3, 1>(0, 3);

            Eigen::Vector3d pp;
            for (size_t h = 0; h < height; h++) {
                for (size_t w = 0; w < width; w++) {
                    int id = w + h * width;
                    if (depth_image.data[id] >= 0.99 * far_plane) // close to far plane
                        continue;
                    pp = R_inv * point_3d(intrinsic_matrix, w, h, depth_image.data[id]) + t_inv;

                    point_cloud.push_back(pp[0]);
                    point_cloud.push_back(pp[1]);
                    point_cloud.push_back(pp[2]);
                }
            }

            return point_cloud;
        }

        Eigen::MatrixXd point_cloud_from_depth_array(const DepthImage& depth_image, const Eigen::Matrix3d& intrinsic_matrix, const Eigen::Matrix4d& tf, double far_plane)
        {
            auto v = point_cloud_from_depth_array_vector(depth_image, intrinsic_matrix, tf, far_plane);
            return Eigen::MatrixXd::Map(v.data(), 3, v.size() / 3);
        }
    } // namespace gui
} // namespace robot_dart