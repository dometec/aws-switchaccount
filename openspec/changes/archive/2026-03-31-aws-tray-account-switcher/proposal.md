## Why

Managing multiple AWS accounts via CLI requires manually editing `~/.aws/credentials` and `~/.aws/config` or using `AWS_PROFILE` environment variables, which is error-prone and slow. A system tray application provides instant, visual switching between AWS profiles without touching terminal sessions.

## What Changes

- New cross-platform desktop tray application (Python + system tray library)
- Reads existing `~/.aws/credentials` and `~/.aws/config` to list available profiles
- Allows selecting a default profile from the tray menu
- Updates the `[default]` section in both files to point to the selected profile's credentials
- Shows the currently active profile in the tray icon tooltip

## Capabilities

### New Capabilities
- `aws-profile-reader`: Parse `~/.aws/credentials` and `~/.aws/config` to enumerate available named profiles
- `default-profile-switcher`: Update the `[default]` section in AWS config files to reflect the selected profile
- `tray-icon-ui`: System tray icon with dropdown menu listing all profiles and current selection indicator

### Modified Capabilities
<!-- none -->

## Impact

- No existing code is modified (new standalone application)
- Dependencies: Python 3.8+, `pystray`, `Pillow` (for tray icon rendering), `configparser` (stdlib)
- Reads and writes `~/.aws/credentials` and `~/.aws/config` — requires filesystem access to user home directory
- Cross-platform target: Linux (primary), macOS, Windows
