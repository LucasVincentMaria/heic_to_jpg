# HEIC → JPG Converter

A desktop GUI app that converts `.heic` files to `.jpg`, copies all other files (photos, videos, etc.) to a single output folder, and renames everything so that sorting by filename gives chronological order.

## Features

- Converts HEIC/HEIF images to JPG at 95% quality
- Copies all other files (JPG, PNG, MP4, MOV, …) unchanged
- Optional checkbox to skip video files
- Renames output files to `YYYYMMDD_HHMMSS.ext` based on capture date
- Capture date priority: EXIF metadata → timestamp in filename → file modification time
- Handles `PXL_` filenames (Google Pixel) by converting from UTC to German local time (CET/CEST)
- Preserves correct rotation using EXIF orientation data
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
5. A summary popup appears when finished

## Output

| Input file | Output |
|---|---|
| `.heic` / `.HEIC` | Converted to `.jpg` (95% quality, rotation corrected) |
| All other files | Copied unchanged |
| Video files (`.mp4`, `.mov`, `.avi`, …) | Copied unchanged, or skipped if checkbox is off |

All output files are renamed to `YYYYMMDD_HHMMSS.ext` and placed flat in the output folder. Sorting by filename in any file manager gives chronological order.
