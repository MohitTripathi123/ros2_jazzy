import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

class ObjectTrackingNode(Node):
    def __init__(self):
        super().__init__('tracking_node')
        self.bridge = CvBridge()
        self.model = YOLO('yolov8m.pt')  # Load YOLOv8 model
        self.tracker = DeepSort(max_age=30)  # Initialize Deep SORT tracker
        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10)
        

    def image_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        # Perform object detection
        results = self.model(frame)[0]  # Get results for the first image in the batch
        
        # Extract bounding boxes and confidence scores        
        detections = []
        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Get bounding box coordinates
            confidence = float(box.conf[0])  # Get confidence score
            class_id = int(box.cls[0])  # Get class ID
            detections.append(([x1, y1, x2-x1, y2-y1], confidence, class_id))
        
        # Update tracker with new detections
        tracks = self.tracker.update_tracks(detections, frame=frame)
        # Draw bounding boxes and track IDs on the frame
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            x1, y1, x2, y2 = track.to_ltrb()  # Get bounding box in (left, top, right, bottom) format
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  # Draw bounding box
            cv2.putText(frame, f'ID: {track_id}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Draw track ID 
        # Display the resulting frame
        cv2.imshow('Object Tracking', frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    object_tracking_node = ObjectTrackingNode()
    rclpy.spin(object_tracking_node)
    object_tracking_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':    
    main()
