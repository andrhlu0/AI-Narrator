from typing import List, Tuple
from PIL import Image
import torch
from transformers import Blip2Processor, Blip2ForConditionalGeneration
import cv2
import io
from tqdm import tqdm

# Load BLIP-2 model & processor once globally for efficiency
processor = Blip2Processor.from_pretrained("Salesforce/blip2-flan-t5-xl")
model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-flan-t5-xl").to("cpu")

def extract_frame(video_path: str, timestamp: float) -> Image.Image:
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise RuntimeError(f"Failed to extract frame at {timestamp}s")
    # Convert BGR to RGB for PIL
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame_rgb)

def analyze_scenes(scenes: List[Tuple[float, float]], video_path: str) -> List[str]:
    scene_descriptions = []
    for start, end in tqdm(scenes, desc="Analyzing scenes", unit="scene"):
        mid_time = (start + end) / 2
        frame = extract_frame(video_path, mid_time)

        prompt = "Describe this scene vividly as part of a story, capturing emotions and actions:"
        inputs = processor(frame, prompt, return_tensors="pt").to(model.device)
        outputs = model.generate(**inputs, max_new_tokens=64)
        description = processor.decode(outputs[0], skip_special_tokens=True)

        scene_descriptions.append(description)

    return scene_descriptions
