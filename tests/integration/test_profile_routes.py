# tests/integration/test_profile_routes.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from datetime import datetime
from main import app


client = TestClient(app)


@pytest.mark.integration
class TestProfileRoutes:
    """Test profile API routes"""

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_get_profile_success(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test GET /api/v1/profiles/{user_id} - success"""
        # Setup JWT mock
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']

        # Setup repository mock
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        now = datetime.utcnow()
        mock_repo.find_by_user_id.return_value = {
            "id": 1,
            "user_id": 1,
            "personal_url": "https://example.com",
            "nickname": "testuser",
            "is_contact_public": True,
            "mailing_address": "123 Test St",
            "biography": "Test bio",
            "organization": "Test Org",
            "country": "Colombia",
            "social_links": {"twitter": "https://twitter.com/test"},
            "created_at": now,
            "updated_at": now
        }

        # Execute
        response = client.get(
            "/api/v1/profiles/1",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["user_id"] == 1
        assert data["nickname"] == "testuser"
        assert data["country"] == "Colombia"

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_get_profile_not_found(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test GET profile when it doesn't exist"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.find_by_user_id.return_value = None

        # Execute
        response = client.get(
            "/api/v1/profiles/1",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # Assert
        assert response.status_code == 404
        assert "no encontrado" in response.json()["detail"].lower()

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_get_profile_forbidden_different_user(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test GET profile for different user - should be forbidden"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        # Execute - token has userId=1, but requesting userId=2
        response = client.get(
            "/api/v1/profiles/2",
            headers={"Authorization": f"Bearer {valid_token}"}
        )

        # Assert
        assert response.status_code == 403
        assert "permisos" in response.json()["detail"].lower()

    def test_get_profile_no_token(self):
        """Test GET profile without authentication token"""
        response = client.get("/api/v1/profiles/1")

        assert response.status_code == 403

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_update_profile_success(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test PUT /api/v1/profiles/{user_id} - success"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        now = datetime.utcnow()
        mock_repo.find_by_user_id.return_value = {
            "id": 1, "user_id": 1, "nickname": "oldname",
            "is_contact_public": True, "social_links": {},
            "created_at": now, "updated_at": now
        }

        mock_repo.update.return_value = {
            "id": 1,
            "user_id": 1,
            "personal_url": "https://newurl.com",
            "nickname": "newname",
            "is_contact_public": True,
            "mailing_address": None,
            "biography": "New bio",
            "organization": None,
            "country": "Argentina",
            "social_links": {},
            "created_at": now,
            "updated_at": now
        }

        # Execute
        response = client.put(
            "/api/v1/profiles/1",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={
                "nickname": "newname",
                "biography": "New bio",
                "country": "Argentina"
            }
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["nickname"] == "newname"
        assert data["country"] == "Argentina"
        mock_repo.update.assert_called_once()

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_update_profile_forbidden_different_user(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test PUT profile for different user - should be forbidden"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']

        # Execute - token has userId=1, but updating userId=2
        response = client.put(
            "/api/v1/profiles/2",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={"nickname": "newname"}
        )

        # Assert
        assert response.status_code == 403

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_update_profile_not_found(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test PUT profile when it doesn't exist"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.find_by_user_id.return_value = None

        # Execute
        response = client.put(
            "/api/v1/profiles/1",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={"nickname": "newname"}
        )

        # Assert
        assert response.status_code == 404

    @patch('middleware.jwt_middleware.jwt_config')
    @patch('controllers.profile_controller.ProfileRepository')
    def test_update_profile_empty_data(self, mock_repo_class, mock_jwt_config, rsa_keys, valid_token):
        """Test PUT profile with empty data"""
        # Setup mocks
        mock_jwt_config.get_public_key.return_value = rsa_keys['public_key']
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo

        now = datetime.utcnow()
        mock_repo.find_by_user_id.return_value = {
            "id": 1, "user_id": 1, "nickname": "test",
            "is_contact_public": True, "social_links": {},
            "created_at": now, "updated_at": now
        }

        # Execute
        response = client.put(
            "/api/v1/profiles/1",
            headers={"Authorization": f"Bearer {valid_token}"},
            json={}
        )

        # Assert
        assert response.status_code == 400
        assert "no hay campos" in response.json()["detail"].lower()