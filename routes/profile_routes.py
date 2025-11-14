from fastapi import APIRouter, Depends
from typing import Dict, Any
from controllers.profile_controller import ProfileController
from models.profile import ProfileUpdate, ProfileResponse
from middleware.jwt_middleware import verify_token

router = APIRouter(prefix="/api/v1/profiles", tags=["Profiles"])
controller = ProfileController()


@router.get("/{user_id}", response_model=ProfileResponse, status_code=200)
def get_profile(user_id: int, token_data: Dict[str, Any] = Depends(verify_token)):
    """Get profile for a user"""
    return controller.get_profile(user_id, token_data)


@router.put("/{user_id}", response_model=ProfileResponse, status_code=200)
def update_profile(
    user_id: int,
    profile_update: ProfileUpdate,
    token_data: Dict[str, Any] = Depends(verify_token)
):
    """Update profile for a user"""
    return controller.update_profile(user_id, profile_update, token_data)

