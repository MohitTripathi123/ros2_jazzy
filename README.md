# ROS 2 Jazzy: Complete Robotics Developer Course

Student code and written lecture companions for the ROS 2 Jazzy course. The repository follows the published Udemy curriculum from the first ROS 2 node through simulation, navigation, perception, MoveIt 2, and full-system integration.

## Course material

- [All 83 lecture descriptions](course_lectures/README.md)
- [Core ROS 2 practical checkpoints: Lectures 3–39](course_lectures/core-practical-checkpoints.md)
- [Applied robotics practical checkpoints: Lectures 40–83](course_lectures/applied-practical-checkpoints.md)
- [Verification status and runtime test checklist](course_lectures/verification.md)
- `src/` contains the ROS 2 packages used in the demonstrations and projects.

## How students should use this repository

1. Find the lecture number in the guide below.
2. Read the linked section notes, then open the listed package or file.
3. Build from the repository root after changing source code.
4. If a row says **Concept / CLI**, there is intentionally no separate source file. Follow the video and run the commands yourself.
5. If a row says **Generated exercise output**, create that file during the lecture. Generated maps, TF graphs, build folders, virtual environments, and downloaded model weights are intentionally not committed.

The same file can appear in several lectures because the course develops one system incrementally. The checked-in source is the final integrated example, not a separate snapshot of every intermediate video step. Use the row matching your lecture and its practical checkpoint for the current commands, expected result, and known differences. The recordings and published lecture order are unchanged.

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

## Lecture-to-code guide

### [Section 1: Course Orientation & ROS 2 Setup](course_lectures/sections/section-01-course-orientation-and-setup.md)

| Lecture | Open in this repository |
| --- | --- |
| 1 — Before You Start Phase 1: How to Learn Core ROS 2 Properly | **Orientation:** read the section notes; no source file is required. |
| 2 — Course Orientation & Roadmap | **Orientation:** [course index](course_lectures/README.md); no source file is required. |
| 3 — Installing ROS 2 Jazzy | **Setup exercise:** follow the lecture, then use the [build commands](#build). |
| 4 — Installing VS Code for ROS 2 Development | **Setup exercise:** editor configuration is local and is not committed. |
| 5 — Creating Your First ROS 2 Package | [`src/my_first_pkg`](src/my_first_pkg), especially [`package.xml`](src/my_first_pkg/package.xml) and [`setup.py`](src/my_first_pkg/setup.py). |
| 6 — Colcon Build System | Use the [build commands](#build); generated `build/`, `install/`, and `log/` directories are ignored. |

### [Section 2: ROS 2 Core Foundations](course_lectures/sections/section-02-core-foundations.md)

| Lecture | Open in this repository |
| --- | --- |
| 7 — Writing Your First ROS 2 Node | [`simple_node.txt`](src/my_first_pkg/my_first_pkg/simple_node.txt) — a teaching snippet to type and run as Python. |
| 8 — Publisher Node | [`publisher_node.py`](src/my_first_pkg/my_first_pkg/publisher_node.py). |
| 9 — Subscriber Node | [`subscriber_node.py`](src/my_first_pkg/my_first_pkg/subscriber_node.py) with the Lecture 8 publisher. |
| 10 — Topic CLI Tools | **Concept / CLI:** run the commands against the Lecture 8–9 publisher and subscriber. |
| 11 — Services | [`add_two_ints_server.py`](src/my_first_pkg/my_first_pkg/add_two_ints_server.py) and [`add_two_ints_client.py`](src/my_first_pkg/my_first_pkg/add_two_ints_client.py). |

### [Section 3: Advanced ROS 2 Communication](course_lectures/sections/section-03-advanced-communication.md)

| Lecture | Open in this repository |
| --- | --- |
| 12 — Actions with a Separate Interface Package | [`Fibonacci.action`](src/my_first_interfaces/action/Fibonacci.action), [`my_first_interfaces`](src/my_first_interfaces), and [`fibonacci_action_server.py`](src/my_first_pkg/my_first_pkg/fibonacci_action_server.py). |
| 13 — Parameters | [`parameter_example.py`](src/my_first_pkg/my_first_pkg/parameter_example.py). |
| 14 — Parameter Callbacks & Validation | [`parameter_callback_example.py`](src/my_first_pkg/my_first_pkg/parameter_callback_example.py). |
| 15 — Launch Files | [`multi_node_launch.py`](src/my_first_pkg/launch/multi_node_launch.py). |
| 16 — Launch Arguments | [`multi_node_launch.py`](src/my_first_pkg/launch/multi_node_launch.py), especially its declared arguments and `LaunchConfiguration` values. |
| 17 — Advanced Launch (Namespaces, Conditions, Groups) | [`multi_node_launch.py`](src/my_first_pkg/launch/multi_node_launch.py), especially namespace and condition usage. |
| 18 — ROS 2 CLI Deep Dive | **Concept / CLI:** inspect the nodes started by [`multi_node_launch.py`](src/my_first_pkg/launch/multi_node_launch.py). |

### [Section 4: ROS 2 Integration & System Architecture](course_lectures/sections/section-04-integration-and-architecture.md)

| Lecture | Open in this repository |
| --- | --- |
| 19 — Mini Integration System: Velocity Controller | [`integration_demo`](src/integration_demo): [`velocity_publisher.py`](src/integration_demo/integration_demo/velocity_publisher.py), [`integration_launch.py`](src/integration_demo/launch/integration_launch.py), and [`params.yaml`](src/integration_demo/config/params.yaml). |
| 20 — Clean Package Structure & ROS 2 Best Practices | Compare [`integration_demo`](src/integration_demo) with [`my_first_pkg`](src/my_first_pkg), including their manifests, setup files, launch, config, resource, and test folders. |
| 21 — ROS Graph & System Visualization | **Concept / CLI:** launch [`integration_launch.py`](src/integration_demo/launch/integration_launch.py), then inspect its graph. Generated TF/graph files are not committed. |
| 22 — YAML Parameter Files | [`params.yaml`](src/integration_demo/config/params.yaml) and the loading logic in [`integration_launch.py`](src/integration_demo/launch/integration_launch.py). |

### [Section 5: ROS 2 Execution Model & Runtime Engineering](course_lectures/sections/section-05-runtime-engineering.md)

| Lecture | Open in this repository |
| --- | --- |
| 23 — Executors & Callback Flow: Single-Threaded Executor | [`execution_demo.py`](src/runtime_demo/runtime_demo/execution_demo.py). |
| 24 — Turtlesim Runtime Visualization | [`turtle_control.py`](src/turtle_runtime_demo/turtle_runtime_demo/turtle_control.py). |
| 25 — Multi-Threaded Executors | [`control_node.py`](src/conveyor_system/conveyor_system/control_node.py) contains the later integrated `MultiThreadedExecutor` example. |
| 26 — Callback Groups | [`control_node.py`](src/conveyor_system/conveyor_system/control_node.py), especially `ReentrantCallbackGroup`. |
| 27 — QoS Fundamentals | [`qos_test.py`](src/qos_demo/qos_demo/qos_test.py). |
| 28 — Clean Shutdown & Error Handling | [`safe_shutdown_demo.py`](src/qos_demo/qos_demo/safe_shutdown_demo.py). |

### [Section 6: Professional ROS 2 Concepts](course_lectures/sections/section-06-professional-concepts.md)

| Lecture | Open in this repository |
| --- | --- |
| 29 — Lifecycle Nodes | [`lifecycle_node_demo.py`](src/lifecycle_demo/lifecycle_demo/lifecycle_node_demo.py). |
| 30 — ros2_control & Hardware Abstraction Overview | **Concept / external ROS package:** no copied `ros2_control` source is stored here. Use the section notes and installed ROS 2 Jazzy packages. |

### [Section 7: Final Project — Autonomous Conveyor Monitoring Micro-System](course_lectures/sections/section-07-conveyor-project.md)

| Lecture | Open in this repository |
| --- | --- |
| 31 — Final Project Architecture Planning | [`conveyor_interfaces`](src/conveyor_interfaces), [`conveyor_system`](src/conveyor_system), and the section notes for the planned responsibilities. |
| 32 — Creating Custom Interfaces for the Monitoring System | [`BoxState.msg`](src/conveyor_interfaces/msg/BoxState.msg), [`BeltCommand.msg`](src/conveyor_interfaces/msg/BeltCommand.msg), [`SystemAlert.msg`](src/conveyor_interfaces/msg/SystemAlert.msg), and [`SetMode.srv`](src/conveyor_interfaces/srv/SetMode.srv). |
| 33 — Sensor Node Implementation | [`sensor_node.py`](src/conveyor_system/conveyor_system/sensor_node.py). |
| 34 — Processing Node Implementation | [`control_node.py`](src/conveyor_system/conveyor_system/control_node.py), which processes box state and publishes belt commands. |
| 35 — Control Node with Service-Based Mode Switching | [`operator_service_node.py`](src/conveyor_system/conveyor_system/operator_service_node.py) and [`SetMode.srv`](src/conveyor_interfaces/srv/SetMode.srv). |
| 36 — Lifecycle-Based Monitoring Node | [`safety_supervisor_node.py`](src/conveyor_system/conveyor_system/safety_supervisor_node.py). |
| 37 — Full Launch System Integration | [`conveyor_system.launch.py`](src/conveyor_system/launch/conveyor_system.launch.py). |
| 38 — YAML Configuration, Parameters & QoS Integration | [`system_params.yaml`](src/conveyor_system/config/system_params.yaml), [`sensor_node.py`](src/conveyor_system/conveyor_system/sensor_node.py), and [`control_node.py`](src/conveyor_system/conveyor_system/control_node.py). |
| 39 — Final Debugging, Refactoring & Strong ROS 2 Engineer Wrap-Up | Review the complete [`conveyor_system`](src/conveyor_system) and [`conveyor_interfaces`](src/conveyor_interfaces) packages. |

### [Section 8: Simulation Workflow, URDF, Xacro and Robot Modeling](course_lectures/sections/section-08-simulation-and-modeling.md)

| Lecture | Open in this repository |
| --- | --- |
| 40 — Before You Start Phase 2: Moving from Core ROS 2 to Applied Robotics | **Orientation:** read the section notes; no new source file is required. |
| 41 — Simulation Workflow & Gazebo Introduction | [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py) and [`simple_robot_world.sdf`](src/robot_description/worlds/simple_robot_world.sdf). |
| 42 — Understanding Robot Description with URDF | [`simple_robot.urdf`](src/robot_description/urdf/simple_robot.urdf). |
| 43 — Building a Differential Drive Robot Model | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro), especially the base and wheel links/joints. |
| 44 — XACRO: Writing Clean and Reusable Robot Models | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro), especially properties and wheel macros. |
| 45 — Understanding robot_state_publisher and joint_state_publisher | [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py) and [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro). |
| 46 — TF2: Understanding Frames and Transforms | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) and the frame publishers in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 47 — TF Debugging: view_frames and Real Issues | **Concept / CLI:** run TF tools against the simulation. Generated `frames_*.gv` and `frames_*.pdf` files are intentionally ignored. |
| 48 — Adding a LiDAR Sensor: Robot Model vs Real Sensor | LiDAR links, joints, and sensor definition in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro). |
| 49 — Adding Camera Sensor & Understanding Optical Frame | Camera and optical-frame definitions in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro). |
| 50 — Visual, Collision, Inertial and Spawning Robot in Gazebo | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) and SDF generation/spawning in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 51 — Launch Files for Robot Simulation System | [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 52 — Gazebo World, Physics and Ground Plane | [`simple_robot_world.sdf`](src/robot_description/worlds/simple_robot_world.sdf). |

### [Section 9: Sensor Integration, ROS-GZ Bridge and LaserScan](course_lectures/sections/section-09-sensor-integration.md)

| Lecture | Open in this repository |
| --- | --- |
| 53 — LiDAR Integration in Gazebo, Scan Bridging, and RViz Visualization | LiDAR sensor in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) and `/scan` bridge in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 54 — LaserScan Deep Understanding: From Data to Meaning | **Concept + model configuration:** inspect the LiDAR scan parameters in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro). |

### [Section 10: SLAM, Mapping, Odometry and TF Reality Check](course_lectures/sections/section-10-slam-mapping-and-amcl.md)

| Lecture | Open in this repository |
| --- | --- |
| 55 — SLAM Fundamentals | **Concept + system reference:** [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py) shows the `map`, `odom`, `base_link`, and scan inputs. |
| 56 — SLAM Implementation, Installation & Debugging | SLAM Toolbox lifecycle setup in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py); launch with `use_slam:=true`. |
| 57 — Mapping Deep Dive: Save Map + Quality | **Generated exercise output:** create the map during the lecture. Runtime `my_map.pgm` and `my_map.yaml` files are intentionally ignored. |
| 58 — Odometry Deep Dive: Motion, TF & Reality Check | Differential-drive/odometry configuration in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) and bridges in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 59 — Motion System Integration: Diff Drive + Bridges + TF + SLAM | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) together with [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 60 — TF2 Deep Dive: Frame System | Frame definitions in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro) and frame publishers/bridges in [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 61 — AMCL Localization: Concept + Setup | AMCL settings in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml). The saved map is generated during Lecture 57. |

### [Section 11: Nav2 Navigation Stack, Planning and Behavior Trees](course_lectures/sections/section-11-nav2.md)

| Lecture | Open in this repository |
| --- | --- |
| 62 — Advanced Debugging for AMCL, TF, Lifecycle and Nav2 | [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml), [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py), and the section's CLI checklist. |
| 63 — Nav2 Architecture & Behavior Trees | Server and navigator configuration in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml). |
| 64 — Global & Local Planning: A* and DWA Concepts | Planner and controller sections in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml); algorithm explanations are conceptual. |
| 65 — Costmaps & Parameter Tuning | Local/global costmap sections in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml). |
| 66 — nav2_params.yaml Deep Dive | [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml). |
| 67 — Behavior Tree XML Deep Dive | **Concept / installed Nav2 resource:** behavior-tree selection is configured in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml); built-in Nav2 XML is not copied into this repository. |
| 68 — Nav2 Recovery Behaviors Inside Behavior Tree | Behavior-server and recovery settings in [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml); the behavior-tree flow is explained in the section notes. |

### [Section 12: Robot Motion, Odometry, Localization and EKF](course_lectures/sections/section-12-motion-localization-and-ekf.md)

| Lecture | Open in this repository |
| --- | --- |
| 69 — TF Tree Deep Dive: map → odom → base_link | Frame configuration in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro), [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py), and [`nav2_params.yaml`](src/robot_description/config/nav2_params.yaml). |
| 70 — Odometry vs Localization: Fusion Concept | **Concept + configuration:** [`ekf.yaml`](src/robot_description/config/ekf.yaml) and the section notes. |
| 71 — Robot Kinematics: Differential Drive | Wheel geometry and differential-drive configuration in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro). |
| 72 — Odometry Computation from Wheels | Differential-drive odometry configuration in [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro); the derivation is in the section notes. |
| 73 — EKF: Extended Kalman Filter Introduction | [`ekf.yaml`](src/robot_description/config/ekf.yaml): single `/odom` input. See the [separate-run and TF-ownership instructions](course_lectures/applied-practical-checkpoints.md#lectures-6973-odometry-and-the-single-source-ekf). |

### [Section 13: MoveIt 2 and Robot Manipulation](course_lectures/sections/section-13-moveit2.md)

| Lecture | Open in this repository |
| --- | --- |
| 74 — MoveIt 2 Introduction | **Concept / external ROS package:** use the section notes and the ROS 2 Jazzy MoveIt 2 installation; upstream tutorials are not copied here. |
| 75 — Inverse Kinematics: IK Basics | **Concept / MoveIt 2 exercise:** no separate authored source file is required. |
| 76 — Forward Kinematics: FK Concept | **Concept / MoveIt 2 exercise:** no separate authored source file is required. |
| 77 — MoveIt 2 Planning Pipeline | **Concept / MoveIt 2 exercise:** use the installed MoveIt 2 demo and section notes. |

### [Section 14: Perception with OpenCV, YOLO and DeepSORT](course_lectures/sections/section-14-perception.md)

| Lecture | Open in this repository |
| --- | --- |
| 78 — OpenCV with ROS2: Perception Begins | [`image_node.py`](src/image_processing/image_processing/image_node.py). First complete the [camera/bridge prerequisite](course_lectures/applied-practical-checkpoints.md#lectures-7882-camera-to-perception-workflow) demonstrated in Lecture 82. |
| 79 — Object Detection: YOLO with ROS2 | [`yolo_node.py`](src/yolo_detection/yolo_detection/yolo_node.py). Model weights download at runtime and are not committed. |
| 80 — Object Tracking: DeepSORT with ROS2 | [`tracking_node.py`](src/object_tracking/object_tracking/tracking_node.py). |
| 81 — Object Counting & Event Detection | [`counting_node.py`](src/object_counting/object_counting/counting_node.py). |

### [Section 15: Full Robotics System Integration and Multi-Node Design](course_lectures/sections/section-15-full-system-integration.md)

| Lecture | Open in this repository |
| --- | --- |
| 82 — Simulation + Full Integration: Gazebo Sim + ROS-GZ Bridge | [`simple_robot.xacro`](src/robot_description/urdf/simple_robot.xacro), [`simple_robot_world.sdf`](src/robot_description/worlds/simple_robot_world.sdf), and [`gazebo_robot.launch.py`](src/robot_description/launch/gazebo_robot.launch.py). |
| 83 — Full System Architecture + Multi-Node Design | **Conceptual architecture review:** compare [`robot_description`](src/robot_description) and [`conveyor_system`](src/conveyor_system). There is no all-in-one Nav2/EKF/MoveIt/perception launch; see the [implemented boundaries](course_lectures/applied-practical-checkpoints.md#lecture-83-architecture-review-not-an-all-in-one-launch). |

## Build

Use Ubuntu 24.04 with ROS 2 Jazzy. From the repository root:

```bash
source /opt/ros/jazzy/setup.bash
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

The perception examples additionally need OpenCV, `cv_bridge`, Ultralytics and DeepSORT as applicable. Follow the [isolated Python environment and camera preflight](course_lectures/applied-practical-checkpoints.md#python-environment-and-image-preflight) rather than installing into Ubuntu’s managed system Python. YOLO weights download on first use and are intentionally not stored in Git.

## Test

Documentation checks require only Python 3 and Bash:

```bash
python3 scripts/check_course_docs.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

After building and sourcing on Ubuntu 24.04 with ROS 2 Jazzy, stop exercise nodes before running tests:

```bash
colcon test --packages-select conveyor_system lifecycle_demo my_first_pkg integration_demo robot_description
colcon test-result --verbose
```

Those focused tests cover conveyor/lifecycle behavior, parameter validation and model/configuration regressions, not the full robotics course. To inspect every package's available tests:

```bash
colcon test
colcon test-result --verbose
```

Report lint, dependency and functional failures separately. Then run the relevant [practical checkpoints](course_lectures/applied-practical-checkpoints.md#runtime-retest-checklist); a successful build or test collection does not prove Gazebo, Nav2 or perception works end-to-end. The [verification record](course_lectures/verification.md) distinguishes executed checks from pending runtime validation.

## Third-party course dependencies

Generated build outputs, local virtual environments, downloaded binary models, and third-party source checkouts are intentionally excluded. Install the ROS 2 Jazzy versions of Gazebo, Nav2, MoveIt 2, `ros_gz`, and `robot_localization` as introduced in the corresponding lectures.

The videos and quizzes remain on Udemy; this repository contains the supporting source code and lecture index.
