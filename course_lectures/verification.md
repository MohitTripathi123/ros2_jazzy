# Course companion verification

[Course index](README.md) · [Core checkpoints](core-practical-checkpoints.md) · [Applied checkpoints](applied-practical-checkpoints.md)

Checked on 2026-11-13. The review branch `docs/course-practical-checkpoints` builds on conveyor/lifecycle fix commit `07461268bcaf61b7d746c6dc898bd21909e4bf3a`. The companion update changes documentation and its validation scripts, not ROS node behavior, configuration values, models or recordings. Main has not been merged or updated by this work.

## Executed checks

- **Passed:** documentation validator across 20 Markdown files and 91 Bash blocks: local links/headings, preserved lecture coverage, shell syntax and repository-owned command targets.
- **Passed:** four unit tests for the validator, including deliberately broken links, command names and shell syntax.
- **Passed:** compilation of 88 Python/snippet files, parsing of 17 XML files and four YAML files.
- **Passed:** source checks confirm the camera topic agrees across Xacro, bridge and all four subscribers, and the EKF uses one `/odom` input.
- **Passed:** Xacro expansion to parseable URDF. Gazebo conversion/physics were not run.
- **Passed:** new validation-script lint (`flake8 scripts --max-line-length 119`), focused source syntax/name lint (`E9,F63,F7,F82`), and Git whitespace checks. This is not a full repository style pass.
- **Blocked by environment:** a fresh `colcon build` attempt stopped at `conveyor_interfaces` because `ament_cmake` is unavailable: zero packages finished, one failed, 13 unprocessed. This does not establish a build failure on a correctly installed Jazzy machine.
- **Blocked at collection:** the three existing conveyor/lifecycle runtime test files could not import generated `conveyor_interfaces`, `lifecycle_msgs` and `rclpy`. No ROS runtime test executed; three collection errors are not passing tests.

No external-link availability, ROS runtime, simulator, model inference or end-to-end pass is claimed. Shell syntax checking does not validate the behavior of an installed ROS executable.

## Environment and runtime limits

The available executor is Debian 13 without ROS 2 Jazzy, Gazebo or a container runtime. Documentation checks, source parsing and Xacro expansion cannot substitute for DDS communication, lifecycle transitions or simulation. Runtime regression tests require a provisioned Ubuntu 24.04/Jazzy environment with generated interfaces. Nav2, AMCL, SLAM, EKF, MoveIt, image display, YOLO and DeepSORT behavior must be checked there.

Use the [test commands](../README.md#test) and the [runtime retest checklist](applied-practical-checkpoints.md#runtime-retest-checklist). Record the exact commit, platform and observed results when completing that verification.

## Known pre-existing limits preserved for review

This is a focused course-companion update, not a claim that all earlier source issues are fixed:

- The Gazebo DiffDrive block uses `cmd_vel_topic`, while Harmonic's plugin reads `topic`. Check its actual command subscriber before calling the motion path functional. [Harmonic plugin source](https://github.com/gazebosim/gz-sim/blob/gz-sim8/src/systems/diff_drive/DiffDrive.cc).
- Wheel origins are at `y = ±0.225` m, but the drive configuration specifies `wheel_separation = 0.4` m. Motion/odometry verification must resolve this discrepancy.
- The conveyor sensor uses a fixed one-second timer; its YAML `publish_rate` is unused. Supported thresholds/speeds are generally startup values, not validated live tuning controls.
- Some package manifests omit directly used runtime dependencies. `rosdep` alone therefore does not establish that all launch/CLI prerequisites are installed.
- The Gazebo launch does not launch Nav2, EKF, MoveIt or perception. The EKF has one `/odom` input; perception examples run independently. Architecture integration discussed in the last lecture is not an implemented combined application.

These limitations are exposed in the practical companions where they affect a checkpoint. They were not silently changed or presented as passing tests.
