import unittest
from src.aligner import align_narration

class TestAlignNarration(unittest.TestCase):
    def test_basic_alignment(self):
        narration = ["Story part 1", "Story part 2", "Story part 3"]
        scenes = [(0.0, 5.0), (5.0, 10.0), (10.0, 15.0)]

        aligned = align_narration(narration, scenes)
        expected = [(0.0, "Story part 1"), (5.0, "Story part 2"), (10.0, "Story part 3")]

        self.assertEqual(aligned, expected)

    def test_more_narration_than_scenes(self):
        narration = ["One", "Two", "Three", "Four"]
        scenes = [(0.0, 5.0), (5.0, 10.0)]

        aligned = align_narration(narration, scenes)
        expected = [(0.0, "One"), (5.0, "Two"), (0.0, "Three"), (0.0, "Four")]

        self.assertEqual(aligned, expected)

if __name__ == "__main__":
    unittest.main()
