from io import BytesIO
from pathlib import Path

from gtts import gTTS

DEFAULT_OUTPUT_FILE = Path(__file__).resolve().parent / "converted_text" / "output.mp3"


def convert_text_to_audio_bytes(text: str) -> bytes:
    """Convert text to MP3 audio in memory, without sharing output files."""
    output = BytesIO()
    gTTS(text=text, lang="en").write_to_fp(output)
    return output.getvalue()


def convert_text_to_audio(
    text: str, output_file: str | Path = DEFAULT_OUTPUT_FILE
) -> None:
    """Convert text to audio using gTTS and save it as an MP3 file."""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(convert_text_to_audio_bytes(text))
