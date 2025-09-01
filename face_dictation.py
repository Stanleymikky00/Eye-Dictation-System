import cv2
import mediapipe as mp
import time
import numpy as np
import gradio as gr

from alarm import *
from util import euclidean_distance, eye_aspect_ratio

# eye landmark indices (MediaPipe face mesh example)
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# Define two constance, EYE_THRESH : for the eye_aspect_ratio to indicate blink
# and EYE_CONSTANCE: Number of consecutive times th eye must be below the threshold

# (Thresholds and Drowsiness Logic
# 	•	Open eye: EAR ≈ 0.25 – 0.35
# 	•	Closed eye: EAR ≈ 0.10 – 0.18
# 	•	Threshold: often chosen ≈ 0.21)

EYE_THRESH = 0.21    # EAR below this = CLOSED
EYE_CONSTANCE = 3    # to count a normal blink (≈0.1s at ~30 FPS)
COUNTER = 0
TOTAL = 0
CLOSED_DROWSY_SEC = 0.8    # eyes closed this long → DROWSY
CLOSED_DANGEROUS_SEC = 2.0 # eyes closed this long → DANGEROUS
closed_start = None
state = "OPEN"     # OPEN, DROWSY, DANGEROUS



mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face =mp_face.FaceMesh(
    max_num_faces= 1,
    min_detection_confidence= 0.5,
    min_tracking_confidence= 0.5,
    refine_landmarks=True
)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame,1)
    h,w = frame.shape[:2]
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    results = face.process(rgb)

    if results.multi_face_landmarks:
        for face_lms in results.multi_face_landmarks:
            thin = mp_drawing.DrawingSpec(color=(0,255,0),thickness=1,circle_radius=0)

            # this code here is optional; its importance was about creating a wide landmark on the face capturing all the visible parts

            mp_drawing.draw_landmarks(frame,face_lms,mp_face.FACEMESH_LEFT_EYE,landmark_drawing_spec=thin,connection_drawing_spec=thin)
            mp_drawing.draw_landmarks(frame, face_lms, mp_face.FACEMESH_RIGHT_EYE, landmark_drawing_spec=thin,connection_drawing_spec=thin)

            # 1) get eye points (x,y)
            left_eye_pts = np.array([(face_lms.landmark[i].x * w,
                                      face_lms.landmark[i].y * h) for i in LEFT_EYE], dtype=np.float32)
            right_eye_pts = np.array([(face_lms.landmark[i].x * w,
                                       face_lms.landmark[i].y * h) for i in RIGHT_EYE], dtype=np.float32)

            # 2) compute EAR for each eye
            leftEAR = eye_aspect_ratio(left_eye_pts)
            rightEAR = eye_aspect_ratio(right_eye_pts)
            ear_avg = (leftEAR + rightEAR) / 2.0



            # 3) Visualization
            for (x, y) in np.vstack([left_eye_pts, right_eye_pts]).astype(int):
                cv2.circle(frame, (x, y), 2, (0, 0, 255), -1)

            # Blink detection logic
            if ear_avg < EYE_THRESH:
                COUNTER += 1
            else:
                if COUNTER >= EYE_CONSTANCE:
                    TOTAL += 1
                COUNTER = 0 # RESET COUNTER

            # close duration timer
            now = time.time()
            if ear_avg < EYE_THRESH:
                if closed_start is None:
                    closed_start = now
                closed_end = now - closed_start

                if  closed_end >= CLOSED_DANGEROUS_SEC:
                    state = "DANGEROUS"  #red alart
                    start_alarm("dangerous")
                elif closed_end >= CLOSED_DROWSY_SEC:
                    state = "DROWSY"
                    start_alarm("drowsy")
                else:
                    state = "CLOSED"
            else:
                closed_start = None
                state = "OPEN"
                stop_alarm()


            #INSERT TEXT ON FRAME:
            cv2.putText(frame, f"EAR: {ear_avg:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"Blinks: {TOTAL}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # colored border by state
            color = (0, 200, 0) if state == "OPEN" else (0, 165, 255) if state in ("CLOSED", "DROWSY") else (0, 0, 255)
            th = 6
            h, w = frame.shape[:2]
            cv2.rectangle(frame, (0, 0), (w - 1, h - 1), color, th)

            # label
            cv2.putText(frame, state, (10, 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 200, 0) if state == "OPEN" else (0, 165, 255) if state in ("CLOSED", "DROWSY") else (
                        0, 0, 255), 2)


        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

