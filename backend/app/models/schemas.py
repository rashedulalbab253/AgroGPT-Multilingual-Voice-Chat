from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str = Field(..., description="Role of the speaker: 'user', 'assistant', or 'system'")
    content: str = Field(..., description="The text content of the message")

class ChatRequest(BaseModel):
    session_id: str = Field(..., description="Unique ID for the chat session.")
    messages: list[Message] = Field(..., description="The full conversation history to maintain context.")
    target_language: str = Field(..., description="The display name of the desired response language.")

class ChatResponse(BaseModel):
    reply: str = Field(..., description="The final, translated response from the assistant.")
    
class TranslateRequest(BaseModel):
    text: str = Field(..., description="The text to be translated.")
    source_language: str = Field(..., description="The display name of the source language.")
    target_language: str = Field(..., description="The display name of the desired target language.")

class TranslateResponse(BaseModel):
    translated_text: str = Field(..., description="The resulting translated text.")
