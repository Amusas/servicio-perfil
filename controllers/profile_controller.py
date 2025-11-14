from fastapi import HTTPException, status, Depends
from typing import Dict, Any
from models.profile import ProfileUpdate, ProfileResponse
from repositories.profile_repository import ProfileRepository
from middleware.jwt_middleware import verify_token
from logger.logger import info, error, warn


class ProfileController:
    def __init__(self):
        self.repository = ProfileRepository()
    
    def get_profile(self, user_id: int, token_data: Dict[str, Any] = Depends(verify_token)) -> ProfileResponse:
        """Get profile for authenticated user"""
        controller = "[ProfileController]"
        info(controller, "Obteniendo perfil", {"userId": user_id})
        
        # Verify user can only access their own profile
        token_user_id = token_data["user_id"]
        if token_user_id != user_id:
            warn(controller, "Intento de acceso no autorizado", {
                "tokenUserId": token_user_id,
                "requestedUserId": user_id
            })
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este perfil"
            )
        
        try:
            profile = self.repository.find_by_user_id(user_id)
            
            if not profile:
                error(controller, "Perfil no encontrado", {"userId": user_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil no encontrado"
                )
            
            info(controller, "Perfil obtenido exitosamente", {"userId": user_id})
            return ProfileResponse(**profile)
            
        except HTTPException:
            raise
        except Exception as e:
            error(controller, "Error obteniendo perfil", {
                "userId": user_id,
                "error": str(e)
            })
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno obteniendo perfil"
            )
    
    def update_profile(
        self,
        user_id: int,
        profile_update: ProfileUpdate,
        token_data: Dict[str, Any] = Depends(verify_token)
    ) -> ProfileResponse:
        """Update profile for authenticated user"""
        controller = "[ProfileController]"
        info(controller, "Actualizando perfil", {"userId": user_id})
        
        # Verify user can only update their own profile
        token_user_id = token_data["user_id"]
        if token_user_id != user_id:
            warn(controller, "Intento de actualización no autorizada", {
                "tokenUserId": token_user_id,
                "requestedUserId": user_id
            })
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para actualizar este perfil"
            )
        
        try:
            # Check if profile exists
            existing_profile = self.repository.find_by_user_id(user_id)
            if not existing_profile:
                error(controller, "Perfil no encontrado para actualizar", {"userId": user_id})
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Perfil no encontrado"
                )
            
            # Prepare update data (only include non-None fields)
            update_data = {}
            if profile_update.personal_url is not None:
                update_data["personal_url"] = profile_update.personal_url
            if profile_update.nickname is not None:
                update_data["nickname"] = profile_update.nickname
            if profile_update.is_contact_public is not None:
                update_data["is_contact_public"] = profile_update.is_contact_public
            if profile_update.mailing_address is not None:
                update_data["mailing_address"] = profile_update.mailing_address
            if profile_update.biography is not None:
                update_data["biography"] = profile_update.biography
            if profile_update.organization is not None:
                update_data["organization"] = profile_update.organization
            if profile_update.country is not None:
                update_data["country"] = profile_update.country
            if profile_update.social_links is not None:
                update_data["social_links"] = profile_update.social_links
            
            if not update_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No hay campos para actualizar"
                )
            
            # Update profile
            updated_profile = self.repository.update(user_id, update_data)
            
            info(controller, "Perfil actualizado exitosamente", {"userId": user_id})
            return ProfileResponse(**updated_profile)
            
        except HTTPException:
            raise
        except Exception as e:
            error(controller, "Error actualizando perfil", {
                "userId": user_id,
                "error": str(e)
            })
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error interno actualizando perfil: {str(e)}"
            )

