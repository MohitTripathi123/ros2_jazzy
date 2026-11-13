import cv2
from cv_bridge import CvBridge
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO


class YoloDetectionNode(Node):
    def __init__(self):
        super().__init__('yolo_detection_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')  # Load the YOLOv8 model

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV format
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        results = self.model(frame)  # Perform object detection
        annotated_frame = results[0].plot()  # Get the annotated frame with detections
        cv2.imshow('YOLO Detection', annotated_frame)  # Display the annotated frame
        cv2.waitKey(1)  # Wait for a key press to update the display


def main(args=None):
    rclpy.init(args=args)
    yolo_detection_node = YoloDetectionNode()
    rclpy.spin(yolo_detection_node)
    yolo_detection_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
