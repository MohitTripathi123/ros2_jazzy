# Section 12: Applied Robotics — Robot Motion, Odometry, Localization and EKF

[Back to course index](../README.md) · [Practical commands and checkpoints](../applied-practical-checkpoints.md)

## Lecture 69: TF Tree Deep Dive: map → odom → base_link

Analyze the standard mobile-robot TF chain and the responsibility of each transform. Understand how global localization corrects drift without breaking the locally continuous odometry frame.

## Lecture 70: Odometry vs Localization: Fusion Concept

Separate relative motion estimation from global pose estimation. Learn why wheel odometry is smooth but drifts, why localization is globally anchored, and how a fused system benefits from both.

## Lecture 71: Robot Kinematics: Differential Drive

Relate left and right wheel velocities to robot linear and angular velocity. Examine straight motion, turning in place, arcs, wheel separation, wheel radius, and nonholonomic constraints.

## Lecture 72: Odometry Computation from Wheels

Integrate wheel motion over time to update planar position and heading. Understand encoder increments, wheel distances, midpoint motion, coordinate transformation, and sources of accumulated error.

## Lecture 73: EKF: Extended Kalman Filter Introduction

Introduce state estimation with prediction and measurement updates. Configure `robot_localization` for 2D motion and select which measurement fields enter the filter. The checked-in example has one `/odom` source, not multiple independent sensors or an AMCL input. Run it separately from the simulation with TF publication disabled for the comparison exercise, as shown in the practical companion.

