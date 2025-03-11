from contextlib import contextmanager
import cv2
import time
import math
import yaml
from mediapipe.framework.formats import landmark_pb2
from mediapipe import solutions


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
print(config)

CAM_PROP = {
    "res" : config["CAM_PROP"]["res"],
    "fps" : config["CAM_PROP"]["fps"]
    }
SCALE_FACTOR = config["SCALE_FACTOR"]


@contextmanager
def timer(code_part = "No part name"):
    start = time.perf_counter()
    yield  # Everything in the `with` block executes here
    end = time.perf_counter()
    take_time = (end - start)*1000
    print(f"***This {code_part} took about {take_time:.2f} millisecond***")
    
class Webcam:
    def __init__(self, cam_index=0):
        self.cam_index = cam_index
        self.is_rotate_90 = False
        self.cap = None

    def __enter__(self):
        with timer("get device"):
            self.cap = cv2.VideoCapture(self.cam_index)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, math.ceil(CAM_PROP["res"][0] * SCALE_FACTOR))  # Set an unrealistically high value 
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, math.ceil(CAM_PROP["res"][1] * SCALE_FACTOR)) 
                self.cap.set(cv2.CAP_PROP_FPS, CAM_PROP["fps"]) 
            else: 
                raise RuntimeError("Failed to open webcam") 
        return self.cap  # Assign `cap` to `as cap` 

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("Webcam released, all windows closed.")
        
def put_multiline_text(image, text, position, font, font_scale, color, thickness, line_type=cv2.LINE_AA, line_space = 30):
    # Split the input text by newlines
    y_offset = position[1]

    # Iterate over each line and put it on the image
    for line in text:
        cv2.putText(image, line, (position[0], y_offset), font, font_scale, color, thickness, line_type)
        y_offset += math.ceil(font_scale * line_space)  # Move the Y position down for the next line
        
        
def draw_hand_landmarks_official(rgb_image, detection_result):
    if detection_result.multi_hand_landmarks:
        for hand_landmarks_list in detection_result.multi_hand_landmarks:
            hand_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
            for landmark in hand_landmarks_list.landmark:
                # can extract specify point in this code
                point = landmark_pb2.NormalizedLandmark(x=landmark.x, y=landmark.y, z=landmark.z)
                hand_landmarks_proto.landmark.extend([point])
                    
            solutions.drawing_utils.draw_landmarks(
                rgb_image,
                hand_landmarks_proto,
                solutions.hands.HAND_CONNECTIONS,
                solutions.drawing_styles.get_default_hand_landmarks_style()
            )