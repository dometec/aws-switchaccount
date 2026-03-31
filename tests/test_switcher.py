"""Unit tests for aws_switcher.switcher."""

import configparser
import stat
import textwrap
from pathlib import Path

import pytest

from aws_switcher.switcher import (
    check_writable,
    switch_credentials_default,
    switch_config_default,
    switch_profile,
)


def write_file(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content))


# ---------------------------------------------------------------------------
# check_writable
# ---------------------------------------------------------------------------

def test_check_writable_existing_file(tmp_path):
    f = tmp_path / "file"
    f.write_text("x")
    assert check_writable(f) is True


def test_check_writable_nonexistent(tmp_path):
    assert check_writable(tmp_path / "nofile") is False


def test_check_writable_readonly(tmp_path):
    f = tmp_path / "file"
    f.write_text("x")
    f.chmod(stat.S_IRUSR)
    try:
        assert check_writable(f) is False
    finally:
        f.chmod(stat.S_IRUSR | stat.S_IWUSR)


# ---------------------------------------------------------------------------
# switch_credentials_default
# ---------------------------------------------------------------------------

def test_switch_credentials_default_success(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [default]
        aws_access_key_id = OLD
        aws_secret_access_key = OLDSECRET

        [dev]
        aws_access_key_id = DEVKEY
        aws_secret_access_key = DEVSECRET
    """)
    ok, err = switch_credentials_default("dev", creds)
    assert ok is True
    assert err is None

    parser = configparser.ConfigParser()
    parser.read(creds)
    assert parser["default"]["aws_access_key_id"] == "DEVKEY"
    assert parser["default"]["aws_secret_access_key"] == "DEVSECRET"
    assert "dev" in parser  # other sections preserved


def test_switch_credentials_default_missing_profile(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [default]
        aws_access_key_id = OLD

        [dev]
        aws_access_key_id = DEVKEY
    """)
    ok, err = switch_credentials_default("staging", creds)
    assert ok is False
    assert "staging" in err


def test_switch_credentials_default_read_only(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [dev]
        aws_access_key_id = DEVKEY
    """)
    creds.chmod(stat.S_IRUSR)
    try:
        ok, err = switch_credentials_default("dev", creds)
        assert ok is False
        assert err is not None
    finally:
        creds.chmod(stat.S_IRUSR | stat.S_IWUSR)


def test_switch_credentials_atomic_write(tmp_path):
    """Original file must remain intact if profile does not exist (no partial write)."""
    creds = tmp_path / "credentials"
    original = "[default]\naws_access_key_id = ORIGINAL\n\n[dev]\naws_access_key_id = DEVKEY\n"
    creds.write_text(original)
    switch_credentials_default("nonexistent", creds)
    assert creds.read_text() == original


# ---------------------------------------------------------------------------
# switch_config_default
# ---------------------------------------------------------------------------

def test_switch_config_default_success(tmp_path):
    cfg = tmp_path / "config"
    write_file(cfg, """\
        [default]
        region = us-east-1

        [profile dev]
        region = eu-west-1
    """)
    ok, err = switch_config_default("dev", cfg)
    assert ok is True
    assert err is None

    parser = configparser.ConfigParser()
    parser.read(cfg)
    assert parser["default"]["region"] == "eu-west-1"


def test_switch_config_default_missing_config(tmp_path):
    ok, err = switch_config_default("dev", tmp_path / "noconfig")
    assert ok is True  # Missing config is not an error


def test_switch_config_default_profile_absent_from_config(tmp_path):
    cfg = tmp_path / "config"
    write_file(cfg, """\
        [default]
        region = us-east-1
    """)
    ok, err = switch_config_default("dev", cfg)
    assert ok is True  # Profile missing from config is not an error


# ---------------------------------------------------------------------------
# switch_profile
# ---------------------------------------------------------------------------

def test_switch_profile_full_success(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [default]
        aws_access_key_id = OLD

        [prod]
        aws_access_key_id = PRODKEY
        aws_secret_access_key = PRODSECRET
    """)
    cfg = tmp_path / "config"
    write_file(cfg, """\
        [default]
        region = us-east-1

        [profile prod]
        region = ap-southeast-1
    """)
    ok, err = switch_profile("prod", creds, cfg)
    assert ok is True
    assert err is None

    cp = configparser.ConfigParser()
    cp.read(creds)
    assert cp["default"]["aws_access_key_id"] == "PRODKEY"

    cc = configparser.ConfigParser()
    cc.read(cfg)
    assert cc["default"]["region"] == "ap-southeast-1"


def test_switch_profile_aborts_on_credentials_failure(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, "[dev]\naws_access_key_id = DEVKEY\n")
    creds.chmod(stat.S_IRUSR)
    try:
        ok, err = switch_profile("dev", creds, tmp_path / "config")
        assert ok is False
    finally:
        creds.chmod(stat.S_IRUSR | stat.S_IWUSR)
