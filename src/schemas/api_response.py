from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional, Any

class ApiResponse(BaseModel):
    message: Optional[str] = None
    data: Optional[Any] = None

def success_response(data: Any = None, message: str = "Request successful"):
    return ApiResponse(message=message, data=data)