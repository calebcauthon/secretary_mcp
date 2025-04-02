from mcp.server.fastmcp import FastMCP
import subprocess
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import assemblyai as aai
import os
from text_pointer import create_text_pointer, TextPointer

mcp = FastMCP("AssemblyAI")

@dataclass
class Word:
    text: str
    start: float
    end: float
    speaker: Optional[str] = None

@dataclass
class TranscriptionResult:
    language_code: str
    confidence: float
    transcript_file_path: str

@mcp.tool()
def extract_audio_from_video(video_path: str) -> str:
    """Extract audio from video file using ffmpeg, return a local path to the resulting audio file"""
    audio_path = str(Path(video_path).with_suffix('.mp3'))
    
    print(f"🎬 Extracting audio from {Path(video_path).name}...")
    
    # Run ffmpeg command
    result = subprocess.run(
        ['ffmpeg', '-i', video_path, '-vn', '-acodec', 'libmp3lame', '-y', audio_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        raise Exception(f"Failed to extract audio: {result.stderr}")
    
    print(f"🎵 Saved audio to {Path(audio_path).name}")
    return audio_path

@mcp.tool()
def transcribe_audio_to_text(file_path: str) -> TranscriptionResult:
    """
    Transcribe audio using AssemblyAI
    Parameters:
        file_path: str - The path to the mp3 audio file to transcribe
    Returns:
        TranscriptionResult - A dataclass containing the transcription result
            - transcript: List[dict] - A diarized transcript with speaker labels
            - language_code: str - The language code of the transcription
            - confidence: float - The confidence score of the transcription
            - transcript_file_path: str - The path to the diarized transcript file
    """
    # If it's an MP4, extract audio first
    audio_path = file_path
    if file_path.endswith('.mp4') or file_path.endswith('.mkv') or file_path.endswith('.mov'):
        audio_path = extract_audio_from_video(file_path)
    
    print(f"🎙️ Starting transcription...")
    
    # Initialize AssemblyAI
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise Exception("❌ ASSEMBLYAI_API_KEY environment variable not set")
    
    # Configure transcription parameters
    config = aai.TranscriptionConfig(
        speaker_labels=True
    )

    print("⚙️ Sending to AssemblyAI...")
    
    transcript = aai.Transcriber().transcribe(
        audio_path,
        config=config
    )
    print("✨ Received transcription")
    
    # Convert to our format
    words = []
    for utterance in transcript.utterances:
        words.append(Word(
            text=utterance.text,
            start=utterance.start / 1000,  # Convert to seconds
            end=utterance.end / 1000,
            speaker=f"speaker_{utterance.speaker}"
        ))

    diarized_transcript = [
        {
            'text': word.text,
            'start': word.start * 1000,  # Convert back to milliseconds
            'end': word.end * 1000,
            'speaker': word.speaker,
            'speaker_name': word.speaker  # Initial name same as ID
        }
        for word in words
    ]
    
    # Generate output filename based on input file
    input_path = Path(audio_path)
    output_filename = f"{input_path.stem}_transcript.txt"
    output_path = input_path.parent / output_filename
    
    # Write the diarized transcript to a text file
    with open(output_path, "w") as f:
        for entry in diarized_transcript:
            f.write(f"{entry['speaker_name']}: {entry['text']}\n")
    print(f"📝 Diarized transcript written to {output_path}")

    return TranscriptionResult(
        language_code="en",  # AssemblyAI defaults to English
        confidence=1.0,  # AssemblyAI doesn't provide this
        transcript_file_path=str(output_path),
    )

if __name__ == "__main__":
    mcp.run()