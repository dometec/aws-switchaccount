"""AWS default profile switcher — atomically rewrites [default] sections."""

import configparser
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

from aws_switcher.reader import (
    CONFIG_PATH,
    CREDENTIALS_PATH,
    parse_config,
    parse_credentials,
)

logger = logging.getLogger(__name__)


def check_writable(path: Path) -> bool:
    """Return True if *path* exists and is writable by the current user."""
    return path.exists() and os.access(path, os.W_OK)


def _write_atomically(path: Path, parser: configparser.ConfigParser) -> None:
    """Write *parser* to *path* via a temp file + atomic rename."""
    dir_ = path.parent
    fd, tmp = tempfile.mkstemp(dir=dir_, prefix=".aws_switcher_")
    try:
        with os.fdopen(fd, "w") as fh:
            parser.write(fh)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def switch_credentials_default(
    profile_name: str,
    credentials_path: Path = CREDENTIALS_PATH,
) -> Tuple[bool, Optional[str]]:
    """Copy *profile_name*'s key-values into [default] in the credentials file.

    Returns ``(True, None)`` on success or ``(False, error_message)`` on failure.
    """
    if not check_writable(credentials_path):
        msg = f"Credentials file is not writable: {credentials_path}"
        logger.error(msg)
        return False, msg

    profiles = parse_credentials(credentials_path)
    if profile_name not in profiles:
        msg = f"Profile '{profile_name}' not found in {credentials_path}"
        logger.error(msg)
        return False, msg

    parser = configparser.ConfigParser()
    parser.read(credentials_path)

    if "default" not in parser:
        parser["default"] = {}

    parser["default"] = dict(profiles[profile_name])

    try:
        _write_atomically(credentials_path, parser)
    except OSError as exc:
        msg = f"Failed to write {credentials_path}: {exc}"
        logger.error(msg)
        return False, msg

    return True, None


def switch_config_default(
    profile_name: str,
    config_path: Path = CONFIG_PATH,
) -> Tuple[bool, Optional[str]]:
    """Copy ``[profile <name>]`` key-values into [default] in the config file.

    Returns ``(True, None)`` on success or ``(False, error_message)`` on failure.
    If the config file doesn't exist or the profile is absent, returns success
    (credentials-only profiles are valid).
    """
    if not config_path.exists():
        return True, None

    if not check_writable(config_path):
        msg = f"Config file is not writable: {config_path}"
        logger.error(msg)
        return False, msg

    profiles = parse_config(config_path)
    if profile_name not in profiles:
        # Profile exists only in credentials — skip config, not an error
        return True, None

    parser = configparser.ConfigParser()
    parser.read(config_path)

    if "default" not in parser:
        parser["default"] = {}

    parser["default"] = dict(profiles[profile_name])

    try:
        _write_atomically(config_path, parser)
    except OSError as exc:
        msg = f"Failed to write {config_path}: {exc}"
        logger.error(msg)
        return False, msg

    return True, None


def switch_profile(
    profile_name: str,
    credentials_path: Path = CREDENTIALS_PATH,
    config_path: Path = CONFIG_PATH,
) -> Tuple[bool, Optional[str]]:
    """Switch the AWS default to *profile_name*.

    Returns ``(True, None)`` on success or ``(False, error_message)`` on failure.
    """
    ok, err = switch_credentials_default(profile_name, credentials_path)
    if not ok:
        return False, err

    ok, err = switch_config_default(profile_name, config_path)
    if not ok:
        return False, err

    logger.info("Switched default AWS profile to '%s'", profile_name)
    return True, None
