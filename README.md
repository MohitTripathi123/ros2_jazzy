# ROS 2 Jazzy: Complete Robotics Developer Course

Student code and written lecture companions for the ROS 2 Jazzy course. The repository follows the published Udemy curriculum from the first ROS 2 node through simulation, navigation, perception, MoveIt 2, and full-system integration.

## Course material

- [All 83 lecture descriptions](course_lectures/README.md)
- `src/` contains the ROS 2 packages used in the demonstrations and projects.

## Packages

| Package | Course area |
| --- | --- |
| `my_first_pkg`, `my_first_interfaces` | Nodes, topics, services, actions, parameters, and launch files |
| `integration_demo` | Velocity-controller integration, YAML parameters, and validation |
| `runtime_demo`, `turtle_runtime_demo` | Executors, callback flow, and runtime visualization |
| `qos_demo` | QoS and clean shutdown examples |
| `lifecycle_demo` | Managed lifecycle nodes |
| `conveyor_interfaces`, `conveyor_system` | Autonomous conveyor monitoring final project |
| `robot_description` | URDF, Xacro, Gazebo, TF, Nav2, odometry, and EKF material |
| `image_processing`, `yolo_detection` | OpenCV and YOLO perception |
| `object_tracking`, `object_counting` | DeepSORT tracking and event counting |

## Build

Use Ubuntu 24.04 with ROS 2 Jazzy. From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

The perception examples additionally require their Python libraries:

```bash
python3 -m pip install ultralytics deep-sort-realtime
```

YOLO model weights are intentionally not stored in Git. Ultralytics downloads the named model on first use.

## Third-party course dependencies

Generated build outputs, local virtual environments, downloaded binary models, and third-party source checkouts are intentionally excluded. Install the ROS 2 Jazzy versions of Gazebo, Nav2, MoveIt 2, `ros_gz`, and `robot_localization` as introduced in the corresponding lectures.

The videos and quizzes remain on Udemy; this repository contains the supporting source code and lecture index.
