## 1. Project Setup

- [x] 1.1 Create project directory structure (`aws_switcher/` with `__main__.py` or single `main.py`)
- [x] 1.2 Create `requirements.txt` with `pystray` and `Pillow`
- [x] 1.3 Verify `pystray` and `Pillow` install cleanly on target platform (`pip install -r requirements.txt`)

## 2. AWS Profile Reader

- [x] 2.1 Implement `parse_credentials(path)` using `configparser` — returns dict of profile name → key-value pairs, excluding `[default]`
- [x] 2.2 Implement `parse_config(path)` — handles `[profile <name>]` section naming convention, returns dict of profile name → key-value pairs
- [x] 2.3 Implement `list_profiles()` — merges and deduplicates profile names from both files, returns sorted list
- [x] 2.4 Implement `get_active_profile()` — compares `[default]` key-value pairs against named profiles to identify the active one (returns `None` if no match)
- [x] 2.5 Write unit tests for all parser functions covering: missing file, multiple profiles, deduplication, active profile detection

## 3. Default Profile Switcher

- [x] 3.1 Implement `check_writable(path)` — returns bool, checks OS write permission before attempting any write
- [x] 3.2 Implement `switch_credentials_default(profile_name)` — copies target profile's key-values into `[default]`, writes atomically via temp file + `os.replace()`
- [x] 3.3 Implement `switch_config_default(profile_name)` — copies `[profile <name>]` key-values into `[default]` in config file, same atomic write pattern
- [x] 3.4 Implement `switch_profile(profile_name)` — orchestrates both file writes, returns `(success: bool, error_message: str | None)`
- [x] 3.5 Write unit tests: successful switch, read-only file abort, missing profile graceful handling, atomic write verification

## 4. Tray Icon UI

- [x] 4.1 Implement `build_icon()` — generate a simple AWS-orange square icon using `Pillow` (no external image assets)
- [x] 4.2 Implement `build_menu()` — reads current profiles via `list_profiles()` and `get_active_profile()`, constructs `pystray.Menu` with profile items + "Quit"
- [x] 4.3 Mark active profile in menu with a checkmark prefix (`✓`) in the item title
- [x] 4.4 Wire profile menu item `on_clicked` callback to `switch_profile()` and update tray tooltip on success
- [x] 4.5 Set tray icon tooltip to `"AWS: <active_profile>"` (or `"AWS: (unknown)"` if no match)
- [x] 4.6 Implement menu refresh on open — rebuild menu each time it's displayed so external file changes are picked up
- [x] 4.7 Implement "Quit" menu item that calls `icon.stop()`
- [x] 4.8 Display error as disabled menu item when `switch_profile()` returns failure

## 5. Entry Point and Integration

- [x] 5.1 Write `main()` function that initializes the tray icon and starts the `pystray` run loop
- [x] 5.2 Add `if __name__ == "__main__": main()` guard
- [x] 5.3 Test full flow manually: launch app, open menu, switch profile, verify `~/.aws/credentials` `[default]` is updated, verify tooltip updates
- [x] 5.4 Test error case: make `~/.aws/credentials` read-only, attempt switch, verify error shown in menu and file unchanged

## 6. Packaging and Documentation

- [x] 6.1 Create `README.md` with installation steps (`pip install -r requirements.txt`), usage, and Linux tray notes (AppIndicator extension)
- [x] 6.2 Optionally create a `aws-switcher.desktop` file for autostart on Linux
