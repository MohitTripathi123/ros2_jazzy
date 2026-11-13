# Course verification

[Course index](README.md) · [Core checkpoints](core-practical-checkpoints.md) · [Applied checkpoints](applied-practical-checkpoints.md)

Checked on 2026-11-13. This record replaces the earlier documentation-only report. The conveyor/lifecycle and course-companion work was merged into main at `67d20a94dfd11b538d337cc0ee300c81b35620b1`; the `fix/main-retest-findings` changes below were built and tested from that base. The recordings, all 83 lecture descriptions and course scope remain unchanged.

## Fixes validated

- Parameter examples reject non-double, non-finite and out-of-range speeds, including startup overrides. Integration reads the committed parameter for each publication without a duplicate cache; rejected atomic batches leave published speed unchanged.
- Gazebo DiffDrive is configured to receive the bridged `/cmd_vel` topic. Wheel separation and radius come from the same Xacro properties as the geometry. CameraInfo has an explicit topic matching its bridge.
- Both Nav2 costmaps use a 0.33 m robot radius. Model-derived regression checks confirm it encloses the collision geometry; the body corners alone require about 0.3202 m.
- Integer-form speed launch arguments such as `robot_speed:=3` are explicitly converted to doubles; invalid, non-finite and out-of-range launch values fail.
- Documented standalone localization and Nav2 commands use the Python-compatible `False` arguments. The repository's own `use_slam:=false` remains valid.
- Conveyor `publish_rate` now sets the actual timer at startup, rejects non-finite/nonpositive rates and timer-period overflow/underflow and rejects changes after startup rather than claiming to change the timer.
- Missing direct ROS/OpenCV runtime dependencies were added to package manifests. Ultralytics/DeepSORT still follow the documented separate Python-environment setup.
- Existing Python lint failures were corrected without changing unrelated example behavior.

## Executed checks on the fixes

- **Build passed:** all 14 packages, clean build/install directories.
- **Complete repository suite passed:** `colcon test-result` reports **135 tests, 0 errors, 0 failures, 11 skipped**. Counts include CTest/xUnit aggregation. The skipped checks are the existing copyright placeholders, not silently skipped runtime failures.
- **All seven earlier conveyor/lifecycle regressions passed.**
- **77 new regression cases passed:** 61 real-rclpy/launch parameter cases (including parameter services over DDS and velocity publication), nine sensor-rate cases (including timed DDS output and extreme-rate rejection), and seven model/config/documentation checks (including real Xacro and SDF conversion).
- **Core process checks passed:** node discovery, approximately 1 Hz pub/sub, AddTwoInts client/server, Fibonacci feedback/result, finite parameter changes and rejection, launch namespaces/conditions/overrides, callback blocking, QoS compatibility, and clean shutdown. Offscreen Turtlesim movement and concurrent callbacks were observed.
- **Localization/Nav2 passed with synthetic inputs:** corrected standalone map-server/AMCL startup; 12 Nav2 lifecycle nodes active; map, AMCL poses and connected TF; successful 38-pose path to (1, 0); successful navigation action at the current pose. These are startup/planning/action checks, not driven-motion tests.
- **Actual perception inference passed:** three pixel-exact grayscale frames; five YOLOv8n frames with six detections each; YOLOv8m/DeepSORT IDs 1–5 confirmed and stable; five static counting frames at zero; a 16-frame synthetic downward crossing increments the unchanged `y=250` line count once and remains one. Counting image headers are preserved. Real OpenCV display calls ran with offscreen Qt.
- **Documentation/static checks passed:** 20 Markdown files, 91 Bash blocks, local links/headings, lecture coverage, command targets, four validator tests, 91 Python/snippet compilations, 17 XML parses and four YAML parses. Git whitespace checks passed.

## Environment

Real ROS 2 Jazzy from RoboStack/conda-forge on Debian 13 x86_64, Python 3.12.16: rclpy 7.1.12, Gazebo Harmonic 8.10.0, Nav2 1.3.13, SLAM Toolbox 2.8.5, robot_localization 3.8.3 and cv_bridge 4.1.0. The build used setuptools 79.0.1 for colcon compatibility.

Perception used CPU PyTorch 2.15.0, torchvision 0.29.2, Ultralytics 8.4.212, DeepSORT 1.3.2, NumPy 2.5.4 and OpenCV 5.0.0, with cached official model weights and a prerecorded sample image. Model and tracker inference were not mocked. These versions record the test environment; they are not a claim that every newer dependency resolution is compatible.

This is not a native Ubuntu 24.04 setup certification. Use the [normal build and test instructions](../README.md#build) on the course's supported Ubuntu/Jazzy setup.

## Remaining runtime limits

The preceding main-branch retest attempted the actual Gazebo launch. It aborted before physics in ZeroMQ transport with `Operation not permitted (src/ip_resolver.cpp:542)` / `getifaddrs`. That environment restriction was not bypassed. SDF conversion/validation and corrected configuration cannot substitute for a running simulator.

Still required on a suitable host:

1. Observe forward/turn/stop motion and wheel odometry with the corrected drive connection.
2. Verify actual lidar, camera, CameraInfo and clock delivery through the bridges.
3. Map while moving, save/reload that map, localize, then navigate a nonzero distance with obstacles and recovery.
4. Check visible RViz/OpenCV/RQt workflows, localization accuracy and live-camera perception.
5. Validate physical hardware separately; conveyor alerts are monitoring output, not a certified emergency stop.

The earlier base-commit retest separately verified unchanged EKF parameters at about 30 Hz, SLAM activation/map production and map saving using synthetic input. It did not prove a Gazebo mapping-to-navigation workflow. Perception checks use a prerecorded photo with synthetic motion, not a general accuracy benchmark.

The Gazebo launch still intentionally does not launch Nav2, EKF, MoveIt or perception together. EKF has one `/odom` input; perception examples run independently. MoveIt material uses conceptual/external exercises rather than a repository-specific integrated configuration. These are course boundaries, not claims of an implemented all-in-one system.

After changes, rerun the [tests](../README.md#test) and the [runtime checklist](applied-practical-checkpoints.md#runtime-retest-checklist). Keep passed, failed and environment-blocked stages separate.
