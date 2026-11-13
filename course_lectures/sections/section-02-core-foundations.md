# Section 2: ROS 2 Core Foundations

[Back to course index](../README.md) · [Practical commands and checkpoints](../core-practical-checkpoints.md)

## Lecture 7: Writing Your First ROS 2 Node

Create a basic `rclpy` node and follow its complete lifecycle from initialization to shutdown. Use the node logger and understand why spinning is required to process ROS callbacks.

## Lecture 8: Publisher Node

Build a timed publisher that sends `std_msgs/String` messages. Learn how message types, topic names, queue depth, timers, and logging fit together in a ROS 2 node.

## Lecture 9: Subscriber Node

Subscribe to a topic and process incoming messages in a callback. Connect the subscriber to the publisher and observe asynchronous topic communication between independent processes.

## Lecture 10: Topic CLI Tools

Inspect topics without changing application code. Use ROS 2 CLI commands to list topics, inspect message types, display live messages, measure frequency, and publish test data.

## Lecture 11: Services

Implement a request-response workflow with an `AddTwoInts` server and asynchronous client. Learn service discovery, request and response objects, futures, and waiting for a result safely.

