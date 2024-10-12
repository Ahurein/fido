from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from typing import Optional, Any

class ApiResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None

def success_response(data: Any = None, message: str = "Request successful"):
    return ApiResponse(success=True, data=data, message=message)

def error_response(message: str = "An error occurred", status_code: int = 400):
    raise HTTPException(status_code=status_code, detail={"success": False, "message": message})