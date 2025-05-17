import os
from typing import List
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_narration(scene_descriptions: List[str]) -> List[str]:
    """
    Convert scene descriptions into a cohesive, engaging narration story.
    Returns a list of narration paragraphs corresponding to each scene.
    """

    prompt = (
        "You are a creative storyteller. Given a sequence of scene descriptions from an animated short film, "
        "write an engaging narration, like in movies, for each scene that tells the story emotionally and dynamically. "
        "Avoid literal captions; instead, create a flowing narrative that feels like a rich audiobook.\n\n"
        "Scenes:\n"
    )
    for i, desc in enumerate(scene_descriptions, 1):
        prompt += f"Scene {i}: {desc}\n"

    prompt += "\nNarration:\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a master storyteller."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=600,
        n=1,
    )

    narration_text = response.choices[0].message.content.strip()

    # Remove leading "Narration" if present
    if narration_text.lower().startswith("narration"):
        narration_text = narration_text.split("\n", 1)[-1].strip()

    # Split narration by scene assuming paragraphs separated by double newlines
    narration_segments = [seg.strip() for seg in narration_text.split("\n\n") if seg.strip()]

    # If output segments are fewer than scenes, pad with empty strings
    if len(narration_segments) < len(scene_descriptions):
        narration_segments += [""] * (len(scene_descriptions) - len(narration_segments))

    return narration_segments
