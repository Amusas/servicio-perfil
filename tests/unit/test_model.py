# tests/unit/test_models.py
import pytest
from datetime import datetime
from pydantic import ValidationError
from models.profile import ProfileUpdate, ProfileResponse, ErrorResponse


@pytest.mark.unit
class TestProfileUpdate:
    """Test ProfileUpdate model"""

    def test_create_empty_profile_update(self):
        """Test creating profile update with no fields"""
        update = ProfileUpdate()

        assert update.personal_url is None
        assert update.nickname is None
        assert update.is_contact_public is None

    def test_create_profile_update_with_all_fields(self):
        """Test creating profile update with all fields"""
        update = ProfileUpdate(
            personal_url="https://example.com",
            nickname="testuser",
            is_contact_public=True,
            mailing_address="123 Test St",
            biography="Test bio",
            organization="Test Org",
            country="Colombia",
            social_links={"twitter": "https://twitter.com/test"}
        )

        assert update.personal_url == "https://example.com"
        assert update.nickname == "testuser"
        assert update.is_contact_public is True
        assert update.mailing_address == "123 Test St"
        assert update.biography == "Test bio"
        assert update.organization == "Test Org"
        assert update.country == "Colombia"
        assert update.social_links == {"twitter": "https://twitter.com/test"}

    def test_create_profile_update_partial_fields(self):
        """Test creating profile update with partial fields"""
        update = ProfileUpdate(
            nickname="newname",
            country="Argentina"
        )

        assert update.nickname == "newname"
        assert update.country == "Argentina"
        assert update.personal_url is None

    def test_profile_update_validates_max_length(self):
        """Test max length validation"""
        with pytest.raises(ValidationError):
            ProfileUpdate(personal_url="https://" + "a" * 500)

    def test_profile_update_accepts_dict_for_social_links(self):
        """Test social_links accepts dictionary"""
        update = ProfileUpdate(
            social_links={
                "twitter": "https://twitter.com/user",
                "linkedin": "https://linkedin.com/in/user"
            }
        )

        assert len(update.social_links) == 2
        assert "twitter" in update.social_links


@pytest.mark.unit
class TestProfileResponse:
    """Test ProfileResponse model"""

    def test_create_profile_response(self):
        """Test creating profile response"""
        now = datetime.utcnow()

        response = ProfileResponse(
            id=1,
            user_id=1,
            personal_url="https://example.com",
            nickname="testuser",
            is_contact_public=True,
            mailing_address="123 Test St",
            biography="Test bio",
            organization="Test Org",
            country="Colombia",
            social_links={"twitter": "https://twitter.com/test"},
            created_at=now,
            updated_at=now
        )

        assert response.id == 1
        assert response.user_id == 1
        assert response.nickname == "testuser"
        assert response.is_contact_public is True

    def test_profile_response_requires_mandatory_fields(self):
        """Test that mandatory fields are required"""
        with pytest.raises(ValidationError):
            ProfileResponse()

    def test_profile_response_with_null_optional_fields(self):
        """Test profile response with null optional fields"""
        now = datetime.utcnow()

        response = ProfileResponse(
            id=1,
            user_id=1,
            personal_url=None,
            nickname=None,
            is_contact_public=False,
            mailing_address=None,
            biography=None,
            organization=None,
            country=None,
            social_links={},
            created_at=now,
            updated_at=now
        )

        assert response.personal_url is None
        assert response.nickname is None
        assert response.social_links == {}

    def test_profile_response_datetime_fields(self):
        """Test datetime fields"""
        now = datetime.utcnow()

        response = ProfileResponse(
            id=1,
            user_id=1,
            is_contact_public=True,
            social_links={},
            created_at=now,
            updated_at=now
        )

        assert isinstance(response.created_at, datetime)
        assert isinstance(response.updated_at, datetime)


@pytest.mark.unit
class TestErrorResponse:
    """Test ErrorResponse model"""

    def test_create_error_response(self):
        """Test creating error response"""
        error = ErrorResponse(
            message="Test error",
            timestamp="2024-01-01T00:00:00Z"
        )

        assert error.success is False
        assert error.message == "Test error"
        assert error.timestamp == "2024-01-01T00:00:00Z"

    def test_error_response_default_success_false(self):
        """Test that success defaults to False"""
        error = ErrorResponse(
            message="Error",
            timestamp="2024-01-01T00:00:00Z"
        )

        assert error.success is False