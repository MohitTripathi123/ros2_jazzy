# Section 3: Advanced ROS 2 Communication

[Back to course index](../README.md) · [Practical commands and checkpoints](../core-practical-checkpoints.md)

## Lecture 12: Actions with a Separate Interface Package

Define a Fibonacci action in a dedicated interface package and use it from an action server. Understand goal, feedback, and result data and why long-running tasks are better represented as actions than services.

## Lecture 13: Parameters

Declare, read, and use node parameters instead of hardcoding runtime values. Explore default values and use ROS 2 CLI commands to inspect and update parameters.

## Lecture 14: Parameter Callbacks & Validation

Validate parameter changes before accepting them. Enforce expected types and safe numeric ranges, return meaningful rejection reasons, and update node behaviour at runtime.

## Lecture 15: Launch Files

Start multiple ROS 2 nodes from a Python launch description. Learn the basic launch structure, node actions, package/executable selection, parameters, names, and console output.

## Lecture 16: Launch Arguments

Expose configurable launch-time values with declared arguments and `LaunchConfiguration`. Pass values into nodes so one launch file can support multiple runtime configurations.

## Lecture 17: Advanced Launch (Namespaces, Conditions, Groups)

Organize larger systems with namespaces, conditions, and grouped launch actions. Use conditional execution and namespacing to run reusable node configurations without topic or node-name collisions.

## Lecture 18: ROS 2 CLI Deep Dive

Use the ROS 2 CLI to investigate nodes, topics, services, actions, interfaces, parameters, and the running graph. Develop a systematic command-line workflow for validating and debugging applications.

