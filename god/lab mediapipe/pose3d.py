import mediapipe as mp
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from my_util import *

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def draw_landmarks_official(rgb_image, detection_result):
    if detection_result.pose_landmarks:
        pose_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
        for landmark in detection_result.pose_landmarks.landmark:
            point = landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
            pose_landmarks_proto.landmark.append(point)

        solutions.drawing_utils.draw_landmarks(
            rgb_image,
            pose_landmarks_proto,
            solutions.pose.POSE_CONNECTIONS,
            solutions.drawing_styles.get_default_pose_landmarks_style()
        )

def plot_3d_pose(ax, landmarks):
    ax.clear()
    if landmarks:
        x, y, z = [], [], []
        for landmark in landmarks.landmark:
            x.append(landmark.x)
            y.append(landmark.y)
            z.append(-landmark.z)  # Invert Z for better visualization
        ax.scatter(x, y, z, c='r', marker='o')
    
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_zlim(-1, 1)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    plt.pause(0.01)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

with timer("use webcam"):
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        with Webcam(cam_index=1) as cap:
            while cap.isOpened():
                ret, frame_bgr = cap.read()
                if not ret:
                    print("Failed to read frame")
                    break
                
                frame_bgr = cv2.rotate(frame_bgr, cv2.ROTATE_90_CLOCKWISE)
                
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                results = pose.process(frame_rgb)
                
                draw_landmarks_official(frame_bgr, results)
                # plot_3d_pose(ax, results.pose_landmarks)

                cv2.imshow("Webcam", frame_bgr)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

cv2.destroyAllWindows()
