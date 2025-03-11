import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
from my_util import *

            
            
def draw_landmarks_official(rgb_image, detection_result):
    if detection_result.pose_landmarks:  # Ensure landmarks exist
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        for landmark in detection_result.pose_landmarks.landmark:  # Access landmarks correctly
            point = landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
            pose_landmarks_proto.landmark.append(point)  # Use `append()` instead of `extend([point])`

        solutions.drawing_utils.draw_landmarks(
            rgb_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

 
with timer("use webcam"):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        with Webcam(cam_index = 1) as cap:
            while cap.isOpened():
                ret, frame_bgr = cap.read()
                if not ret:
                    print("Failed to read frame")
                    break
                
                
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)
                
                draw_landmarks_official(frame_bgr, results)
                        
                cv2.imshow("Webcam", frame_bgr)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                    break


