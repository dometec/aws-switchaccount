# aws-switcher

A system tray application for switching the active AWS CLI profile on Linux, macOS, and Windows.

Click the tray icon to see all named profiles from `~/.aws/credentials` and `~/.aws/config`. Selecting a profile rewrites the `[default]` section in both files so that AWS CLI tools, SDKs, and Terraform use it immediately — no terminal required.

## Requirements

- Python 3.8+
- `pystray` and `Pillow`

## Installation

```bash
pip install -r requirements.txt
```

## Running

```bash
python -m aws_switcher
```

Or directly:

```bash
python aws_switcher/tray.py
```

## Usage

1. Launch the app — a small orange icon appears in the system tray.
2. Click the icon to open the profile menu.
3. Click a profile name to set it as default. A checkmark (✓) marks the current default.
4. The tooltip shows `AWS: <profile>` reflecting the active selection.
5. Click **Quit** to exit.

## Linux notes

On GNOME 40+ the legacy system tray is hidden by default. Install the AppIndicator extension:

```bash
# Fedora / RHEL
sudo dnf install gnome-shell-extension-appindicator

# Ubuntu / Debian
sudo apt install gnome-shell-extension-appindicator
```

Then enable it via GNOME Extensions or:

```bash
gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
```

On other desktop environments (KDE Plasma, XFCE, etc.) the tray icon should appear without extra steps.

## How it works

The app uses `configparser` (stdlib) to parse the INI-format AWS config files. When you select a profile:

1. It reads the named profile's key-value pairs from `~/.aws/credentials`.
2. It overwrites the `[default]` section with those values using an atomic write (temp file + rename) to prevent corruption.
3. It does the same for `~/.aws/config` using the `[profile <name>]` section.

No credentials are transmitted anywhere — all operations are local filesystem reads and writes.

## Autostart (Linux)

Copy `aws-switcher.desktop` to the XDG autostart directory so the app launches automatically at login:

```bash
cp aws-switcher.desktop ~/.config/autostart/
```

To make it available in application launchers system-wide:

```bash
sudo cp aws-switcher.desktop /usr/share/applications/
```

To launch it immediately without logging out:

```bash
gtk-launch aws-switcher
```

> **Note:** The `Exec` path in `aws-switcher.desktop` assumes `python` and `aws_switcher` are on your `PATH`. If you installed in a virtualenv, replace `python` with the full path to the virtualenv's Python binary (e.g. `/home/user/.venv/bin/python`).
