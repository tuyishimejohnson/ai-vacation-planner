from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi.concurrency import run_in_threadpool

from ...audio.convert_audio_to_text import transcribe_audio
from ...audio.convert_text_to_audio import convert_text_to_audio_bytes
from ..text.service import ask_travel_question


async def ask_audio_question(
    audio_bytes: bytes,
    extension: str,
    conversation_id: str | None = None,
) -> dict:
    """Transcribe an audio upload and pass the transcript to the travel agent."""
    temp_path: Path | None = None
    try:
        with NamedTemporaryFile(suffix=extension, delete=False) as temp_file:
            temp_file.write(audio_bytes)
            temp_path = Path(temp_file.name)

        transcript = await run_in_threadpool(transcribe_audio, temp_path)
        print(f"Transcribed audio: {transcript}", flush=True)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)

    if not transcript:
        raise ValueError("No speech was detected in the audio.")

    result = await ask_travel_question(transcript, conversation_id)
    print(f"Agent response: {result['answer']}", flush=True)
    return {"transcript": transcript, **result}


async def ask_audio_question_with_audio(
    audio_bytes: bytes,
    extension: str,
    conversation_id: str | None = None,
) -> tuple[bytes, dict]:
    """Ask the text agent with a transcript and speak its answer as MP3."""
    result = await ask_audio_question(audio_bytes, extension, conversation_id)
    audio_response = await run_in_threadpool(convert_text_to_audio, result["answer"])

    return audio_response, result


def convert_text_to_audio(text: str) -> bytes:
    """Create an MP3 response for the supplied text."""
    return convert_text_to_audio_bytes(text)
