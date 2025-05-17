import os
import json
import argparse
from src.video_utils import extract_scenes
from src.vision_analysis import analyze_scenes
from src.llm_storygen import generate_narration
from src.tts_engine import synthesize_audio
from src.aligner import align_narration
from src.muxer import mux_audio_to_video

def validate_input_video(video_path: str) -> None:
    """Raise error if video file is missing or not an .mp4."""
    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Input video '{video_path}' not found.")
    if not video_path.lower().endswith('.mp4'):
        raise ValueError(f"Unsupported format: '{video_path}'. Only .mp4 files are accepted.")

def process_video(video_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Extract scenes
    print("[1/6] Extracting scenes from video...")
    scenes = extract_scenes(video_path)
    with open("sample_data/scenes.json", "w", encoding="utf-8") as f:
        json.dump(scenes, f, indent=2)

    # Step 2: Analyze scenes
    print("[2/6] Analyzing scenes with vision model...")
    scene_descriptions = analyze_scenes(scenes, video_path)
    with open("sample_data/scene_descriptions.json", "w", encoding="utf-8") as f:
        json.dump(scene_descriptions, f, indent=2)

    # Step 3: Generate story narration
    print("[3/6] Generating story narration with LLM...")
    narration = generate_narration(scene_descriptions)
    with open("sample_data/narration.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(narration) if isinstance(narration, list) else narration)

    # Step 4: Align narration to video timeline
    print("[4/6] Aligning narration to video timeline...")
    narration_timed = align_narration(narration, scenes)

    # Step 5: Synthesize narration audio
    print("[5/6] Synthesizing narration audio...")
    audio_path = os.path.join(output_dir, "narration.mp3")
    synthesize_audio(narration_timed, audio_path)

    # Step 6: Mux audio with original video
    print("[6/6] Muxing audio with original video...")
    narrated_video_path = os.path.join(output_dir, "narrated_output.mp4")
    mux_audio_to_video(video_path, audio_path, narrated_video_path)

    print("Narration pipeline complete.")
    return narration_timed, audio_path, narrated_video_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Narrate an input MP4 video.")
    parser.add_argument("video_path", help="Path to input .mp4 video")
    parser.add_argument("--output_dir", default="test_output", help="Directory to save outputs")
    args = parser.parse_args()

    try:
        validate_input_video(args.video_path)
        process_video(args.video_path, args.output_dir)
    except Exception as e:
        print(f"[ERROR] {e}")
