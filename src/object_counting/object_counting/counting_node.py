import cv2
from cv_bridge import CvBridge
from deep_sort_realtime.deepsort_tracker import DeepSort
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from ultralytics import YOLO


class ObjectCountingNode(Node):
    def __init__(self):
        super().__init__('counting_node')
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )
        self.publisher = self.create_publisher(Image, '/object_counting/image', 10)
        self.bridge = CvBridge()
        self.model = YOLO('yolov8m.pt')  # Load YOLOv8 model
        self.tracker = DeepSort()  # Initialize Deep SORT tracker
        self.counted_ids = set()  # Set to store unique object IDs
        self.previous_center_y = {}
        self.count = 0  # Counter for unique objects
        self.line_y = 250  # Y-coordinate of the counting line

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV format
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Perform object detection using YOLOv8
        results = self.model(cv_image)[0]  # Get the first result (assuming batch size of 1)

        # Extract bounding boxes and class labels
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                confidence = float(box.conf[0])
                class_id = int(box.cls[0])
                detections.append(([x1, y1, x2-x1, y2-y1], confidence, class_id))

        # Update tracker with new detections
        tracks = self.tracker.update_tracks(detections, frame=cv_image)

        # Count objects based on tracked IDs and class labels
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            left, top, right, bottom = track.to_ltrb()
            center_y = int((top + bottom) / 2)
            previous_y = self.previous_center_y.get(track_id)
            crossed_line = (
                previous_y is not None
                and previous_y <= self.line_y < center_y
            )
            if crossed_line and track_id not in self.counted_ids:
                self.counted_ids.add(track_id)
                self.count += 1
                self.get_logger().info(
                    f'Object {track_id} crossed the counting line. '
                    f'Total count: {self.count}'
                )
            self.previous_center_y[track_id] = center_y
            cv2.rectangle(
                cv_image,
                (int(left), int(top)),
                (int(right), int(bottom)),
                (0, 255, 0),
                2,
            )
            cv2.putText(
                cv_image,
                f'ID: {track_id}',
                (int(left), int(top)-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

        # Draw counting line
        cv2.line(cv_image, (0, self.line_y), (cv_image.shape[1], self.line_y), (255, 0, 0), 2)
        # Display count on image
        cv2.putText(
            cv_image,
            f'Count: {self.count}',
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

        # Publish annotated image so rqt_image_view can display it
        annotated_msg = self.bridge.cv2_to_imgmsg(cv_image, encoding='bgr8')
        annotated_msg.header = msg.header
        self.publisher.publish(annotated_msg)

        cv2.imshow('Object Counting', cv_image)
        cv2.waitKey(1)

        # Print the current counts of each object class
        print(f'Total Count: {self.count}')


def main(args=None):
    rclpy.init(args=args)
    counting_node = ObjectCountingNode()
    rclpy.spin(counting_node)
    counting_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
