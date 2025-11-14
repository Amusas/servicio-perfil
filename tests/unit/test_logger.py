# tests/unit/test_logger.py
import pytest
import json
from unittest.mock import patch
from logger.logger import info, debug, warn, error, log


@pytest.mark.unit
class TestLogger:
    """Test logger functions"""

    def test_log_info(self, capsys):
        """Test info logging"""
        info("TestLogger", "Test info message", {"key": "value"})
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["level"] == "info"
        assert log_data["logger"] == "TestLogger"
        assert log_data["message"] == "Test info message"
        assert log_data["key"] == "value"
        assert "timestamp" in log_data
        assert "thread" in log_data

    def test_log_debug(self, capsys):
        """Test debug logging"""
        debug("TestLogger", "Debug message")
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["level"] == "debug"
        assert log_data["message"] == "Debug message"

    def test_log_warn(self, capsys):
        """Test warn logging"""
        warn("TestLogger", "Warning message", {"code": "WARN001"})
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["level"] == "warn"
        assert log_data["code"] == "WARN001"

    def test_log_error(self, capsys):
        """Test error logging"""
        error("TestLogger", "Error message", {"error": "Something went wrong"})
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["level"] == "error"
        assert log_data["error"] == "Something went wrong"

    def test_log_without_metadata(self, capsys):
        """Test logging without metadata"""
        info("TestLogger", "Simple message")
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["level"] == "info"
        assert log_data["message"] == "Simple message"

    def test_log_with_complex_metadata(self, capsys):
        """Test logging with complex metadata"""
        meta = {
            "userId": 123,
            "action": "update_profile",
            "changes": {"name": "John", "age": 30}
        }

        info("TestLogger", "Complex log", meta)
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert log_data["userId"] == 123
        assert log_data["action"] == "update_profile"
        assert log_data["changes"] == {"name": "John", "age": 30}

    def test_timestamp_format(self, capsys):
        """Test timestamp format"""
        info("TestLogger", "Test")
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())
        timestamp = log_data["timestamp"]

        # Should end with 'Z' for UTC
        assert timestamp.endswith('Z')
        # Should be valid ISO format
        assert 'T' in timestamp

    def test_thread_id_is_string(self, capsys):
        """Test thread ID is string"""
        info("TestLogger", "Test")
        captured = capsys.readouterr()

        log_data = json.loads(captured.out.strip())

        assert isinstance(log_data["thread"], str)
        assert len(log_data["thread"]) > 0