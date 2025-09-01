import cv2
import mediapipe as mp
import time
import numpy as np
import gradio as gr

cap = cv2.VideoCapture(0)

#set resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera not available")
        break

    cv2.imshow('Camera (press q to quit)', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()    # free the camera
cv2.destroyAllWindows()  # close the window