# Animated Video Narration Pipeline

This project automatically generates engaging narration for an input video by extracting scenes, analyzing visuals, generating a story with a language model, synthesizing narration audio, and muxing it with the original video.

---

## Features

- Scene extraction based on frame difference (OpenCV)
- Visual scene analysis with BLIP-2 vision-language model (Transformers)
- Story narration generation using OpenAI GPT-4o-mini
- Text-to-speech audio synthesis (pyttsx3 or Pydub-based)
- Audio and video muxing with ffmpeg-python

---

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/animated-narration.git
   cd animated-narration
2. Create and activate a Python virtual environment:
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
3. Install requirements:
    pip install -r requirements.txt
4. Set your OpenAI API key in a .env file:
    OPENAI_API_KEY=your_api_key_here

---

## Usage

Run the pipeline on a video file:

```bash
python main.py --video_path path/to/video.mp4 --output_dir output
```

---

## Project Structure

- `src/video_utils.py`: Scene extraction from video  
- `src/video_analysis.py`: Scene visual description with BLIP-2  
- `src/llm_storygen.py`: Generate narration using GPT-4o-mini  
- `src/aligner.py`: Align narration text to scene timestamps  
- `src/tts_engine.py`: Synthesize speech audio from narration  
- `src/muxer.py`: Combine audio and video with FFmpeg  
- `main.py`: Main pipeline runner script  

---

## Requirements

- Python 3.8+  
- OpenAI API key  
- FFmpeg installed and in your PATH  

---

## Notes

- The BLIP-2 model runs on CPU by default.  
- Ensure FFmpeg is installed for muxing.  
- The project saves intermediate data in `sample_data/`.  
