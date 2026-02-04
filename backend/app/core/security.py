from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from .config import settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(API_KEY_HEADER)):
    if api_key == settings.MASTER_API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )
