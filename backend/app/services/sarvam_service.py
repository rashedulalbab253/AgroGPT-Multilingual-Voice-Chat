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

    try:
        import io
        audio_file = io.BytesIO(file_content)
        audio_file.name = "audio.wav"
        
        # sarvamai sdk call
        response = sarvam_client.speech_to_text.transcribe(
            file=audio_file,
            model="saarika:v2.5",
            language_code=language_code
        )
        return response.transcript
    except Exception as e:
        logger.error(f"Transcription failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Voice recognition failed")
