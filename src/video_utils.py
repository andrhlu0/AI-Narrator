import cv2
import os
from typing import List, Tuple

def extract_scenes(video_path: str, scene_threshold: float = 30.0) -> List[Tuple[float, float]]:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    scene_changes = [0.0]

    prev_frame = None
    frame_idx = 0
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if prev_frame is not None:
            diff = cv2.absdiff(gray, prev_frame)
            score = diff.mean()

            if score > scene_threshold:
                timestamp = frame_idx / fps
                scene_changes.append(timestamp)

        prev_frame = gray
        frame_idx += 1

    scene_changes.append(duration)
    cap.release()

    scenes = [(scene_changes[i], scene_changes[i + 1]) for i in range(len(scene_changes) - 1)]
    return scenes
