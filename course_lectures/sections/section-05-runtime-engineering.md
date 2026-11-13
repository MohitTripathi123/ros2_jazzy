# Section 5: ROS 2 Execution Model & Runtime Engineering

[Back to course index](../README.md) · [Practical commands and checkpoints](../core-practical-checkpoints.md)

## Lecture 23: Executors & Callback Flow: Single-Threaded Executor

Study how a single-threaded executor schedules timers and other callbacks. Use a deliberately slow callback to observe how blocking work delays every other callback in the same executor.

## Lecture 24: Turtlesim Runtime Visualization

Control Turtlesim with `geometry_msgs/Twist` and observe callback timing through visible robot motion. Connect abstract execution behaviour to a clear runtime result.

## Lecture 25: Multi-Threaded Executors

Run independent callbacks concurrently with a multi-threaded executor. Compare behaviour with the single-threaded example and understand when extra executor threads improve responsiveness.

## Lecture 26: Callback Groups

Control which callbacks may execute concurrently with callback groups. Use a reentrant callback group and understand the difference between concurrency permission and the number of executor threads.

## Lecture 27: QoS Fundamentals

Configure queue depth, reliability, and durability for ROS 2 communication. Understand reliable versus best-effort delivery and volatile versus transient-local data retention.

## Lecture 28: Clean Shutdown & Error Handling

Handle keyboard interruption and unexpected exceptions while leaving the robot in a safe state. Publish a final stop command, release timers and nodes, and guarantee ROS shutdown with `finally`.

