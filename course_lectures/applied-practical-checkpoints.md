# Applied robotics practical checkpoints

[Course index](README.md) · [Core ROS 2 checkpoints](core-practical-checkpoints.md) · [Verification record](verification.md)

These checks supplement the existing recordings; they do not add lectures or claim that every subsystem is launched together. The checked-in files are the final examples, not a saved version of every intermediate video step. All commands start in the repository root. Source ROS 2 and the workspace in **each terminal** using the [build instructions](../README.md#build). Run motion commands only in the course simulator, not on connected hardware. Stop one exercise before starting another that publishes the same topics.

A command starting successfully is not a passing checkpoint. Check messages, lifecycle state and visible behavior. Stop at a failed prerequisite rather than debugging a later layer.

## Lectures 40–54: model, simulation and sensors

**Prerequisites:** Ubuntu 24.04, ROS 2 Jazzy, Gazebo Harmonic, the built `robot_description` package, and a working graphical session for Gazebo/RViz. Install the corresponding Jazzy packages introduced in the course. In addition to `rosdep`, confirm these executables are available:

```bash
ros2 pkg prefix ros_gz_sim
ros2 pkg prefix ros_gz_bridge
ros2 pkg prefix robot_state_publisher
ros2 pkg prefix joint_state_publisher
ros2 pkg prefix tf2_ros
ros2 pkg prefix tf2_tools
command -v xacro
command -v gz
```

The package manifest does not yet list every launched dependency. If one is missing, install its Jazzy package before continuing; successful Python parsing does not install ROS packages.

### Model checks before launching

```bash
xacro src/robot_description/urdf/simple_robot.xacro > /tmp/course_robot.urdf
gz sdf -p /tmp/course_robot.urdf > /tmp/course_robot.sdf
```

Expect both commands to finish successfully with nonempty output. Inspect conversion warnings; an expanded URDF alone does not prove correct Gazebo physics or sensors.

| Lecture | File or activity | Check before continuing |
| --- | --- | --- |
| 40 | Phase 2 orientation | Explain how a working ROS graph differs from a working simulated robot. |
| 41 | [Simulation launch](../src/robot_description/launch/gazebo_robot.launch.py) | World opens, then one robot spawns. |
| 42 | [URDF](../src/robot_description/urdf/simple_robot.urdf) | Identify the root link and each parent/child joint. |
| 43 | [Xacro](../src/robot_description/urdf/simple_robot.xacro) | Identify left/right wheels and compare their origins with drive geometry. |
| 44 | Xacro expansion above | Generated URDF contains concrete links/joints rather than unresolved macros. |
| 45 | State publishers | `ros2 node list` includes the state publishers; distinguish joint-state input from TF output. |
| 46 | TF2 | `base_link` connects to the sensor frames; no competing parent for a child frame. |
| 47 | `ros2 run tf2_tools view_frames` | Inspect the generated graph; disconnected frames are a failure, not a cosmetic warning. |
| 48 | LiDAR definition | Identify model link, sensor frame and scan topic separately. |
| 49 | Camera/optical frame | Identify the optical-frame rotation; check the live image's `header.frame_id` rather than assuming it. |
| 50 | URDF-to-SDF conversion | Conversion succeeds and the robot remains physically stable after spawning. |
| 51 | Launch orchestration | Inspect `--show-args`; explain `spawn_delay` and `use_slam`. |
| 52 | [World](../src/robot_description/worlds/simple_robot_world.sdf) | Confirm the ground, walls, running physics and sensor rendering. |
| 53 | Scan bridge and RViz | `/scan` has messages and RViz can transform their frame into the selected fixed frame. |
| 54 | LaserScan | Inspect angle/range fields and relate an obstacle to its reported range. |

### Launch and inspect

Terminal A:

```bash
ros2 launch robot_description gazebo_robot.launch.py use_slam:=false
```

Terminal B, after the spawn completes:

```bash
ros2 node list
ros2 topic echo /clock --once
ros2 topic echo /odom --once
ros2 topic echo /scan --once --field header
ros2 topic echo /camera/image_raw --once --field header
ros2 run tf2_ros tf2_echo odom base_link
```

Stop continuous commands with Ctrl+C. Expected: advancing simulation time; odometry with `odom` and `base_link`; scan/image headers; an available `odom → base_link` transform. In RViz use `odom` as the fixed frame before mapping/localization supplies `map`.

If a topic exists but has no messages, inspect the actual Gazebo source and ROS bridge endpoints:

```bash
gz topic -l
gz topic -i -t /scan
gz topic -i -t /camera/image_raw
ros2 topic info /scan --verbose
ros2 topic info /camera/image_raw --verbose
```

Confirm the simulation is unpaused, the sensor plugin loaded and the topic/type matches on both sides. A topic name in `ros2 topic list` is not proof of data delivery.

### Motion prerequisite for mapping

Before mapping, demonstrate forward motion and turning at low speed in the simulator, then stop. Observe both the robot and `/odom`; a published command alone is insufficient.

**Current source caveat:** the model's DiffDrive configuration uses `<cmd_vel_topic>` while Gazebo Harmonic expects `<topic>`, and its `wheel_separation` is `0.4` despite wheel origins separated by `0.45` m. These pre-existing simulation issues are not repaired by this documentation update. Check the actual Gazebo command subscriber and geometry before declaring motion, odometry or downstream mapping verified. See the [verification record](verification.md). Do not compensate by increasing speed or assume Nav2 can repair a broken drive connection.

## Lectures 55–61: map first, then localize

**Prerequisites:** the simulation/sensor/motion checks above pass; SLAM Toolbox, `nav2_bringup`, and Nav2 map-server/AMCL packages are installed. The map is your generated exercise output, not a missing repository asset.

### Mapping mode: Lectures 55–60

Stop the earlier simulation, then start one simulation with SLAM enabled:

```bash
ros2 launch robot_description gazebo_robot.launch.py use_slam:=true
```

In a second sourced terminal:

```bash
ros2 lifecycle get /slam_toolbox
ros2 topic echo /map --once --qos-durability transient_local --field info
ros2 run tf2_ros tf2_echo map odom
```

Expect SLAM Toolbox to be `active`, an occupancy grid, and `map → odom`. If SLAM is unconfigured/inactive, inspect its launch logs and available transitions with `ros2 lifecycle list /slam_toolbox`. Fix the first failure; do not start another SLAM instance to hide it.

Drive the simulator through the area using the lecture's motion controls only after the motion prerequisite passes. In RViz set the fixed frame to `map` and inspect coverage, wall alignment and loop closure. Then save from the repository root:

```bash
ros2 run nav2_map_server map_saver_cli -f "$PWD/my_map" --ros-args -p use_sim_time:=true
ls -l my_map.yaml my_map.pgm
cat my_map.yaml
```

Expect the YAML and referenced image to exist; inspect their content and the map in RViz. Keep both together. The root-level `my_map.yaml` and `my_map.pgm` are intentionally ignored by Git.

| Lecture | Checkpoint |
| --- | --- |
| 55 | Explain why mapping needs scans, timestamps, odometry and a connected TF tree. |
| 56 | SLAM lifecycle is active and `/map` updates while exploring. |
| 57 | Save the map and verify both metadata and image; reject visibly doubled/distorted walls. |
| 58 | Observe odometry while driving and distinguish it from globally corrected pose. |
| 59 | Trace commands into Gazebo and scan/odom/TF back into ROS, with actual motion. |
| 60 | Identify the sole publisher responsible for each TF edge. |
| 61 | Complete the saved-map localization workflow below with one active AMCL instance and initialized pose. |

### Saved-map localization: Lecture 61

Stop the mapping launch and start simulation again with `use_slam:=false`. Do **not** run SLAM Toolbox and AMCL as competing publishers of `map → odom`.

Terminal A:

```bash
ros2 launch robot_description gazebo_robot.launch.py use_slam:=false
```

Terminal B, after simulation prerequisites pass:

```bash
test -f "$PWD/my_map.yaml" && test -f "$PWD/my_map.pgm"
ros2 launch nav2_bringup localization_launch.py \
  map:="$PWD/my_map.yaml" \
  params_file:="$PWD/src/robot_description/config/nav2_params.yaml" \
  use_sim_time:=true autostart:=true use_composition:=false
```

Use the YAML belonging to the same world you mapped. If the file check fails, stop and complete Lecture 57. `localization_launch.py` starts map-server/AMCL and their lifecycle manager; the repository's Gazebo launch alone does not.

Open RViz in another terminal:

```bash
ros2 run rviz2 rviz2 --ros-args -p use_sim_time:=true
```

Set fixed frame `map`, add the `/map` and `/scan` displays, and use **2D Pose Estimate** to supply the robot's approximate position and heading on the saved map. Then verify:

```bash
ros2 lifecycle get /map_server
ros2 lifecycle get /amcl
ros2 param get /amcl use_sim_time
ros2 topic echo /amcl_pose --once
ros2 run tf2_ros tf2_echo map base_link
```

**Pass checkpoint:** both lifecycle nodes active; simulation time enabled; an AMCL pose after initialization and scan processing; scans aligned with map walls; connected `map → odom → base_link`. Investigate missing map, initial pose, scans, TF or clock in that order before tuning AMCL.

## Lectures 62–68: Nav2 after localization

Complete Lecture 61 first. To test navigation, stop its standalone localization launch but keep the simulator running without SLAM. Start Nav2 bringup once, with the same saved map:

```bash
ros2 launch nav2_bringup bringup_launch.py \
  slam:=false map:="$PWD/my_map.yaml" \
  params_file:="$PWD/src/robot_description/config/nav2_params.yaml" \
  use_sim_time:=true autostart:=true use_composition:=false
```

Bringup starts localization again as well as navigation. Set the initial pose again in RViz. Do not leave the previous standalone AMCL instance running. The provided Nav2 configuration still requires runtime validation against the installed Jazzy plugins; do not interpret these launch instructions as an end-to-end certification.

| Lecture | Checkpoint |
| --- | --- |
| 62 | Use `ros2 lifecycle get /amcl`, `ros2 lifecycle get /planner_server` and `ros2 lifecycle get /controller_server`; resolve inactive/error states first. |
| 63 | Identify planner, controller, navigator and behavior-server roles using `ros2 node list`. |
| 64 | Inspect the actual configured planner/controller plugin names; A* and DWA explanations do not imply those exact plugins are selected. |
| 65 | Display local/global costmaps in RViz and check that observed obstacles are represented. |
| 66 | Inspect live values with `ros2 param dump /controller_server` and compare with [nav2_params.yaml](../src/robot_description/config/nav2_params.yaml). |
| 67 | Inspect the selected Nav2 behavior-tree resource in the installed package; it is not an authored XML file in this repository. |
| 68 | In simulation, observe a recovery scenario and its logs; confirm a subsequent valid goal can complete. |

Only send a nearby RViz navigation goal after TF, localization, costmaps and the drive command path pass. Stop the exercise if the robot does not follow the expected safe path.

## Lectures 69–73: odometry and the single-source EKF

[ekf.yaml](../src/robot_description/config/ekf.yaml) configures **one input: `odom0: /odom`**. There is no IMU input and no AMCL pose input. This is a single-source state-estimation exercise, not a demonstrated multi-sensor fusion or global-localization system. Selecting several fields from one odometry message does not create independent sensors or establish better accuracy. Review correlations and covariances before treating a configuration as production fusion.

The simulation launch does not start `robot_localization`. With one simulator running, `/odom` available, and the Jazzy `robot_localization` package installed, run the filter separately:

```bash
ros2 run robot_localization ekf_node --ros-args \
  --params-file "$PWD/src/robot_description/config/ekf.yaml" \
  -p use_sim_time:=true -p publish_tf:=false \
  -p odom_frame:=odom -p base_link_frame:=base_link -p world_frame:=odom
```

`publish_tf:=false` is deliberate for this comparison exercise: the Gazebo DiffDrive TF is already bridged into ROS and remains the owner of `odom → base_link`. The filter publishes `/odometry/filtered` for inspection without becoming a competing TF publisher. Do not feed that output back into the filter's `/odom` input.

In another terminal:

```bash
ros2 param get /ekf_filter_node odom0
ros2 param get /ekf_filter_node publish_tf
ros2 topic echo /odom --once
ros2 topic echo /odometry/filtered --once
ros2 topic hz /odometry/filtered
```

| Lecture | Checkpoint |
| --- | --- |
| 69 | Identify `map → odom` as SLAM **or** AMCL, and `odom → base_link` as the simulator in this exercise. |
| 70 | Explain why filtering relative odometry alone cannot anchor global position or eliminate drift. |
| 71 | Derive straight and turning motion from wheel radius and separation; compare against actual model geometry. |
| 72 | Compare input odometry position, orientation, velocity and timestamps while moving. |
| 73 | After input arrives, verify filtered output and frames; compare covariances, not just a smoother-looking trace. |

The configured output target is 30 Hz, not a guaranteed measured rate. If no filtered output arrives, check input messages, simulation clock, frame names and filter diagnostics. Replacing the simulator's TF with EKF ownership is a separate integration change, not required to finish this lesson.

## Lectures 74–77: external MoveIt 2 exercises

These lessons use the installed MoveIt 2 tutorial/demo from the recordings. No custom MoveIt robot package, controller integration or planning pipeline is implemented by this repository. Use the [official MoveIt tutorials](https://moveit.picknik.ai/main/index.html), selecting the installation/version suitable for ROS 2 Jazzy rather than mixing distributions.

| Lecture | Checkpoint in the chosen demo |
| --- | --- |
| 74 | Load the demo robot and planning scene in RViz without missing-model errors. |
| 75 | Request a reachable end-effector pose, then compare with an unreachable request. |
| 76 | Change joint values and explain the resulting end-effector pose. |
| 77 | Distinguish planning from execution; inspect a plan before running it in the tutorial's simulated system. |

## Lectures 78–82: camera-to-perception workflow

**Prerequisite order:** the camera and ROS-GZ bridge setup demonstrated in Lecture 82 is needed before running Lectures 78–81 against Gazebo. Use the simulation/sensor setup above first, then return to the published lecture order. You do not need Nav2 or the EKF for these image exercises.

The current Xacro sensor topic, ROS-GZ bridge and all four perception subscribers use **`/camera/image_raw`**. If a recording shows another name, inspect the live publisher and remap at launch; do not rename only one end of the connection.

### Python environment and image preflight

OpenCV examples require a graphical session because they use `cv2.imshow`. YOLO also needs its Python dependencies and downloads weights on first use (`yolov8n.pt` for detection; `yolov8m.pt` for tracking/counting). A first model download may take time and requires network access. Neither downloaded weights nor a virtual environment belong in Git.

For YOLO/DeepSORT, use an isolated environment with access to the ROS system packages, created with Ubuntu's system Python. Install `python3-venv` first if needed:

```bash
/usr/bin/python3 -m venv --system-site-packages yolovenv
source yolovenv/bin/activate
python3 -m pip install ultralytics deep-sort-realtime
python3 -c "import rclpy, cv_bridge, cv2; from ultralytics import YOLO; from deep_sort_realtime.deepsort_tracker import DeepSort; print('Imports OK')"
```

Source ROS/workspace as described above in this terminal too. If the import check reports a NumPy/OpenCV binary-compatibility error, resolve that environment conflict before continuing. Do not bypass an externally-managed-system-Python warning with `sudo pip` or `--break-system-packages`. The commands below use the active environment's `python3` explicitly; an already-built `ros2 run` wrapper can still point to the Python interpreter used at build time.

Start one simulator without SLAM if none is running. Before starting a perception node:

```bash
ros2 topic info /camera/image_raw --verbose
ros2 topic echo /camera/image_raw --once --field header
ros2 topic hz /camera/image_raw
```

Expect an image publisher, delivered frames and increasing timestamps. Stop `hz` with Ctrl+C. Missing frames are a sensor/bridge problem to resolve before investigating a model. If frames exist but a node receives nothing, inspect QoS compatibility: these subscribers request reliable delivery.

### Run one lesson at a time

Keep the simulator running. Choose **one** command; stop that node before starting the next:

```bash
# Lecture 78: grayscale OpenCV window
python3 src/image_processing/image_processing/image_node.py
```

```bash
# Lecture 79: YOLO detections
python3 src/yolo_detection/yolo_detection/yolo_node.py
```

```bash
# Lecture 80: confirmed track IDs
python3 src/object_tracking/object_tracking/tracking_node.py
```

```bash
# Lecture 81: annotated image and crossing events
python3 src/object_counting/object_counting/counting_node.py
```

If your camera publishes `/image_raw` instead, for example, remap the expected input on the command being run:

```bash
python3 src/image_processing/image_processing/image_node.py --ros-args \
  -r /camera/image_raw:=/image_raw
```

Use that only when `/image_raw` is an actual verified publisher. The Gazebo workflow above does not need this remap.

| Lecture | Pass checkpoint |
| --- | --- |
| 78 | The grayscale window updates when the camera view changes. |
| 79 | A recognizable object produces a detection, confidence and bounding box. A blank scene is not a detector test. |
| 80 | A confirmed track retains its ID across consecutive frames while the object stays visible; reacquisition is not guaranteed to retain an ID. |
| 81 | A confirmed track crossing from `y <= 250` to `y > 250` increments the count once. Merely appearing below the line or crossing upward does not count. Inspect `/object_counting/image`. |
| 82 | Trace the real camera frame from Gazebo through the bridge to the selected node, alongside clock, scan, odometry and TF checks. |

The simple course world does not guarantee recognizable moving YOLO objects. Use the lecture's suitable scene/camera input before calling detection, tracking or counting verified. Each detection/tracking/counting example currently consumes the camera independently and performs its own inference; they are not a chain of detection-message producer/consumers. Counting publishes an annotated image and logs a total, not a structured count message or a navigation command.

## Lecture 83: architecture review, not an all-in-one launch

Use the actual launch files and ROS graph to distinguish implemented paths from design discussion:

- `conveyor_system.launch.py` launches the conveyor teaching system. Its safety supervisor publishes alerts; an alert is not automatically a physical emergency stop.
- `gazebo_robot.launch.py` launches simulation, state publishers, bridges and optional SLAM. It does **not** launch Nav2, the EKF, MoveIt 2 or perception.
- Nav2/AMCL and the EKF are started separately in the exercises above.
- The perception examples are independent camera consumers. No perception-to-navigation decision node or combined navigation/manipulation application is supplied.

**Completion checkpoint:** sketch node responsibilities, topic/service/action connections, TF ownership and the startup prerequisites from the systems you actually ran. Mark proposed connections as proposed. Explain where a missing sensor, inactive lifecycle node or mismatched topic would interrupt data flow. This completes the architecture lesson without inventing an additional project or claiming an integrated application that is not present.

## Runtime retest checklist

On Ubuntu/Jazzy, run the [build and regression commands](../README.md#test), then repeat the affected checkpoints. Record failures rather than skipping them:

1. Lifecycle publication only while active, repeated activation/cleanup, conveyor default launch and modes.
2. Simulation spawn, physics, live clock/scan/camera/odom/TF and verified command-to-motion flow.
3. Save map, restart without SLAM, initialize AMCL and verify localization before navigation goals.
4. One-source EKF output with no duplicate TF ownership.
5. Real image delivery, OpenCV display, detections, stable tracks and one downward-crossing event.

See [verification.md](verification.md) for what was actually checked during this update, as distinct from this checklist.
