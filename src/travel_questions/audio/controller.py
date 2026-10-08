from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status
from fastapi.responses import Response

from . import service

voice_router = APIRouter(tags=["travel voice"])

MAX_AUDIO_BYTES = 20 * 1024 * 1024
SUPPORTED_AUDIO_EXTENSIONS = {".mp4", ".webm"}
MIME_EXTENSIONS = {
    "audio/mp4": ".mp4",
    "audio/webm": ".webm",
}


async def _read_audio_upload(audio: UploadFile) -> tuple[bytes, str]:
    """Validate and read a browser recording sent as multipart field ``audio``."""
    filename_extension = Path(audio.filename or "").suffix.lower()
    content_type = (audio.content_type or "").split(";")[0].lower()
    extension = (
        filename_extension
        if filename_extension in SUPPORTED_AUDIO_EXTENSIONS
        else MIME_EXTENSIONS.get(content_type)
    )
    if extension not in SUPPORTED_AUDIO_EXTENSIONS:
        await audio.close()
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Upload an audio/mp4 or audio/webm recording.",
        )

    try:
        audio_bytes = await audio.read(MAX_AUDIO_BYTES + 1)
    finally:
        await audio.close()

    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded audio file is empty.",
        )
    if len(audio_bytes) > MAX_AUDIO_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Audio files must be 20 MB or smaller.",
        )

    return audio_bytes, extension


def _map_audio_error(exc: Exception) -> HTTPException:
    if isinstance(exc, ValueError):
        return HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        )
    return HTTPException(
        status_code=status.HTTP_502_BAD_GATEWAY,
        detail="Could not transcribe the recording or generate a travel response.",
    )


@voice_router.post("/voice", status_code=status.HTTP_200_OK)
async def receive_audio(
    audio: UploadFile = File(...),
    conversation_id: str | None = Form(default=None),
):
    """Transcribe an upload and return the agent response and transcript as JSON."""
    audio_bytes, extension = await _read_audio_upload(audio)
    try:
        return await service.ask_audio_question(
            audio_bytes,
            extension,
            conversation_id,
        )
    except ValueError as exc:
        raise _map_audio_error(exc) from exc
    except Exception as exc:
        raise _map_audio_error(exc) from exc


@voice_router.post("/travel/ask-audio", status_code=status.HTTP_200_OK)
async def ask_audio_and_return_speech(
    audio: UploadFile = File(...),
    conversation_id: str | None = Form(default=None),
):
    """Transcribe audio, ask the text agent, and return its answer as MP3."""
    audio_bytes, extension = await _read_audio_upload(audio)
    try:
        mp3_bytes, result = await service.ask_audio_question_with_audio(
            audio_bytes,
            extension,
            conversation_id,
        )
    except ValueError as exc:
        raise _map_audio_error(exc) from exc
    except Exception as exc:
        raise _map_audio_error(exc) from exc

    return Response(
        content=mp3_bytes,
        media_type="audio/mpeg",
        headers={"X-Conversation-Id": result["conversation_id"]},
    )
