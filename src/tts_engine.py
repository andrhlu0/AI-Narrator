from typing import List, Tuple
import pyttsx3
import os
import tempfile
from pydub import AudioSegment

def synthesize_audio(narration_timed: List[Tuple[float, str]], output_path: str) -> None:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)

    temp_files = []
    tasks = []

    # Prepare all TTS tasks first
    for i, (start_time, text) in enumerate(narration_timed):
        if not text.strip():
            temp_files.append(None)
            continue
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_files.append(tf.name)
        engine.save_to_file(text, tf.name)
        tf.close()

    # Only call runAndWait once
    engine.runAndWait()

    # Combine audio segments
    combined = AudioSegment.silent(duration=0)
    current_time = 0.0

    for i, (start_time, text) in enumerate(narration_timed):
        if not text.strip() or temp_files[i] is None:
            continue
        try:
            segment = AudioSegment.from_wav(temp_files[i])
        except Exception as e:
            print(f"[ERROR] Could not load audio segment {temp_files[i]}: {e}")
            continue
        silence_duration = max(0, (start_time - current_time) * 1000)
        combined += AudioSegment.silent(duration=silence_duration)
        combined += segment
        current_time = start_time + segment.duration_seconds

    combined.export(output_path, format="mp3")

    for f in temp_files:
        if f and os.path.exists(f):
            os.remove(f)