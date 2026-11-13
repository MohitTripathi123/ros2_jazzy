# Section 15: Applied Robotics — Full Robotics System Integration and Multi-Node Design

[Back to course index](../README.md) · [Practical commands and checkpoints](../applied-practical-checkpoints.md)

## Lecture 82: Simulation + Full Integration: Gazebo Sim + ROS-GZ Bridge

Bring together the Gazebo world, robot model, differential drive, simulated sensors, clock, TF, and bidirectional ROS-GZ bridges. Verify command flow into simulation and sensor feedback into ROS 2. Its camera/bridge setup is also a runtime prerequisite for Lectures 78–81; the practical companion makes that dependency explicit.

## Lecture 83: Full System Architecture + Multi-Node Design

Review the complete robotics system as cooperating nodes with explicit responsibilities and interfaces. Apply modular design, lifecycle management, QoS, configuration, observability, failure handling, and systematic integration testing.


This final lesson is a conceptual architecture review. The repository provides separate conveyor and simulation examples, optional SLAM, separate Nav2/EKF configurations, and independent perception nodes. It does not provide an all-in-one launch or a perception-to-navigation/manipulation decision layer. Mark proposed integrations as proposed rather than treating them as implemented.
