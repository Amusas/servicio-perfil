# tests/unit/test_repository.py
import pytest
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime

# Import will work because psycopg2 is mocked in conftest.py
from repositories.profile_repository import ProfileRepository


@pytest.mark.unit
class TestProfileRepository:
    """Test ProfileRepository"""

    def test_find_by_user_id_found(self):
        """Test finding profile by user_id when it exists"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            now = datetime.utcnow()
            mock_cursor.fetchone.return_value = (
                1,  # id
                1,  # user_id
                "https://example.com",  # personal_url
                "testuser",  # nickname
                True,  # is_contact_public
                "123 Test St",  # mailing_address
                "Test bio",  # biography
                "Test Org",  # organization
                "Colombia",  # country
                {"twitter": "https://twitter.com/test"},  # social_links
                now,  # created_at
                now  # updated_at
            )

            # Execute
            repo = ProfileRepository()
            profile = repo.find_by_user_id(1)

            # Assert
            assert profile is not None
            assert profile["id"] == 1
            assert profile["user_id"] == 1
            assert profile["nickname"] == "testuser"
            assert profile["is_contact_public"] is True
            assert profile["social_links"] == {"twitter": "https://twitter.com/test"}

            mock_cursor.execute.assert_called_once()
            mock_cursor.close.assert_called_once()

    def test_find_by_user_id_not_found(self):
        """Test finding profile by user_id when it doesn't exist"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            mock_cursor.fetchone.return_value = None

            # Execute
            repo = ProfileRepository()
            profile = repo.find_by_user_id(999)

            # Assert
            assert profile is None

    def test_find_by_user_id_with_null_social_links(self):
        """Test finding profile with null social_links"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            now = datetime.utcnow()
            mock_cursor.fetchone.return_value = (
                1, 1, "https://example.com", "testuser", True,
                "123 Test St", "Test bio", "Test Org", "Colombia",
                None,  # social_links is NULL
                now, now
            )

            # Execute
            repo = ProfileRepository()
            profile = repo.find_by_user_id(1)

            # Assert
            assert profile["social_links"] == {}

    def test_update_profile_success(self):
        """Test updating profile successfully"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            now = datetime.utcnow()
            mock_cursor.fetchone.return_value = (
                1, 1, "https://newurl.com", "newname", True,
                "456 New St", "New bio", "New Org", "Argentina",
                {"twitter": "https://twitter.com/new"},
                now, now
            )

            # Execute
            repo = ProfileRepository()
            update_data = {
                "nickname": "newname",
                "country": "Argentina"
            }
            profile = repo.update(1, update_data)

            # Assert
            assert profile is not None
            assert profile["nickname"] == "newname"
            assert profile["country"] == "Argentina"

            mock_cursor.execute.assert_called_once()
            mock_conn.commit.assert_called_once()

    def test_update_profile_all_fields(self):
        """Test updating all profile fields"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            now = datetime.utcnow()
            mock_cursor.fetchone.return_value = (
                1, 1, "https://new.com", "newnick", False,
                "789 St", "New bio", "New Org", "Chile",
                {"linkedin": "https://linkedin.com"},
                now, now
            )

            # Execute
            repo = ProfileRepository()
            update_data = {
                "personal_url": "https://new.com",
                "nickname": "newnick",
                "is_contact_public": False,
                "mailing_address": "789 St",
                "biography": "New bio",
                "organization": "New Org",
                "country": "Chile",
                "social_links": {"linkedin": "https://linkedin.com"}
            }
            profile = repo.update(1, update_data)

            # Assert
            assert profile["nickname"] == "newnick"
            assert profile["country"] == "Chile"
            assert profile["is_contact_public"] is False

    def test_update_profile_not_found(self):
        """Test updating profile that doesn't exist"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            mock_cursor.fetchone.return_value = None

            # Execute & Assert
            repo = ProfileRepository()
            with pytest.raises(ValueError, match="Profile not found"):
                repo.update(999, {"nickname": "test"})

            mock_conn.rollback.assert_called_once()

    def test_update_profile_database_error(self):
        """Test handling database errors during update"""
        with patch('repositories.profile_repository.db_config') as mock_db_config:
            mock_conn = MagicMock()
            mock_cursor = MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_db_config.get_connection.return_value = mock_conn

            mock_cursor.execute.side_effect = Exception("Database error")

            # Execute & Assert
            repo = ProfileRepository()
            with pytest.raises(Exception, match="Database error"):
                repo.update(1, {"nickname": "test"})

            mock_conn.rollback.assert_called_once()