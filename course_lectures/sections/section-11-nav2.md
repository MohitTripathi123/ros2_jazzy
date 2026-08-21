# Section 11: Applied Robotics — Nav2 Navigation Stack, Planning and Behavior Trees

[Back to course index](../README.md)

## Lecture 62: Advanced Debugging for AMCL, TF, Lifecycle and Nav2

Debug navigation as a connected system instead of treating errors independently. Check lifecycle states, transforms, timestamps, map availability, sensor topics, parameters, and action servers in a repeatable order.

## Lecture 63: Nav2 Architecture & Behavior Trees

Understand the main Nav2 servers and how a behavior tree coordinates planning, path following, recovery, and goal completion. Trace a navigation request through the stack.

## Lecture 64: Global & Local Planning: A* and DWA Concepts

Compare global path search with local velocity selection. Study A* graph search and the Dynamic Window Approach conceptually, including obstacle avoidance, kinematic constraints, and scoring candidate motion.

## Lecture 65: Costmaps & Parameter Tuning

Understand local and global costmaps, sensor sources, obstacle marking and clearing, inflation, robot footprint, resolution, and update frequency. Tune parameters while observing their effect on navigation.

## Lecture 66: nav2_params.yaml Deep Dive

Read the Nav2 configuration as a complete system contract. Connect each server, plugin, frame, topic, frequency, tolerance, and limit to its runtime behavior.

## Lecture 67: Behavior Tree XML Deep Dive

Read a navigation Behavior Tree XML file from its root pipeline to action, condition, control, and decorator nodes. Understand ports, blackboard values, retries, fallbacks, and recovery subtrees.

## Lecture 68: Nav2 Recovery Behaviors Inside Behavior Tree

Study how the tree responds when planning or control fails. Follow costmap clearing, spinning, waiting, backup, retry counters, and fallback logic that prevents a single failure from immediately aborting navigation.

