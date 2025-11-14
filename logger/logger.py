import json
import os
from datetime import datetime
from typing import Any, Dict, Optional


def log(level: str, logger: str, message: str, meta: Optional[Dict[str, Any]] = None):
    """Log function that outputs JSON formatted logs"""
    if meta is None:
        meta = {}
    
    payload = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "logger": logger,
        "message": message,
        "thread": str(os.getpid()),
        **meta
    }
    print(json.dumps(payload))


def info(logger: str, message: str, meta: Optional[Dict[str, Any]] = None):
    log("info", logger, message, meta)


def debug(logger: str, message: str, meta: Optional[Dict[str, Any]] = None):
    log("debug", logger, message, meta)


def warn(logger: str, message: str, meta: Optional[Dict[str, Any]] = None):
    log("warn", logger, message, meta)


def error(logger: str, message: str, meta: Optional[Dict[str, Any]] = None):
    log("error", logger, message, meta)

