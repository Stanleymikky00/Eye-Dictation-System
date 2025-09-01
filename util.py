import cv2
import numpy as np

def euclidean_distance(a, b):
    return np.linalg.norm(a - b)



def eye_aspect_ratio(eye):
    """compute the euclidean distance between the two swta of.
    vertical eye and horizontal eye"""

    A = euclidean_distance(eye[1], eye[5])
    B = euclidean_distance(eye[2], eye[4])
    C = euclidean_distance(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)
    return ear