
import unittest
import os
from src.main import process_video

class TestIntegration(unittest.TestCase):
    def test_full_pipeline(self):
        video_path = "sample_data/sample_video2.mp4"
        output_dir = "sample_data/test_output"

        narration_timed, audio_path, narrated_video_path = process_video(video_path, output_dir)

        self.assertTrue(os.path.exists(audio_path))
        self.assertTrue(os.path.exists(narrated_video_path))
        self.assertTrue(len(narration_timed) > 0)

if __name__ == "__main__":
    unittest.main()
