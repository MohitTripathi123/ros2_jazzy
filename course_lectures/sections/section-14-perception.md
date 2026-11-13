# Section 14: Applied Robotics — Perception with OpenCV, YOLO and DeepSORT

[Back to course index](../README.md) · [Practical commands and checkpoints](../applied-practical-checkpoints.md)

**Before running these examples:** complete the camera and ROS-GZ bridge setup demonstrated in Lecture 82. The current sensor, bridge and subscribers use `/camera/image_raw`; verify live images before starting a model. Run one perception example at a time.

## Lecture 78: OpenCV with ROS2: Perception Begins

Subscribe to `sensor_msgs/Image`, convert images with `cv_bridge`, and process frames with OpenCV. Perform a grayscale transformation and display the result as the first ROS 2 perception pipeline.

## Lecture 79: Object Detection: YOLO with ROS2

Load an Ultralytics YOLO model and run inference on incoming camera frames. Interpret detections, confidence, class IDs, bounding boxes, and model-generated annotations.

## Lecture 80: Object Tracking: DeepSORT with ROS2

Convert YOLO detections into Deep SORT tracker input and maintain object identities over consecutive frames. Draw confirmed tracks, bounding boxes, and persistent IDs on the video stream.

## Lecture 81: Object Counting & Event Detection

Track object centers relative to a virtual counting line and count each confirmed track only when it crosses. Publish an annotated image and log crossing events while preventing duplicate counts for the same ID.

