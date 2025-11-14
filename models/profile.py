from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class ProfileUpdate(BaseModel):
    personal_url: Optional[str] = Field(None, max_length=500, description="URL de página personal")
    nickname: Optional[str] = Field(None, max_length=100, description="Apodo del usuario")
    is_contact_public: Optional[bool] = Field(None, description="Si la información de contacto es pública")
    mailing_address: Optional[str] = Field(None, description="Dirección de correspondencia")
    biography: Optional[str] = Field(None, description="Biografía del usuario")
    organization: Optional[str] = Field(None, max_length=200, description="Organización a la que pertenece")
    country: Optional[str] = Field(None, max_length=100, description="País de residencia")
    social_links: Optional[Dict[str, str]] = Field(None, description="Links de redes sociales")


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    personal_url: Optional[str] = None
    nickname: Optional[str] = None
    is_contact_public: bool
    mailing_address: Optional[str] = None
    biography: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    social_links: Dict[str, str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    timestamp: str

