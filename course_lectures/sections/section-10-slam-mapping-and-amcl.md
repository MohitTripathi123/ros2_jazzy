# Section 10: Applied Robotics — SLAM, Mapping, Odometry and TF Reality Check

[Back to course index](../README.md)

## Lecture 55: SLAM Fundamentals

Understand simultaneous localization and mapping and the data required to build a map while estimating robot motion. Review the relationships among the `map`, `odom`, and `base_link` frames.

## Lecture 56: SLAM Implementation, Installation & Debugging

Install and run SLAM Toolbox with simulated time, odometry, TF, and LaserScan input. Diagnose missing scans, incorrect frames, lifecycle state, timing problems, and invalid parameters.

## Lecture 57: Mapping Deep Dive: Save Map + Quality

Drive the robot methodically, evaluate occupancy-grid quality, and save a completed map. Understand the generated image and YAML metadata and how motion, scan quality, and loop closure affect the result.

## Lecture 58: Odometry Deep Dive: Motion, TF & Reality Check

Inspect odometry messages and the `odom` to `base_link` transform while the robot moves. Understand accumulated drift, velocity estimates, timestamps, and the difference between odometry and global position.

## Lecture 59: Motion System Integration: Diff Drive + Bridges + TF + SLAM

Connect velocity commands, the Gazebo differential-drive plugin, odometry, ROS-GZ bridges, dynamic TF, LiDAR, and SLAM into one motion pipeline. Trace data in both command and feedback directions.

## Lecture 60: TF2 Deep Dive: Frame System

Study the full frame system used by mobile robots and navigation. Understand which component owns each transform and why a tree must have one consistent path between frames.

## Lecture 61: AMCL Localization: Concept + Setup

Use a saved map and Adaptive Monte Carlo Localization to estimate robot pose. Review particle-filter behavior, initial pose, scan matching, odometry input, map-server integration, and the `map` to `odom` transform.

