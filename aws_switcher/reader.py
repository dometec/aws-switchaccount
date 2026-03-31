"""AWS profile reader — parses ~/.aws/credentials and ~/.aws/config."""

import configparser
import logging
import os
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

CREDENTIALS_PATH = Path.home() / ".aws" / "credentials"
CONFIG_PATH = Path.home() / ".aws" / "config"


def parse_credentials(path: Path = CREDENTIALS_PATH) -> Dict[str, Dict[str, str]]:
    """Return named profiles from an AWS credentials file, excluding [default]."""
    profiles: Dict[str, Dict[str, str]] = {}
    if not path.exists():
        logger.warning("Credentials file not found: %s", path)
        return profiles
    parser = configparser.ConfigParser()
    parser.read(path)
    for section in parser.sections():
        if section.lower() == "default":
            continue
        profiles[section] = dict(parser[section])
    return profiles


def parse_config(path: Path = CONFIG_PATH) -> Dict[str, Dict[str, str]]:
    """Return named profiles from an AWS config file.

    The config file uses ``[profile <name>]`` sections for named profiles and
    ``[default]`` for the default profile.
    """
    profiles: Dict[str, Dict[str, str]] = {}
    if not path.exists():
        logger.warning("Config file not found: %s", path)
        return profiles
    parser = configparser.ConfigParser()
    parser.read(path)
    for section in parser.sections():
        if section.lower() == "default":
            continue
        if section.lower().startswith("profile "):
            name = section[len("profile "):].strip()
            profiles[name] = dict(parser[section])
    return profiles


def list_profiles(
    credentials_path: Path = CREDENTIALS_PATH,
    config_path: Path = CONFIG_PATH,
) -> List[str]:
    """Return a sorted, deduplicated list of all named AWS profile names."""
    cred_profiles = set(parse_credentials(credentials_path).keys())
    cfg_profiles = set(parse_config(config_path).keys())
    return sorted(cred_profiles | cfg_profiles)


def get_active_profile(
    credentials_path: Path = CREDENTIALS_PATH,
    config_path: Path = CONFIG_PATH,
) -> Optional[str]:
    """Return the named profile whose credentials match [default], or None."""
    if not credentials_path.exists():
        return None

    parser = configparser.ConfigParser()
    parser.read(credentials_path)

    if "default" not in parser:
        return None

    default_items = dict(parser["default"])
    profiles = parse_credentials(credentials_path)

    for name, items in profiles.items():
        if items == default_items:
            return name
    return None
