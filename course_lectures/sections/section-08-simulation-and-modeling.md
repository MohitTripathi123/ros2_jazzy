# Section 8: Applied Robotics — Simulation Workflow, URDF, Xacro and Robot Modeling

[Back to course index](../README.md) · [Practical commands and checkpoints](../applied-practical-checkpoints.md)

## Lecture 40: Before You Start Phase 2: Moving from Core ROS 2 to Applied Robotics

Transition from isolated ROS 2 examples to complete robotic systems. Review the tools, mental models, and debugging discipline needed for simulation, sensing, navigation, manipulation, and perception.

## Lecture 41: Simulation Workflow & Gazebo Introduction

Understand the simulation workflow from robot description and world definition to spawning, bridging, visualization, and control. Learn the responsibilities of Gazebo, ROS 2 nodes, and the ROS-GZ bridge.

## Lecture 42: Understanding Robot Description with URDF

Describe a robot with URDF links and joints. Build visual, collision, and inertial models and understand how the resulting kinematic tree represents the physical structure.

## Lecture 43: Building a Differential Drive Robot Model

Model a mobile base with left and right continuous wheel joints and caster support. Define wheel dimensions, separation, joint axes, origins, mass, and inertia.

## Lecture 44: XACRO: Writing Clean and Reusable Robot Models

Replace repeated URDF blocks with Xacro properties and macros. Generate wheels from one reusable definition and keep dimensions consistent throughout the model.

## Lecture 45: Understanding robot_state_publisher and joint_state_publisher

Publish the robot's link transforms from its description and joint positions. Understand the distinct roles of `robot_state_publisher` and `joint_state_publisher` in producing a complete TF tree.

## Lecture 46: TF2: Understanding Frames and Transforms

Learn how coordinate frames express the position and orientation of robot components. Follow transforms through the robot tree and understand parent-child relationships, timestamps, and frame naming.

## Lecture 47: TF Debugging: view_frames and Real Issues

Inspect the live TF tree and export a frame graph with `view_frames`. Diagnose disconnected trees, duplicate publishers, incorrect parents, missing transforms, stale timestamps, and naming mismatches.

## Lecture 48: Adding a LiDAR Sensor: Robot Model vs Real Sensor

Add a LiDAR link, joint, collision model, and Gazebo sensor configuration. Distinguish the physical sensor mount, ROS frame, Gazebo sensor entity, and resulting LaserScan topic.

## Lecture 49: Adding Camera Sensor & Understanding Optical Frame

Add a simulated RGB camera and define its optical frame. Understand camera image settings and the standard optical-frame orientation required by ROS perception tools.

## Lecture 50: Visual, Collision, Inertial and Spawning Robot in Gazebo

Review the three essential physical representations in a robot model and convert the Xacro-generated URDF into SDF. Spawn the resulting model into a running Gazebo world.

## Lecture 51: Launch Files for Robot Simulation System

Coordinate robot-description generation, Gazebo startup, robot spawning, state publishing, bridges, and supporting processes from one Python launch file. Use delays and event handlers where startup order matters.

## Lecture 52: Gazebo World, Physics and Ground Plane

Create an SDF world containing physics, sensor, scene, and user-command systems. Add lighting, a ground plane, and static walls with collision and visual geometry.

