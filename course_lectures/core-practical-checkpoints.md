# Core ROS 2 practical checkpoints: Lectures 3–39

[Course index](README.md) · [Repository setup and build](../README.md#build)

These are runnable companions to the existing lectures, not replacement recordings or new curriculum. **The source is the final integrated snapshot, not a checkout for each video.** In particular, conveyor mode delivery, threshold handling, lifecycle activation/cleanup, and startup STOP behavior include later fixes. Read the named source alongside the video when behavior differs.

## Before each exercise

Use Ubuntu 24.04, ROS 2 Jazzy, and a built workspace as described in the repository README. Turtlesim and RQt exercises additionally need the installed Jazzy `turtlesim` and `rqt_graph` packages and a graphical desktop. Use separate terminals for long-running nodes and inspection commands. **Run every command below from the repository root**, sourcing each new terminal:

```bash
source /opt/ros/jazzy/setup.bash
source install/setup.bash
```

Stop previous exercises with Ctrl+C before starting a new one. Keep all exercise terminals on the same `ROS_DOMAIN_ID`; do not use a domain connected to real hardware. All movement, deliberate faults, and conveyor commands here are **simulation-only**. A topic message or a shutdown log is not proof that physical machinery has stopped.

Each checkpoint describes expected behavior from the source. It is not a claim that these commands have passed runtime testing on your computer. If a package/executable/type is missing, build its package and dependencies, then source the overlay again. If nodes exist but data does not arrive, check names, discovery/domain, and QoS before changing code.

## Setup and first communication (3–12)

### Lecture 3 — Verify Jazzy

After the installation shown in the lecture:

```bash
source /opt/ros/jazzy/setup.bash
printenv ROS_DISTRO
ros2 --help
python3 -c 'import rclpy; print(rclpy.__file__)'
```

**Check:** distro is `jazzy`, CLI help appears, and Python imports `rclpy`. A missing command/import usually means installation or sourcing is incomplete; do not diagnose this as a course-node bug.

### Lecture 4 — Verify the editor environment

With VS Code installed as shown in the lecture:

```bash
code .
```

Open [publisher_node.py](../src/my_first_pkg/my_first_pkg/publisher_node.py). In the editor's integrated terminal, run the Lecture 3 commands and source `install/setup.bash`. **Check:** the same ROS/Python environment works there. If the terminal works but the editor reports unresolved imports, inspect the editor's selected Python interpreter. Editor configuration is local, not a repository deliverable.

### Lecture 5 — Inspect package structure without overwriting it

The package-creation exercise is already represented by [my_first_pkg](../src/my_first_pkg):

```bash
ls src/my_first_pkg
cat src/my_first_pkg/package.xml
sed -n '/entry_points/,$p' src/my_first_pkg/setup.py
```

**Check:** identify the manifest, module, resource marker, tests, and `console_scripts`. Do not run `ros2 pkg create my_first_pkg` over this existing directory. For package creation practice, use a separate scratch workspace as in the recording.

### Lecture 6 — Build and discover an executable

After the README's dependency setup:

```bash
colcon build --symlink-install --packages-up-to my_first_pkg
source install/setup.bash
ros2 pkg prefix my_first_pkg
ros2 pkg executables my_first_pkg
```

**Check:** the prefix is this workspace's install space and `publisher_node` is listed. A prefix from another workspace indicates overlay/source order, not missing source. `build/`, `install/`, and `log/` are generated outputs.

### Lecture 7 — First node

```bash
python3 src/my_first_pkg/my_first_pkg/simple_node.txt
```

In another terminal:

```bash
ros2 node list
ros2 node info /simple_node
```

**Check:** one greeting, followed by a spinning `/simple_node`. The `.txt` file is a Python teaching snippet, not an installed executable. Silence after the greeting is expected; stop it with Ctrl+C.

### Lecture 8 — Publisher

```bash
ros2 run my_first_pkg publisher_node
```

In another terminal:

```bash
ros2 topic echo /hello_topic std_msgs/msg/String --once
```

**Check:** `data: Hello from ROS 2`; the source timer is one second. See [publisher_node.py](../src/my_first_pkg/my_first_pkg/publisher_node.py).

### Lecture 9 — Subscriber

Keep the Lecture 8 publisher running; in another terminal:

```bash
ros2 run my_first_pkg subscriber_node
```

**Check:** repeated `Received: Hello from ROS 2`. The executable is `subscriber_node`, but the source's node name is spelled `/subsriber_node`. Use that spelling for `ros2 node info`; do not mistake it for a second implementation.

### Lecture 10 — Topic inspection and injection

With Lectures 8–9 running:

```bash
ros2 topic list -t
ros2 topic info /hello_topic --verbose
ros2 topic hz /hello_topic
```

Stop only the `hz` command with Ctrl+C, then:

```bash
ros2 topic pub --once /hello_topic std_msgs/msg/String "{data: 'CLI checkpoint'}"
```

**Check:** approximately 1 Hz before injection, compatible String endpoints, and the subscriber receives `CLI checkpoint`. Measurements vary with scheduling; two publishers change the measured frequency.

### Lecture 11 — Service request and response

```bash
ros2 run my_first_pkg add_two_ints_server
```

In another terminal:

```bash
ros2 run my_first_pkg add_two_ints_client
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts '{a: 4, b: 5}'
```

**Check:** the client prints `7 + 3 = 10`; the CLI response is `sum: 9`. A client repeatedly waiting means the server is absent or undiscovered. Sources: [server](../src/my_first_pkg/my_first_pkg/add_two_ints_server.py), [client](../src/my_first_pkg/my_first_pkg/add_two_ints_client.py).

### Lecture 12 — Action interface, feedback, and result

```bash
ros2 interface show my_first_interfaces/action/Fibonacci
ros2 run my_first_pkg fibonacci_action_server
```

In another terminal:

```bash
ros2 action list -t
ros2 action send_goal /fibonacci my_first_interfaces/action/Fibonacci '{order: 6}' --feedback
```

**Check:** feedback grows and the successful result is `[0, 1, 1, 2, 3, 5]`. The server deliberately sleeps between iterations. The generated type comes from [my_first_interfaces](../src/my_first_interfaces/action/Fibonacci.action), not the duplicate teaching file under `my_first_pkg/action`. This minimal server does not demonstrate validated orders or a complete cancellation policy.

## Parameters, launch, and integration (13–22)

### Lecture 13 — Parameter storage versus behavior

```bash
ros2 run my_first_pkg parameter_example
```

In another terminal:

```bash
ros2 param get /parameter_example robot_speed
ros2 param set /parameter_example robot_speed 2.5
ros2 param get /parameter_example robot_speed
```

**Check:** `1.0`, successful update, then `2.5`. [This node](../src/my_first_pkg/my_first_pkg/parameter_example.py) reads/logs speed only at startup; changing the stored parameter does not produce motion or a periodic updated log.

### Lecture 14 — Reject invalid parameter values

Stop Lecture 13 and run:

```bash
ros2 run my_first_pkg parameter_callback_example
```

In another terminal:

```bash
ros2 param set /parameter_callback_example robot_speed 2.5
ros2 param set /parameter_callback_example robot_speed 6.0
ros2 param set /parameter_callback_example robot_speed 2
ros2 param get /parameter_callback_example robot_speed
```

**Check:** `2.5` is accepted; out-of-range and integer values are rejected; stored value remains `2.5`. Use decimals for this declared double. Inspect [validation](../src/my_first_pkg/my_first_pkg/parameter_callback_example.py), rather than treating every error as a range error.

### Lecture 15 — Start a launch description

Stop standalone parameter nodes:

```bash
ros2 launch my_first_pkg multi_node_launch.py
```

In another terminal:

```bash
ros2 node list
ros2 param get /robot1/parameter_node robot_speed
```

**Check:** `/robot1/parameter_node` and `/robot1/callback_node`, with speed `2.0`. These are parameter examples, not the earlier talker/listener pair.

### Lecture 16 — Launch arguments

Stop the previous launch before restarting:

```bash
ros2 launch my_first_pkg multi_node_launch.py --show-args
ros2 launch my_first_pkg multi_node_launch.py robot_speed:=3.0
```

Query `ros2 param get /robot1/parameter_node robot_speed` in another terminal. **Check:** `3.0`. Keep `use_sim_time` false here; these exercises provide no `/clock` publisher.

### Lecture 17 — Namespace and condition

Stop the launch, then:

```bash
ros2 launch my_first_pkg multi_node_launch.py enable_callback:=false
```

In another terminal, run `ros2 node list`. **Check:** `/robot1/parameter_node` exists and `/robot1/callback_node` does not. [The final launch file](../src/my_first_pkg/launch/multi_node_launch.py) uses node namespaces and `IfCondition`; it imports `GroupAction` but does not actually construct a group. Distinguish the lecture's grouping concept from this committed implementation.

### Lecture 18 — Inspect the actual graph

With Lecture 17 running:

```bash
ros2 node info /robot1/parameter_node
ros2 param list /robot1/parameter_node
ros2 service list -t
ros2 interface show rcl_interfaces/srv/GetParameters
```

**Check:** parameter services and `robot_speed` appear. Services are not all authored application services; ROS exposes node parameter services too. No `/fibonacci` action is expected after stopping its server.

### Lecture 19 — Integrated velocity publisher

Stop the earlier launch:

```bash
ros2 launch integration_demo integration_launch.py
```

In another terminal:

```bash
ros2 topic echo /robot1/velocity std_msgs/msg/Float32 --once
ros2 param set /robot1/velocity_publisher robot_speed 3.5
ros2 topic echo /robot1/velocity std_msgs/msg/Float32 --once
ros2 param set /robot1/velocity_publisher robot_speed 11.0
```

**Check:** initial `1.0`, then `3.5`, with `11.0` rejected. This is a Float32 demonstration, not a motor driver or Twist controller. [Source](../src/integration_demo/integration_demo/velocity_publisher.py) validates before commit and reads the committed parameter for each publication, so a rejected change cannot alter its output.

### Lecture 20 — Verify installed resources

```bash
ros2 pkg executables integration_demo
ls "$(ros2 pkg prefix integration_demo)/share/integration_demo/launch"
ls "$(ros2 pkg prefix integration_demo)/share/integration_demo/config"
```

**Check:** executable, launch file, and `params.yaml` are installed. Compare [setup.py](../src/integration_demo/setup.py) and [package.xml](../src/integration_demo/package.xml) to the source directories. A file existing in `src/` alone does not prove launch can find it in the installed package.

### Lecture 21 — Visualize the graph

With Lecture 19 running:

```bash
ros2 node info /robot1/velocity_publisher
ros2 topic info /robot1/velocity --verbose
ros2 run rqt_graph rqt_graph
```

**Check:** a publisher on `/robot1/velocity`. Run a continuous `ros2 topic echo /robot1/velocity` in another terminal to add a subscriber; adjust RQt filters if leaf topics/CLI nodes are hidden. This example has no TF publishers; an empty TF graph is not a velocity failure.

### Lecture 22 — YAML matching and override order

Stop the integration launch. Run the executable using only YAML:

```bash
ros2 run integration_demo velocity_publisher --ros-args -r __ns:=/robot1 --params-file src/integration_demo/config/params.yaml
```

In another terminal:

```bash
ros2 param get /robot1/velocity_publisher robot_speed
```

**Check:** `5.5` from [params.yaml](../src/integration_demo/config/params.yaml). Stop this node and run `ros2 launch integration_demo integration_launch.py robot_speed:=2.5`; the same query should give `2.5`. The [launch file](../src/integration_demo/launch/integration_launch.py) places its explicit override after YAML; even its default `1.0` overrides YAML's `5.5`. Do not expect editing YAML alone to win over that override.

## Execution, QoS, and lifecycle (23–30)

### Lecture 23 — Observe blocking

```bash
ros2 run runtime_demo execution_demo
```

**Check:** Timer 1 sleeps for five seconds; Timer 2 cannot fire during that callback on the single-threaded executor. Its configured two-second period is not a guaranteed execution interval. Inspect [execution_demo.py](../src/runtime_demo/runtime_demo/execution_demo.py). Stop before proceeding.

### Lecture 24 — Visualize callbacks in Turtlesim

```bash
ros2 run turtlesim turtlesim_node
```

In another terminal:

```bash
ros2 run turtle_runtime_demo turtle_control
```

**Check:** forward motion and logs naming callback threads. The final [turtle_control.py](../src/turtle_runtime_demo/turtle_runtime_demo/turtle_control.py) already uses two executor threads and a reentrant group; it is not the single-threaded stage of the recording. Motion may pause under load or reach the window edge; inspect `ros2 topic hz /turtle1/cmd_vel` rather than assuming every visual pause proves a QoS fault.

### Lecture 25 — Multi-threaded execution

Keep Lecture 24 running. Read the executor construction:

```bash
grep -n -E 'Executor|callback_group|sleep' src/turtle_runtime_demo/turtle_runtime_demo/turtle_control.py
ros2 topic hz /turtle1/cmd_vel
```

**Check:** movement callbacks can run while a heavy callback sleeps, unlike Lecture 23. Two threads do not guarantee exact 1 Hz under overlapping heavy callbacks. The later [conveyor controller](../src/conveyor_system/conveyor_system/control_node.py) also uses `MultiThreadedExecutor`; its functional checkpoint is Lecture 34.

### Lecture 26 — Callback groups and shared state

```bash
grep -n -E 'Reentrant|callback_group|Lock|with self._command_lock' src/conveyor_system/conveyor_system/control_node.py
```

**Check:** both subscriptions share a reentrant group, but a lock serializes state update plus command publication. A reentrant group permits concurrency; it does not create threads or protect state. Repeat Lecture 35's STOP check while sensor input is arriving to exercise the integrated design. A successful manual run alone is not proof of race freedom.

### Lecture 27 — Match QoS explicitly

Stop turtle control. Run:

```bash
ros2 run qos_demo qos_test
```

In another terminal:

```bash
ros2 topic info /qos_topic --verbose
ros2 topic echo /qos_topic std_msgs/msg/String --qos-reliability best_effort --qos-durability transient_local
```

**Check:** increasing count messages, best-effort/transient-local publisher with depth 10. For a deliberate incompatible subscriber, stop the echo and run:

```bash
ros2 topic echo /qos_topic std_msgs/msg/String --qos-reliability reliable --qos-durability transient_local
```

**Check:** no matching delivery, usually with a QoS incompatibility warning. Best-effort cannot satisfy a reliable request. Do not rely on implicit CLI QoS defaults to demonstrate this distinction. Transient-local history belongs to the living publisher; it is not disk persistence.

### Lecture 28 — Fault and shutdown observation

Stop `turtle_control` and the QoS publisher. Keep or restart Turtlesim. Before starting the demo, monitor in another terminal:

```bash
ros2 topic echo /turtle1/cmd_vel geometry_msgs/msg/Twist
```

Then:

```bash
ros2 run qos_demo safe_shutdown_demo
```

**Check:** five nonzero commands, a deliberate exception on the next timer callback, and cleanup/shutdown output. [The demo](../src/qos_demo/qos_demo/safe_shutdown_demo.py) attempts to publish a zero Twist in `finally`. Observe whether the subscriber receives it; immediate teardown and an already-interrupted context can affect delivery. Its `Robot stopped` log is not an acknowledgment from an actuator. Do not teach this as a hardware emergency-stop guarantee.

### Lecture 29 — Lifecycle transitions

```bash
ros2 run lifecycle_demo lifecycle_node_demo
```

In another terminal, run sequentially:

```bash
ros2 lifecycle get /managed_node
ros2 lifecycle set /managed_node configure
ros2 lifecycle get /managed_node
ros2 lifecycle set /managed_node activate
ros2 topic echo /lifecycle_topic std_msgs/msg/String --once
ros2 lifecycle set /managed_node deactivate
ros2 lifecycle get /managed_node
```

**Check:** unconfigured → inactive → active publication → inactive. Start a fresh `ros2 topic echo /lifecycle_topic std_msgs/msg/String` after deactivation: it should remain silent. Stop the echo, then:

```bash
ros2 lifecycle set /managed_node cleanup
ros2 lifecycle set /managed_node configure
ros2 lifecycle set /managed_node activate
ros2 topic hz /lifecycle_topic
```

**Check:** approximately 1 Hz after reconfiguration, not doubled timers. Stop `hz`, then `ros2 lifecycle set /managed_node shutdown`. The [implementation](../src/lifecycle_demo/lifecycle_demo/lifecycle_node_demo.py) delegates publisher activation to base lifecycle hooks and releases resources during cleanup. If publication is absent, inspect lifecycle state first.

### Lecture 30 — ros2_control concept boundary

This is a concept/external-package lecture; no hardware driver or controller-manager launch is authored here. If its Jazzy dependencies are installed:

```bash
ros2 pkg prefix controller_manager
ros2 control --help
```

**Check:** installed package and CLI discovery, not a running controller. `ros2 control list_controllers` needs a separately running controller manager from the lecture/demo. Do not interpret its absence as a failure of this repository's conveyor example.

## Conveyor integration (31–39)

Use an isolated simulation graph. Stop other conveyor processes before each fresh setup. The random sensor and the deterministic CLI injector must **not** publish together when checking exact thresholds. No conveyor hardware, actuator feedback, or emergency-stop implementation is present.

### Lecture 31 — Trace responsibilities

Open [the launch file](../src/conveyor_system/launch/conveyor_system.launch.py) and [interfaces](../src/conveyor_interfaces). Trace:

- `sensor_node` → `/box_state` → `control_node` → `/belt_command`.
- `/set_mode` → `operator_service_node` → retained `/conveyor_mode` → `control_node`.
- `/box_state` → active `safety_supervisor_node` → `/system_alert` → `logger_node`.

**Check:** distinguish a service response from delivery of the selected mode. Alerts are informational: **the controller does not subscribe to `/system_alert`, so an alert does not stop the belt.** The controller starts in STOP until retained mode arrives, while a fresh operator service starts in NORMAL. Missing mode input and explicit STOP must not be confused with sensor overload.

### Lecture 32 — Build custom interfaces

```bash
colcon build --symlink-install --packages-up-to conveyor_system lifecycle_demo
source install/setup.bash
ros2 interface show conveyor_interfaces/msg/BoxState
ros2 interface show conveyor_interfaces/msg/BeltCommand
ros2 interface show conveyor_interfaces/msg/SystemAlert
ros2 interface show conveyor_interfaces/srv/SetMode
```

**Check:** count/overload, speed/stop, level/message, and mode request with success/message response. A Python import error normally means the interface package was not built or its overlay is not sourced.

### Lecture 33 — Random sensor

```bash
ros2 run conveyor_system sensor_node
```

In another terminal:

```bash
ros2 topic echo /box_state conveyor_interfaces/msg/BoxState
```

**Check:** integer counts 0–10, about once per second; overload is true only above the default threshold 7. [The source](../src/conveyor_system/conveyor_system/sensor_node.py) uses randomness, so do not require a particular sequence. Stop both commands before Lecture 34.

### Lecture 34 — Deterministic controller threshold

Start **only** the controller in terminal A:

```bash
ros2 run conveyor_system control_node
```

In terminal B, keep a continuous observer running:

```bash
ros2 topic echo /belt_command conveyor_interfaces/msg/BeltCommand
```

In terminal C, with no operator service yet:

```bash
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 7, overload: false}'
```

**Check:** startup command is speed `0.0`, stop `true` because mode has not arrived. Now start in terminal D and leave running:

```bash
ros2 run conveyor_system operator_service_node
```

Its retained NORMAL mode allows speed `1.0` using the saved count 7. In terminal C:

```bash
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 8, overload: false}'
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 7, overload: true}'
```

**Check:** `0.5` then `1.0`, both with stop `false`. The intentionally inconsistent overload flags demonstrate that the controller uses its own configured count threshold (`> 7`), not that flag. Keep A, B, and D for Lecture 35. If output differs, look for duplicate sensor/control/mode publishers with `ros2 topic info --verbose`.

### Lecture 35 — Mode switching and retained STOP

Using Lecture 34's terminals:

```bash
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'STOP'}"
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 10, overload: true}'
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'invalid'}"
```

**Check:** STOP succeeds and immediately publishes zero speed with stop true; further box input cannot override it. Invalid mode returns success false and leaves STOP unchanged. Stop and restart **only** controller terminal A, keeping the operator service and observer alive: it should receive retained STOP. Inject another box sample to confirm it remains stopped.

Then:

```bash
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'slow'}"
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 1, overload: false}'
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'NORMAL'}"
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'STOP'}"
```

**Check:** slow mode gives `0.5` even at count 1, normal gives `1.0`, and final STOP gives `0.0`/true. Case is normalized. Retention requires the operator publisher to remain alive; restarting it resets mode to NORMAL. Stop this setup before the next exercise.

### Lecture 36 — Monitor lifecycle and critical boundary

Start the supervisor alone:

```bash
ros2 run conveyor_system safety_supervisor_node
```

Keep an observer in a second terminal:

```bash
ros2 topic echo /system_alert conveyor_interfaces/msg/SystemAlert
```

In a third terminal:

```bash
ros2 lifecycle set /safety_supervisor_node configure
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 9, overload: true}'
ros2 lifecycle set /safety_supervisor_node activate
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 8, overload: true}'
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 9, overload: true}'
ros2 lifecycle set /safety_supervisor_node deactivate
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 10, overload: true}'
```

**Check:** no alert while inactive; no alert at 8; CRITICAL at 9 while active; no new alert after deactivation. The actual comparison is `>= critical_threshold`, despite the alert text saying “exceeds.” Drain any already-delivered output before interpreting the inactive check. No belt-stop command is produced by this monitor. Stop all three terminals before Lecture 37.

### Lecture 37 — Full launch

```bash
ros2 launch conveyor_system conveyor_system.launch.py
```

In another terminal:

```bash
ros2 node list
ros2 lifecycle get /safety_supervisor_node
ros2 topic echo /box_state conveyor_interfaces/msg/BoxState --once
ros2 topic echo /belt_command conveyor_interfaces/msg/BeltCommand --once
ros2 service call /set_mode conveyor_interfaces/srv/SetMode "{mode: 'STOP'}"
```

**Check:** five application nodes (sensor, control, supervisor, logger, operator service), supervisor active, random sensor readings, and belt commands. The launch automatically configures then activates the supervisor; do not send `configure` again to an already-active node. At counts 9 or 10, active monitoring should emit alerts, but randomness may delay seeing one. Inspect graph/state rather than assuming a fixed time-to-alert. End with STOP, then stop launch.

### Lecture 38 — Parameters and QoS are explicit contracts

With the full launch running again:

```bash
ros2 param get /sensor_node max_box_threshold
ros2 param get /control_node max_box_threshold
ros2 param get /control_node normal_speed
ros2 param get /control_node slow_speed
ros2 param get /safety_supervisor_node critical_threshold
ros2 topic info /box_state --verbose
ros2 topic info /conveyor_mode --verbose
```

**Check:** defaults `7`, `7`, `1.0`, `0.5`, and `9`; reliable box-state communication; reliable/transient-local mode endpoints with depth 1. [system_params.yaml](../src/conveyor_system/config/system_params.yaml) uses a wildcard node key, but each node only uses the parameters its source declares/reads.

**Rate checkpoint:** YAML's `publish_rate: 1.0` sets the sensor timer to 1 Hz. Change it to `5.0`, restart the launch, and check `ros2 topic hz /box_state` for approximately 5 Hz. The rate must be finite, positive and produce a nonzero timer period representable in ROS nanoseconds; it is read-only after startup. Other sensor/control values are cached at construction, and the monitor rereads its threshold on configure; they do not provide validated live tuning callbacks. Changing stored parameters is not proof that behavior changed. Use startup overrides/restarts for this exercise.

For an isolated override check, stop the full launch. Recreate Lecture 34's controller, observer, and operator-service terminals, replacing its controller command with:

```bash
ros2 run conveyor_system control_node --ros-args --params-file src/conveyor_system/config/system_params.yaml -p max_box_threshold:=3
```

With the operator in NORMAL and no random sensor running, inject in a separate terminal:

```bash
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 3, overload: false}'
ros2 topic pub --once /box_state conveyor_interfaces/msg/BoxState '{box_count: 4, overload: true}'
```

**Check:** normal then slow speed. Stop that setup. For a separate sensor-only check:

```bash
ros2 run conveyor_system sensor_node --ros-args --params-file src/conveyor_system/config/system_params.yaml -p max_box_threshold:=3
```

Observe with `ros2 topic echo /box_state conveyor_interfaces/msg/BoxState` in another terminal. **Check:** overload means count > 3. Override both sensor and controller in a combined system so their thresholds agree.

### Lecture 39 — Repeatable debugging and regression checks

Run Lectures 34–38 again after rebuilding any changed source. Record observed topic names, lifecycle states, parameters, and boundary results instead of only “it runs.” Stop the demo graph, then:

```bash
colcon test --packages-select conveyor_system lifecycle_demo
colcon test-result --verbose
```

**Check:** inspect the actual test report, including failures; do not assume these commands guarantee a pass. [Conveyor tests](../src/conveyor_system/test) cover mode/threshold/runtime and default launch behavior; [lifecycle tests](../src/lifecycle_demo/test/test_lifecycle_runtime.py) cover managed publication. Runtime tests need working ROS dependencies and discovery. Template lint/license failures and functional failures should be reported separately, not hidden.

Completion means you can explain startup STOP versus operator NORMAL, retain STOP across controller restart, demonstrate the strict slowdown and inclusive alert thresholds, deactivate monitoring without new alerts, and distinguish alert logging from an implemented safety stop. On shutdown, stop every exercise process and verify no unintended command publisher remains. This educational system does not implement hardware safety, sensor-loss watchdogs, or persistent operator mode across an operator-service restart.
