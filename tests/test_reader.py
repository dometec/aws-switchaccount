"""Unit tests for aws_switcher.reader."""

import textwrap
from pathlib import Path

import pytest

from aws_switcher.reader import (
    get_active_profile,
    list_profiles,
    parse_config,
    parse_credentials,
)


def write_file(path: Path, content: str) -> None:
    path.write_text(textwrap.dedent(content))


# ---------------------------------------------------------------------------
# parse_credentials
# ---------------------------------------------------------------------------

def test_parse_credentials_missing_file(tmp_path):
    result = parse_credentials(tmp_path / "nonexistent")
    assert result == {}


def test_parse_credentials_excludes_default(tmp_path):
    f = tmp_path / "credentials"
    write_file(f, """\
        [default]
        aws_access_key_id = DEFAULTKEY
        aws_secret_access_key = DEFAULTSECRET

        [dev]
        aws_access_key_id = DEVKEY
        aws_secret_access_key = DEVSECRET
    """)
    result = parse_credentials(f)
    assert "default" not in result
    assert "dev" in result
    assert result["dev"]["aws_access_key_id"] == "DEVKEY"


def test_parse_credentials_multiple_profiles(tmp_path):
    f = tmp_path / "credentials"
    write_file(f, """\
        [default]
        aws_access_key_id = X

        [dev]
        aws_access_key_id = DEVKEY

        [prod]
        aws_access_key_id = PRODKEY
    """)
    result = parse_credentials(f)
    assert set(result.keys()) == {"dev", "prod"}


# ---------------------------------------------------------------------------
# parse_config
# ---------------------------------------------------------------------------

def test_parse_config_missing_file(tmp_path):
    result = parse_config(tmp_path / "nonexistent")
    assert result == {}


def test_parse_config_profile_sections(tmp_path):
    f = tmp_path / "config"
    write_file(f, """\
        [default]
        region = us-east-1

        [profile staging]
        region = eu-west-1

        [profile prod]
        region = us-west-2
    """)
    result = parse_config(f)
    assert "staging" in result
    assert "prod" in result
    assert "default" not in result
    assert result["staging"]["region"] == "eu-west-1"


def test_parse_config_ignores_non_profile_sections(tmp_path):
    f = tmp_path / "config"
    write_file(f, """\
        [default]
        region = us-east-1

        [sso-session my-sso]
        sso_start_url = https://example.com
    """)
    result = parse_config(f)
    assert result == {}


# ---------------------------------------------------------------------------
# list_profiles
# ---------------------------------------------------------------------------

def test_list_profiles_deduplicates(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [dev]
        aws_access_key_id = DEVKEY

        [prod]
        aws_access_key_id = PRODKEY
    """)
    cfg = tmp_path / "config"
    write_file(cfg, """\
        [profile prod]
        region = us-east-1

        [profile staging]
        region = eu-west-1
    """)
    result = list_profiles(creds, cfg)
    assert result == ["dev", "prod", "staging"]


def test_list_profiles_sorted(tmp_path):
    creds = tmp_path / "credentials"
    write_file(creds, """\
        [zebra]
        aws_access_key_id = Z

        [alpha]
        aws_access_key_id = A
    """)
    result = list_profiles(creds, tmp_path / "noconfig")
    assert result == ["alpha", "zebra"]


def test_list_profiles_missing_both_files(tmp_path):
    result = list_profiles(tmp_path / "nc", tmp_path / "nc2")
    assert result == []


# ---------------------------------------------------------------------------
# get_active_profile
# ---------------------------------------------------------------------------

def test_get_active_profile_matches(tmp_path):
    f = tmp_path / "credentials"
    write_file(f, """\
        [default]
        aws_access_key_id = DEVKEY
        aws_secret_access_key = DEVSECRET

        [dev]
        aws_access_key_id = DEVKEY
        aws_secret_access_key = DEVSECRET

        [prod]
        aws_access_key_id = PRODKEY
        aws_secret_access_key = PRODSECRET
    """)
    result = get_active_profile(f)
    assert result == "dev"


def test_get_active_profile_no_match(tmp_path):
    f = tmp_path / "credentials"
    write_file(f, """\
        [default]
        aws_access_key_id = UNKNOWNKEY

        [dev]
        aws_access_key_id = DEVKEY
    """)
    result = get_active_profile(f)
    assert result is None


def test_get_active_profile_missing_file(tmp_path):
    result = get_active_profile(tmp_path / "nofile")
    assert result is None


def test_get_active_profile_no_default_section(tmp_path):
    f = tmp_path / "credentials"
    write_file(f, """\
        [dev]
        aws_access_key_id = DEVKEY
    """)
    result = get_active_profile(f)
    assert result is None
