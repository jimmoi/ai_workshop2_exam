import cv2
import mediapipe as mp
import numpy as np
import time


"""
def calculate_angle(a, b, c):
    # Calculate the angle between three points (a, b, c)
    # Vectors b->a and b->c
    ab = np.array(a) - np.array(b)
    bc = np.array(c) - np.array(b)
    
    dot_product = np.dot(ab, bc)
    magnitude_ab = np.linalg.norm(ab)
    magnitude_bc = np.linalg.norm(bc)
    
    cos_angle = dot_product / (magnitude_ab * magnitude_bc)
    
    angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
    angle = np.degrees(angle)
    
    return angle
"""

def calculate_angle(a, c):
    # Calculate the angle between two points (a and c)
    # Vector a->c
    ac = np.array(c) - np.array(a)
    
    angle = np.arctan2(ac[1], ac[0]) 
    angle = np.degrees(angle)
    
    return angle

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

prev_time = 0

cap = cv2.VideoCapture(0)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        
        # Make detection
        results = pose.process(image)
        
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Extract landmarks
        try:
            landmarks = results.pose_landmarks.landmark
            
            # Get coordinates of left shoulder and left wrist
            # Part extract keypoint ตรงนี้สามารถเอาไปเทรนพวก machine learning ต่อได้แล้วเอามาใช้งานด้วยกัน
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            # Calculate the angle between shoulder and wrist
            angle = calculate_angle(shoulder, wrist)
            
            # Convert coordinates from normalized to pixel values (assuming image size is 640x480)
            shoulder_px = np.multiply(shoulder, [640, 480]).astype(int)
            wrist_px = np.multiply(wrist, [640, 480]).astype(int)
            
            # Draw a red line connecting shoulder to wrist
            cv2.line(image, tuple(shoulder_px), tuple(wrist_px), (0, 0, 255), 2) 
            
            # Find the midpoint of the line
            midpoint = ((shoulder_px[0] + wrist_px[0]) // 2, (shoulder_px[1] + wrist_px[1]) // 2)
            
            # Display the angle at the midpoint of the line
            cv2.putText(image, str(int(angle)), midpoint, 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
        except:
            pass
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2))   
                    
        cv2.putText(image, f'FPS: {int(fps)}', (10, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        
        # Display the frame
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()