# HEIC → JPG Converter — USB Slideshow Tool

> Turn your iPhone photo library into a TV-ready slideshow on a USB stick — sorted by capture date, oldest first, so your photos tell the story of your life from the very beginning.

## The Idea

Modern iPhones save photos in HEIC format, which most TVs and older devices cannot display. This tool was built to solve a simple but meaningful problem: creating a USB stick slideshow that works on any TV and shows your photos in the right order — from your earliest memories to today.

The result is a life journey in pictures. Plug the USB stick into any TV, start the slideshow, and watch your story unfold chronologically — old and grainy photos first, gradually becoming newer and newer.

## Features

- Converts HEIC/HEIF images to JPG at 95% quality
- Copies all other files (JPG, PNG, MP4, MOV, …) unchanged
- Optional checkbox to skip video files
- Renames every output file to `YYYYMMDD_HHMMSS.ext` — sorting by filename = sorting by date
- Capture date priority: EXIF metadata → timestamp in filename → file modification time
- Handles `PXL_` filenames (Google Pixel) by converting UTC to German local time (CET/CEST)
- Preserves correct photo rotation using EXIF orientation data
- Recursively scans all subfolders
- Avoids filename collisions automatically (`_1`, `_2`, …)
- Live progress bar and log — UI stays responsive during conversion

## Requirements

- Python 3.10+
- [Pillow](https://pypi.org/project/Pillow/)
- [pillow-heif](https://pypi.org/project/pillow-heif/)

```bash
pip install pillow pillow-heif
```

## Usage

**Double-click** `Run Converter.bat`, or run directly:

```bash
py converter.py
```

1. Click **Browse…** next to "Source folder" and select the folder with your photos/videos
2. The output folder auto-fills as `<source>_converted` — change it if needed
3. Check or uncheck **Copy video files** depending on whether you want videos included
4. Click **Convert**
5. Copy the output folder to a USB stick and plug it into your TV
6. Start the slideshow — photos will play in chronological order, oldest first

## Output

| Input file | Output |
|---|---|
| `.heic` / `.HEIC` | Converted to `.jpg` (95% quality, rotation corrected) |
| All other files | Copied unchanged |
| Video files (`.mp4`, `.mov`, `.avi`, …) | Copied unchanged, or skipped if checkbox is off |

All output files are renamed to `YYYYMMDD_HHMMSS.ext` and placed flat in the output folder. Any TV or device that supports USB slideshows will display them in the correct chronological order when sorted by filename.

## Use Case

This tool is perfect for:
- Creating a **life journey slideshow** for a birthday, anniversary, or family event
- Making your iPhone photo library **compatible with older TVs** via USB
- Archiving photos in a **universally readable format** (JPG) with a clean chronological structure
- Preparing a **memorial or tribute slideshow** that tells someone's story from beginning to present
