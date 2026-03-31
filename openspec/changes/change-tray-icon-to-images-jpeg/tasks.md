## 1. Update tray.py

- [x] 1.1 Remove `build_icon()` function and its `_ICON_COLOR` / `_ICON_SIZE` constants from `aws_switcher/tray.py`
- [x] 1.2 Add `_load_icon()` function that resolves `images.jpeg` relative to `tray.py` using `pathlib`, opens it with `Image.open()`, and converts to RGBA
- [x] 1.3 Update `main()` to call `_load_icon()` instead of `build_icon()`
- [x] 1.4 Remove unused `ImageDraw` import if no longer needed

## 2. Verify

- [x] 2.1 Run the application and confirm the tray icon shows the `images.jpeg` image
- [x] 2.2 Confirm tooltip and menu behaviour are unchanged
