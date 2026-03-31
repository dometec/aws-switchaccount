## Why

The tray icon is currently a programmatically generated orange square, which looks generic. Replacing it with `images.jpeg` (a project-specific image already present in the repo) gives the application a more polished and recognisable appearance.

## What Changes

- Remove the `build_icon()` function that generates an orange rectangle at runtime.
- Load `images.jpeg` from the project's root directory (or a bundled path) using Pillow and use it as the tray icon image.

## Capabilities

### New Capabilities
<!-- none -->

### Modified Capabilities
- `tray-icon-ui`: The tray icon image source changes from a generated solid-colour square to the static `images.jpeg` file. The requirement "Display system tray icon" is still met, but the visual appearance specification changes.

## Impact

- `aws_switcher/tray.py`: `build_icon()` replaced with an image-loading helper.
- `images.jpeg`: Read at application startup; must be accessible relative to the installed package or working directory.
- No API, dependency, or configuration changes.
