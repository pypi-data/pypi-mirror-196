"""
Pre-configured logging handlers for manual setup.

Can be specified in logging config dict:
    handlers:
    info_file_handler:
        (): np_logging.handlers.FileHandler
        level: INFO
"""
from __future__ import annotations

import contextlib
import logging
import logging.handlers
import os
import pathlib
import platform
import sys
from typing import Any, Callable, Optional

import np_logging.config

PKG_CONFIG = np_logging.config.PKG_CONFIG

SERVER_BACKUP: dict[str, Any] = PKG_CONFIG["handlers"]["log_server_file_backup"]
SERVER: dict[str, Any] = PKG_CONFIG["handlers"]["log_server"]
CONSOLE: dict[str, Any] = PKG_CONFIG["handlers"]["console"]
FILE: dict[str, Any] = PKG_CONFIG["handlers"]["file"]
EMAIL: dict[str, Any] = PKG_CONFIG["handlers"]["email"]

FORMAT: dict[str, logging.Formatter] = {
    k: logging.Formatter(**v) for k, v in PKG_CONFIG["formatters"].items()
}


def setup_record_factory(project_name: str) -> Callable:
    "Make log records compatible with eng-mindscope log server."
    log_factory = logging.getLogRecordFactory()

    def record_factory(*args, **kwargs) -> logging.LogRecord:
        record = log_factory(*args, **kwargs)
        record.project = project_name
        record.comp_id = os.getenv("aibs_comp_id", None)
        record.rig_name = record.hostname = platform.node()
        record.version = None
        return record

    logging.setLogRecordFactory(record_factory)
    return record_factory


class ServerBackupHandler(logging.handlers.RotatingFileHandler):
    def __init__(
        self,
        filename: str = SERVER_BACKUP["backup_filepath"],
        mode: str = SERVER_BACKUP["mode"],
        maxBytes: int = SERVER_BACKUP["maxBytes"],
        backupCount: int = SERVER_BACKUP["backupCount"],
        encoding: str = SERVER_BACKUP["encoding"],
        delay: bool = SERVER_BACKUP["delay"],
        formatter: logging.Formatter = FORMAT[SERVER_BACKUP["formatter"]],
        **kwargs,
    ):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        self.setLevel(logging.NOTSET)
        self.setFormatter(formatter)

    def emit(self, record):
        with contextlib.suppress(OSError):
            super().emit(record)


class ServerHandler(logging.handlers.SocketHandler):
    def __init__(
        self,
        project_name: str = pathlib.Path.cwd().name,
        host: str = SERVER["host"],
        port: int = SERVER["port"],
        formatter: logging.Formatter = FORMAT[SERVER["formatter"]],
        level: int = SERVER["level"],
        backup: logging.Handler = None,
        **kwargs,
    ):
        super().__init__(host, port)
        self.setLevel(level)
        self.setFormatter(formatter)
        setup_record_factory(project_name)
        if backup is None:
            with contextlib.suppress(Exception):
                backup = ServerBackupHandler()
                self.backup = backup

    def emit(self, record):
        super().emit(record)
        with contextlib.suppress(Exception):
            self.backup.emit(record)


class EmailHandler(logging.handlers.SMTPHandler):
    def __init__(
        self,
        toaddrs: str | list[str],
        project_name: str = pathlib.Path.cwd().name,
        mailhost: str | tuple[str, int] = EMAIL["mailhost"],
        fromaddr: str = EMAIL["fromaddr"],
        subject: str = EMAIL["subject"],
        credentials: Optional[tuple[str, str]] = EMAIL["credentials"],
        secure=EMAIL["secure"],
        timeout: float = EMAIL["timeout"],
        formatter: logging.Formatter = FORMAT[EMAIL["formatter"]],
        level: int = EMAIL["level"],
        **kwargs,
    ):
        super().__init__(
            mailhost, fromaddr, toaddrs, subject, credentials, secure, timeout
        )
        self.setLevel(level)
        self.setFormatter(formatter)
        setup_record_factory(project_name)


class ConsoleHandler(logging.StreamHandler):
    def __init__(
        self,
        stream=sys.stdout,
        formatter: logging.Formatter = FORMAT[CONSOLE["formatter"]],
        level: int = CONSOLE["level"],
        **kwargs,
    ):
        super().__init__(stream)
        self.setLevel(level)
        self.setFormatter(formatter)


class FileHandler(logging.handlers.RotatingFileHandler):
    def __init__(
        self,
        logs_dir: str | pathlib.Path = FILE["logs_dir"],
        mode: str = FILE["mode"],
        maxBytes: int = FILE["maxBytes"],
        backupCount: int = FILE["backupCount"],
        encoding: str = FILE["encoding"],
        delay: bool = FILE["delay"],
        formatter: logging.Formatter = FORMAT[FILE["formatter"]],
        level: int = FILE["level"],
        **kwargs,
    ):
        name = logging.getLevelName(level) if not isinstance(level, str) else level
        filename = pathlib.Path(logs_dir).resolve() / f"{name.lower()}.log"
        filename.parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay)
        self.setLevel(level)
        self.setFormatter(formatter)

    def emit(self, record):
        with contextlib.suppress(Exception):
            super().emit(record)