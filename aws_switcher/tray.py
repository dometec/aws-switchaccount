"""System tray UI for the AWS profile switcher."""

import logging
from pathlib import Path
from typing import Optional

import pystray
from PIL import Image

from aws_switcher.reader import get_active_profile, list_profiles
from aws_switcher.switcher import switch_profile

logger = logging.getLogger(__name__)

# Module-level reference to the running icon so callbacks can mutate it
_icon: Optional[pystray.Icon] = None
# Tracks the last error so it can be surfaced in the menu
_last_error: Optional[str] = None


def _load_icon() -> Image.Image:
    """Load the tray icon from aws-white.png in the project root."""
    icon_path = Path(__file__).parent.parent / "aws-white.png"
    return Image.open(icon_path).convert("RGBA")


def _make_profile_item(profile_name: str, active: Optional[str]) -> pystray.MenuItem:
    """Return a menu item for *profile_name*, marked if it is active."""
    prefix = "✓ " if profile_name == active else "   "
    label = f"{prefix}{profile_name}"

    def on_click(icon: pystray.Icon, item: pystray.MenuItem) -> None:
        global _last_error
        ok, err = switch_profile(profile_name)
        if ok:
            _last_error = None
            active_now = profile_name
            icon.title = f"AWS: {active_now}"
        else:
            _last_error = err
            logger.error("Switch failed: %s", err)
        # Rebuild menu to reflect new active profile / error state
        icon.menu = build_menu()
        icon.update_menu()

    return pystray.MenuItem(label, on_click)


def build_menu() -> pystray.Menu:
    """Build the tray menu, re-reading profiles from disk each time."""
    global _last_error

    profiles = list_profiles()
    active = get_active_profile()

    items = []

    if _last_error:
        items.append(pystray.MenuItem(f"Error: {_last_error}", None, enabled=False))
        items.append(pystray.Menu.SEPARATOR)

    if profiles:
        for name in profiles:
            items.append(_make_profile_item(name, active))
    else:
        items.append(pystray.MenuItem("No profiles found", None, enabled=False))

    items.append(pystray.Menu.SEPARATOR)
    items.append(pystray.MenuItem("Quit", _on_quit))

    return pystray.Menu(*items)


def _on_quit(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    icon.stop()


def _tooltip() -> str:
    active = get_active_profile()
    return f"AWS: {active}" if active else "AWS: (unknown)"


def main() -> None:
    """Initialise the tray icon and start the pystray run loop."""
    global _icon

    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")

    image = _load_icon()
    title = _tooltip()
    menu = build_menu()

    _icon = pystray.Icon(
        name="aws-switcher",
        icon=image,
        title=title,
        menu=menu,
    )
    _icon.run()


if __name__ == "__main__":
    main()
