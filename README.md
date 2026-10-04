# ♡ Kawaii Maid Viewer ♡

A cute pastel desktop app for Windows 11 that shows random SFW anime maid art (otoko no ko / femboy maids) with a one-click slideshow.

## Features
- ✨ **Generate New** – fetch a fresh random image (or press Space)
- ▶ **Slideshow** – auto-advances every 5 seconds
- 💾 **Save Image** – save the current picture as PNG or JPG
- 📌 **Pop Out** – floats the current image in a small always-on-top window that stays above everything until you close it (✕, Esc, or the button again). It updates whenever you generate a new image, is resizable, and the mouse wheel over it adjusts transparency
- Safe-for-work only: general-rated posts, with loli/shota/child tags excluded

## Download (easy way)
1. Go to the [**Releases**](../../releases) page.
2. Download `KawaiiMaidViewer.exe`.
3. Double-click it. That's it!

> Windows SmartScreen may warn about an unrecognized app since the exe isn't code-signed. Click **More info → Run anyway**.

## Run from source
```bash
pip install -r requirements.txt
python app.py
```

## Build the exe yourself
Double-click `build.bat`, or run:
```bash
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --windowed --name KawaiiMaidViewer app.py
```
The exe appears in `dist/`.

## Customizing
Edit the top of `app.py`:
- `TAGS` – the Safebooru search tags
- `SLIDESHOW_MS` – slideshow delay in milliseconds

## Credits
Images are fetched live from [Safebooru](https://safebooru.org) and belong to their original artists. This app doesn't host or redistribute any images; it is for personal use.

## License
MIT – see [LICENSE](LICENSE).
