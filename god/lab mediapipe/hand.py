import mediapipe as mp
import cv2
from contextlib import contextmanager
from my_util import *

def draw_landmarks_custom(image, detection_result):
    height, width, _ = image.shape
    res = (width, height)
    if detection_result.multi_hand_landmarks:
        for hand_landmarks_list in detection_result.multi_hand_landmarks:
            landmarks = hand_landmarks_list.landmark
            
            ## custom 
            thumb_f = [landmarks[mp_hands.HandLandmark.THUMB_TIP.value].x, landmarks[mp_hands.HandLandmark.THUMB_TIP.value].y]
            index_f = [landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP.value].x, landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP.value].y]
            thumb_f = [int(value * res) for value, res in zip(thumb_f, res)]
            index_f = [int(value * res) for value, res in zip(index_f, res)]
            cv2.circle(image, thumb_f, radius=5, color=(0, 255, 0), thickness=-1)
            cv2.circle(image, index_f, radius=5, color=(0, 255, 0), thickness=-1)
            


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

 
with timer("use webcam"):
    with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        with Webcam(cam_index = 0) as cap:
            while cap.isOpened():
                ret, frame_bgr = cap.read()
                if not ret:
                    print("Failed to read frame")
                    break
                
                
                frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)
                
                draw_hand_landmarks_official(frame_bgr, results)
                
                # # add text
                # text = ["a", "b", "c"]
                # put_multiline_text(image = frame_bgr, 
                #                    text = text, 
                #                    position = [10,10], 
                #                    font = cv2.FONT_HERSHEY_SIMPLEX, 
                #                    font_scale = 0.5, 
                #                    color = (0, 255, 0), 
                #                    thickness = 1, 
                #                    line_type = cv2.LINE_AA, 
                #                    line_space = 30
                #                    )
                        
                cv2.imshow("Webcam", frame_bgr)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
                    break

