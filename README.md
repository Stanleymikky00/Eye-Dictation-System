## EYE BLINK DICTATION

This project implements real-time eye blink detection and drowsiness monitoring using OpenCV and MediaPipe.
It calculates the Eye Aspect Ratio (EAR) from facial landmarks to distinguish between open and closed eyes.
The system also provides both visual and audio feedback for blink counting, drowsy states, and dangerous prolonged eye closure.

## DEMO VIDEO
A short Demo video of the project.
![Demo](data/demo.gif)


## FEATURES

•	Real-time face and eye landmark tracking using MediaPipe
•	Calculation of Eye Aspect Ratio (EAR) for each eye
•	Blink counter with configurable threshold
•	Drowsiness detection
•	Closed eyes for 0.8 seconds triggers a “Drowsy” alert
•	Closed eyes for 2.0 seconds triggers a “Dangerous” alert
•	Visual feedback
•	EAR values and blink count displayed on the video frame
•	Green border: eyes open
•	Orange border: eyes closed briefly or drowsy
•	Red border: eyes dangerously closed
•	Audio feedback
•	Looping alarm sound for drowsy state
•	Louder alarm sound for dangerous state
•	Sound stops immediately when eyes open


## REQUIREMENTS

•	Python 3.8 or higher
•	Required Python packages:
•	opencv-python
•	mediapipe
•	numpy
•	pygame

All dependencies can be installed with:
pip install -r requirements.txt

## EAR THRESHOLDS

•	Open eye: EAR approximately 0.25 – 0.35
•	Closed eye: EAR approximately 0.10 – 0.18
•	Default threshold: 0.21

Threshold values may need to be adjusted depending on camera quality, lighting, and the individual user.

## NOTES

Good lighting conditions improve tracking accuracy.
EAR threshold and time constants (drowsy vs dangerous) can be tuned in face_dictation.py.

# This project is for research and educational purposes only and is not a certified driver assistance tool.
