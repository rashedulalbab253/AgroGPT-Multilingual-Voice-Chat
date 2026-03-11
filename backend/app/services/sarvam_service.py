import requests
from sarvamai import SarvamAI
from ..core.config import settings
from ..core.logger import logger
from ..models.schemas import ChatRequest, ChatResponse, TranslateRequest, TranslateResponse
from fastapi import HTTPException

# Initialize SarvamAI client safely
try:
    sarvam_client = SarvamAI(api_subscription_key=settings.SARVAM_API_KEY)
except Exception as e:
    logger.error(f"Error initializing SarvamAI client: {e}")
    sarvam_client = None

LANGUAGES_MAP = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Gujarati": "gu-IN",
    "Bengali": "bn-IN",
    "Kannada": "kn-IN",
    "Punjabi": "pa-IN"
}

def get_language_code(lang_name: str) -> str:
    code = LANGUAGES_MAP.get(lang_name)
    if not code:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported language: {lang_name}. Available: {', '.join(LANGUAGES_MAP.keys())}"
        )
    return code

from sqlalchemy.orm import Session
from ..models.db_models import ChatSession, ChatMessage

# ... (inside file after imports)

async def process_chat(request: ChatRequest, db: Session) -> ChatResponse:
    target_lang_code = get_language_code(request.target_language)
    
    # Ensure session exists
    session = db.query(ChatSession).filter(ChatSession.session_id == request.session_id).first()
    if not session:
        session = ChatSession(session_id=request.session_id, language=request.target_language)
        db.add(session)
        db.commit()

    # Save user message (assuming the last message is the new user one)
    if request.messages:
        user_msg = request.messages[-1]
        db_user_msg = ChatMessage(session_id=request.session_id, role=user_msg.role, content=user_msg.content)
        db.add(db_user_msg)
        db.commit()

    headers = {
        "Authorization": f"Bearer {settings.SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Payload for Sarvam
    # Enforce strict System Prompt to keep it focused on Agriculture
    final_messages = [{"role": "system", "content": settings.AGRO_SYSTEM_PROMPT}]
    
    for msg in request.messages:
        if msg.role != "system": # Skip client-provided system prompts
            final_messages.append(msg.model_dump())

    payload = {
        "model": "sarvam-m",
        "messages": final_messages
    }
    
    try:
        response = requests.post(settings.SARVAM_CHAT_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        assistant_reply = data["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Sarvam API Request Failed: {e}", exc_info=True)
        raise HTTPException(status_code=502, detail="Error communicating with AI provider")
    except (KeyError, IndexError) as e:
        logger.error(f"Sarvam API Unexpected Response: {e}", exc_info=True)
        raise HTTPException(status_code=502, detail="Invalid response from AI provider")

    # Translation
    final_reply = assistant_reply
    if target_lang_code != "en-IN":
        final_reply = _translate_text(assistant_reply, "en-IN", target_lang_code)

    # Save Assistant message
    db_assistant_msg = ChatMessage(session_id=request.session_id, role="assistant", content=final_reply)
    db.add(db_assistant_msg)
    db.commit()

    return ChatResponse(reply=final_reply)

async def process_translation(request: TranslateRequest) -> TranslateResponse:
    source_code = get_language_code(request.source_language)
    target_code = get_language_code(request.target_language)
    
    translated_text = _translate_text(request.text, source_code, target_code)
    return TranslateResponse(translated_text=translated_text)

def _translate_text(text: str, source_code: str, target_code: str) -> str:
    if not sarvam_client:
        logger.error("Sarvam Client is not initialized for translation")
        return text # Fallback to original
        
    try:
        translation = sarvam_client.text.translate(
            input=text,
            source_language_code=source_code,
            target_language_code=target_code,
            speaker_gender="Male"
        )
        return translation.translated_text
    except Exception as e:
        logger.error(f"Translation failed: {e}", exc_info=True)
        return text # Fallback to original

async def transcribe_audio(file_content: bytes, language_code: str) -> str:
    if not sarvam_client:
        logger.error("Sarvam Client is not initialized for transcription")
        raise HTTPException(status_code=500, detail="Transcription service unavailable")

    if not file_content or len(file_content) < 100:
        logger.error(f"Audio content too small: {len(file_content) if file_content else 0} bytes")
        raise HTTPException(status_code=400, detail="Audio recording is too short or empty")

    logger.info(f"Received audio: {len(file_content)} bytes, target lang: {language_code}")

    try:
        import io
        
        # --- Detect audio format from magic bytes ---
        def detect_format(data: bytes) -> str:
            if data[:4] == b'\x1aE\xdf\xa3':
                return "webm"
            elif data[:4] == b'RIFF':
                return "wav"
            elif data[:4] == b'OggS':
                return "ogg"
            elif data[4:8] == b'ftyp':
                return "mp4"
            else:
                return "webm"  # Default assumption for browser recordings

        detected_format = detect_format(file_content)
        logger.info(f"Detected audio format: {detected_format}")

        audio_file = None
        audio_file_name = "audio.wav"

        # --- Audio Format Conversion ---
        # Browsers record audio as WebM (Opus codec), but Sarvam ASR expects WAV.
        # We use pydub to convert the raw audio bytes into a proper WAV format.
        try:
            from pydub import AudioSegment
            audio_io = io.BytesIO(file_content)
            audio_segment = AudioSegment.from_file(audio_io, format=detected_format)
            # Convert to 16kHz mono WAV — standard ASR input format
            audio_segment = audio_segment.set_frame_rate(16000).set_channels(1).set_sample_width(2)
            wav_io = io.BytesIO()
            audio_segment.export(wav_io, format="wav")
            wav_io.seek(0)
            audio_file = wav_io
            audio_file_name = "audio.wav"
            logger.info(f"Audio successfully converted from {detected_format} to WAV ({wav_io.getbuffer().nbytes} bytes)")
        except ImportError:
            logger.warning("pydub not installed, sending raw audio as fallback")
            audio_file = io.BytesIO(file_content)
            audio_file_name = f"audio.{detected_format}"
        except Exception as conv_err:
            logger.warning(f"Audio conversion from {detected_format} failed: {conv_err}, trying raw upload")
            audio_file = io.BytesIO(file_content)
            audio_file_name = f"audio.{detected_format}"

        # Attach a name attribute so the Sarvam SDK can detect the format
        audio_file.name = audio_file_name

        # Sarvam ASR SDK call
        logger.info(f"Calling Sarvam ASR with file: {audio_file_name}, lang: {language_code}")
        response = sarvam_client.speech_to_text.transcribe(
            file=audio_file,
            model="saarika:v2.5",
            language_code=language_code
        )
        
        transcript = response.transcript if response and hasattr(response, 'transcript') else ""
        
        if not transcript or not transcript.strip():
            logger.warning("Sarvam ASR returned empty transcript")
            raise HTTPException(status_code=422, detail="Could not recognize speech. Please speak clearly and try again.")
        
        logger.info(f"Transcription successful: '{transcript[:50]}...'")
        return transcript
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        logger.error(f"Transcription failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Voice recognition failed. Please try again.")
