import subprocess

def mux_audio_to_video(video_input, narration_audio, output_path):
    mixed_audio = "sample_data/test_output/mixed_audio.mp3"

    # Step 1: Mix original audio and narration into one
    mix_cmd = [
        "ffmpeg", "-y",
        "-i", video_input,
        "-i", narration_audio,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2",
        "-c:a", "libmp3lame", "-q:a", "4",
        mixed_audio
    ]
    subprocess.run(mix_cmd, check=True)

    # Step 2: Mux video + mixed audio
    mux_cmd = [
        "ffmpeg", "-y",
        "-i", video_input,
        "-i", mixed_audio,
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy", "-c:a", "aac",
        output_path
    ]
    subprocess.run(mux_cmd, check=True)
