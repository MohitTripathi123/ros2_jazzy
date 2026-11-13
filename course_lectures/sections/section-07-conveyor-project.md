# Section 7: Final Project — Autonomous Conveyor Monitoring Micro-System

[Back to course index](../README.md) · [Practical commands and checkpoints](../core-practical-checkpoints.md)

## Lecture 31: Final Project Architecture Planning

Design the conveyor monitoring system before implementation. Define node responsibilities, communication paths, custom interfaces, parameters, QoS choices, lifecycle boundaries, and failure behaviour.

## Lecture 32: Creating Custom Interfaces for the Monitoring System

Create the `BoxState`, `BeltCommand`, and `SystemAlert` messages and the `SetMode` service. Build the interface package and make the generated types available to Python nodes.

## Lecture 33: Sensor Node Implementation

Simulate conveyor sensor readings and publish box state periodically. Populate box count and overload data while applying an explicit QoS profile.

## Lecture 34: Processing Node Implementation

Process incoming box-state data and convert it into operational decisions. Apply configured thresholds and publish commands that represent normal or reduced conveyor speed.

## Lecture 35: Control Node with Service-Based Mode Switching

Expose operator-selectable `NORMAL`, `SLOW`, and `STOP` modes through a custom ROS 2 service. Validate requested modes and connect the selected mode to conveyor-control behaviour.

## Lecture 36: Lifecycle-Based Monitoring Node

Implement safety monitoring as a lifecycle node. Create monitoring resources during configuration, activate controlled behaviour, and publish critical alerts when the safety threshold is exceeded.

## Lecture 37: Full Launch System Integration

Launch the complete multi-node conveyor application from one file. Load shared configuration, start each executable, and verify the final ROS graph and topic connections.

## Lecture 38: YAML Configuration, Parameters & QoS Integration

Centralize the supported conveyor thresholds and speeds in YAML and combine them with deliberate QoS choices. The `publish_rate` YAML entry sets the sensor rate at startup; use a finite positive number and restart after editing it. Review how runtime configuration influences each node without modifying source code.

## Lecture 39: Final Debugging, Refactoring & Strong ROS 2 Engineer Wrap-Up

Build, run, inspect, and debug the complete project systematically. Refactor duplicated or hardcoded logic, verify shutdown behaviour, and summarize the engineering practices developed during Phase 1.

