cmake_minimum_required(VERSION 3.8)
project(four_wheel_robot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

# Install directories containing robot descriptions, launch scripts, controller configs, worlds, and meshes
install(
  DIRECTORY
    description
    launch
    config
    worlds
    meshes
    scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
