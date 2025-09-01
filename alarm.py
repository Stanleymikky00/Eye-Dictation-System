import pygame
import os

# --- Audio init ---
pygame.mixer.init()  # default sample rate is fine
DROWSY_PATH    = os.path.join("data", "221088__alaskarobotics__1000-hz-beeps.wav")
DANGEROUS_PATH = os.path.join("data", "324394__o_ultimo__003-invasion-alarm.mp3")
DANGEROUS_PATH1 = os.path.join("data", "338848__archeos__danger.wav")


# Load sounds (wrap to avoid crash if missing)
drowsy_snd = pygame.mixer.Sound(DROWSY_PATH)    if os.path.exists(DROWSY_PATH)    else None
danger_snd = pygame.mixer.Sound(DANGEROUS_PATH) if os.path.exists(DANGEROUS_PATH) else None
danger_snd1 = pygame.mixer.Sound(DANGEROUS_PATH1) if os.path.exists(DANGEROUS_PATH) else None

# Optional volumes (0.0–1.0)
if drowsy_snd:  drowsy_snd.set_volume(0.6)
if danger_snd:  danger_snd.set_volume(1.0)
if danger_snd1:  danger_snd1.set_volume(4.0)

# Manage which alarm is currently playing
_current_alarm = None  # None / "drowsy" / "dangerous"

def start_alarm(level: str):
    """Start looping the right alarm if not already playing."""
    global _current_alarm
    if level == _current_alarm:
        return  # already playing this level
    stop_alarm()  # stop any previous level first
    if level == "drowsy" and drowsy_snd:
        drowsy_snd.play(loops=-1)  # loop forever
        _current_alarm = "drowsy"
    elif level == "dangerous" and danger_snd:
        danger_snd.play(loops=-1)
        danger_snd1.play(loops=-1)
        _current_alarm = "dangerous"

def stop_alarm():
    """Stop any alarm immediately."""
    global _current_alarm
    pygame.mixer.stop()
    _current_alarm = None