## Context

AWS CLI stores named profiles in `~/.aws/credentials` (access keys) and `~/.aws/config` (region, output format, etc.). The `[default]` profile is what tools use when no explicit profile is specified. Power users managing multiple accounts (dev, staging, prod, multiple organizations) currently must edit these files manually or export `AWS_PROFILE`.

This is a new standalone desktop application — no existing codebase to modify.

## Goals / Non-Goals

**Goals:**
- Parse both AWS config files to list all named profiles
- Display profiles in a system tray menu
- Switch the active default by rewriting the `[default]` section in both files
- Show the currently active profile in the tray tooltip/label
- Run in the background as a persistent tray process

**Non-Goals:**
- Creating or deleting profiles (only switching between existing ones)
- Supporting `AWS_PROFILE` env var injection into running shells
- SSO / IAM Identity Center authentication flows
- Encrypting or securing credential storage
- Multi-region awareness beyond what's already in the config file

## Decisions

### Language and Runtime: Python 3.8+
**Why Python over Electron/Go/Rust:** The task is pure file I/O + GUI tray. Python's `configparser` stdlib handles INI-format AWS files natively. `pystray` provides a cross-platform tray API in ~10 lines. No build toolchain needed; ships as a single script or simple package.
**Alternatives considered:** Go with `systray` lib (heavier build chain for minimal gain), Electron (massive overhead for a file-edit utility).

### Tray Library: `pystray` + `Pillow`
**Why:** `pystray` is the de-facto cross-platform Python tray library supporting Linux (AppIndicator/GTK), macOS, and Windows. `Pillow` is its dependency for generating the icon image at runtime.
**Alternatives considered:** `PyQt5` / `wxPython` — bring full GUI framework overhead; overkill for tray-only use.

### Profile Switching Strategy: Rewrite `[default]` section
**Why:** The AWS CLI reads `[default]` literally. The safest approach is to copy the target profile's key/value pairs into `[default]`, preserving all other sections. This avoids pointer/symlink hacks that could confuse third-party tools.
**Alternatives considered:** Writing `AWS_PROFILE=<name>` to a shell rc file (fragile, session-scoped), symlinking files (breaks on Windows).

### Icon: Programmatically generated via Pillow
**Why:** Avoids shipping binary assets. A simple colored circle or AWS-orange square is generated at startup and can change color to indicate the active profile.
**Alternatives considered:** Bundled PNG (simpler but requires asset management).

### Single-file entry point
The application is a single `main.py` (or `aws_switcher.py`) for simplicity. No internal package structure needed at this scope.

## Risks / Trade-offs

- **Concurrent writes** → If another process (e.g., `aws configure`) edits the file while the tray app is running, changes could collide. Mitigation: re-read files on every menu open, write atomically via temp file + rename.
- **configparser quirks** → AWS config uses `[profile name]` format in `~/.aws/config` but `[name]` in `~/.aws/credentials`. Mitigation: handle both section name formats explicitly in the parser.
- **Linux tray support** → Some desktop environments (GNOME 40+) hide tray icons by default. Mitigation: document that users may need `gnome-shell-extension-appindicator` or similar.
- **File permissions** → If `~/.aws/credentials` is not writable, the switch silently fails. Mitigation: check writability before showing the menu; display error via tray notification.
