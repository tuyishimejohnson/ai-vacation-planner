from functools import lru_cache
from pathlib import Path

import whisper

SUPPORTED_AUDIO_EXTENSIONS = {
    ".mp3",
    ".mp4",
    ".mpeg",
    ".mpga",
    ".m4a",
    ".wav",
    ".webm",
}


TRANSCRIPTION_MODEL = "base"
DEFAULT_AUDIO_PATH = Path(__file__).resolve().parent


@lru_cache(maxsize=2)
def _load_model(model_name: str):
    """Load each Whisper model once for repeated API requests."""
    return whisper.load_model(model_name)


def transcribe_audio(audio_path: Path, model_name: str = TRANSCRIPTION_MODEL) -> str:
    """Transcribe an audio file with the local Whisper model."""
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    if not audio_path.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS:
        raise ValueError(
            f"Unsupported audio format: {audio_path.suffix}. "
            f"Supported formats: {', '.join(SUPPORTED_AUDIO_EXTENSIONS)}"
        )
    model = _load_model(model_name)
    result = model.transcribe(str(audio_path))
    return result.get("text", "").strip()
