# GIF Overlay Plugin for Dank Material Shell   /ᐠ˵- ⩊ -˵マ

A "lightweight" floating animated sprite overlay for Wayland using GTK4 + GStreamer.

Designed for Dank Material Shell (DMS) as a DankBar widget plugin.

---

## ✨ Features

- Floating transparent animated GIF / WebM overlay
- Always-on-top window
- ❌❌ Adjustable playback speed (⬆ / ⬇) ❌❌
- Next / Previous media (← / →)
- Pause / Resume (Space)
- Close (Esc)
- Portable plugin structure
- Fully integrated with DankBar



## 🧩 Requirements

### 1️⃣ System Dependencies (Fedora)

```bash
sudo dnf install \
    gtk4 \
    gtk4-devel \
    gstreamer1 \
    gstreamer1-plugins-base \
    gstreamer1-plugins-good \
    gstreamer1-plugins-bad-free \
    gstreamer1-libav \
    gstreamer1-plugin-gtk4 \
    python3-gobject
```

## Changes You Need To Make

- Change MEDIA_DIR in ```sprite.py``` to the path of your sprites folder
- Icon for Dank Widget (optional)


## Doesn't Work Yet ❌❌

- Up/Down Button: Playback Speed ❌❌
- Clickthrough ❌❌


## 🤝 Contributions

If want to you improve something, refactor stuff, add features, or clean up my questionable decisions and this well-organized readme — please do.

Changes are much appreciated!! ฅ^>⩊<^ฅ

---
Inspired by claymorwan's [media-frame](https://codeberg.org/claymorwan/dms-plugins/src/branch/master/mediaFrame) DMS plugin.
This is a fresh GTK4/DMS-compatible implementation.
