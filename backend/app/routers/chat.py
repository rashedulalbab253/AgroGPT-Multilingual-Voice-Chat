from fastapi import APIRouter, Security, Request, Depends, File, UploadFile, Form
from ..models.schemas import ChatRequest, ChatResponse, TranslateRequest, TranslateResponse
from ..services import sarvam_service
from ..core.security import get_api_key
from ..core.logger import logger
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from ..core.database import get_db

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, body: ChatRequest, api_key: str = Security(get_api_key), db: Session = Depends(get_db)):
    logger.info(f"Chat request for language: {body.target_language} (Session: {body.session_id})")
    return await sarvam_service.process_chat(body, db)

@router.get("/history/{session_id}")
async def get_history_endpoint(session_id: str, api_key: str = Security(get_api_key), db: Session = Depends(get_db)):
    messages = db.query(sarvam_service.ChatMessage).filter(sarvam_service.ChatMessage.session_id == session_id).all()
    return [{"role": m.role, "content": m.content} for m in messages]

@router.post("/translate", response_model=TranslateResponse)
@limiter.limit("10/minute")
async def translate_endpoint(request: Request, body: TranslateRequest, api_key: str = Security(get_api_key)):
    logger.info(f"Translate request: {body.source_language} -> {body.target_language}")
    return await sarvam_service.process_translation(body)

@router.post("/transcribe")
@limiter.limit("10/minute")
async def transcribe_endpoint(
    request: Request, 
    file: UploadFile = File(...), 
    language_name: str = Form("English"), 
    api_key: str = Security(get_api_key)
):
    logger.info(f"Transcription request for: {language_name}")
    lang_code = sarvam_service.get_language_code(language_name)
    content = await file.read()
    transcript = await sarvam_service.transcribe_audio(content, lang_code)
    return {"transcript": transcript}
