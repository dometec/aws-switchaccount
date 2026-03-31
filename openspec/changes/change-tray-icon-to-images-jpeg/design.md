## Context

`aws_switcher/tray.py` currently generates the tray icon programmatically via `build_icon()`, which draws a plain AWS-orange rectangle using Pillow's `ImageDraw`. The file `images.jpeg` is already committed to the project root and contains the desired icon image.

## Goals / Non-Goals

**Goals:**
- Load `images.jpeg` at startup and use it as the pystray icon instead of the generated rectangle.
- Keep the change minimal: one function replaced, no new dependencies.

**Non-Goals:**
- Resizing or colour-adjusting the image (use it as-is).
- Packaging the image inside the Python package (path resolution is handled by convention).
- Changing any other aspect of the tray UI.

## Decisions

**1. Path resolution — use `pathlib` relative to `tray.py`**

`images.jpeg` lives in the project root. We resolve the path relative to `tray.py`'s own location (`Path(__file__).parent.parent / "images.jpeg"`). This works for both direct execution and `pip install -e` development installs without requiring changes to `setup.py`/`pyproject.toml`.

Alternative considered: rely on the current working directory. Rejected because the CWD may differ depending on how the app is launched (e.g., from a `.desktop` file).

**2. Replace `build_icon()` with `_load_icon()`**

Rename the helper to `_load_icon()` (private, underscore-prefixed) to signal it is an implementation detail. It opens the JPEG, converts to `RGBA` (pystray expects RGBA), and returns the `Image` object.

Alternative: inline the loading in `main()`. Rejected to keep testability — the function can be imported and tested independently.

## Risks / Trade-offs

- [Missing file] If `images.jpeg` is absent at runtime the app crashes on startup. → Mitigation: file is committed to the repo; document the requirement in README. No graceful fallback is added to keep the change minimal.
- [Image format] JPEG does not support transparency. Converting to RGBA fills the alpha channel at 255 (fully opaque), which is acceptable for a tray icon.

## Migration Plan

1. Replace `build_icon()` with `_load_icon()` in `tray.py`.
2. Update the call site in `main()`.
3. No data migration or deployment steps required.
4. Rollback: revert `tray.py` to regenerate the orange square.
