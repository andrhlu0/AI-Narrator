from typing import List, Tuple

def align_narration(narration: List[str], scenes: List[Tuple[float, float]]) -> List[Tuple[float, str]]:
    """
    Align narration paragraphs with scene intervals.
    Returns list of (start_time, text) tuples for TTS synthesis.

    Parameters:
    - narration: List of narration paragraphs, one per scene.
    - scenes: List of (start_time, end_time) tuples per scene.

    The output is timed to start exactly at each scene's start time.
    """
    aligned = []
    for i, text in enumerate(narration):
        start_time = scenes[i][0] if i < len(scenes) else 0.0
        aligned.append((start_time, text))
    return aligned
