# HEIC → JPG Converter

A simple desktop GUI app that converts `.heic` / `.HEIC` files to `.jpg` and copies existing `.jpg` / `.jpeg` files into a new output folder.

## Features

- Converts HEIC/HEIF images to JPG at 95% quality
- Copies existing JPG/JPEG files as-is
- Recursively scans subfolders
- Live progress bar and log during conversion
- Avoids filename collisions automatically
- Runs conversion on a background thread — UI stays responsive

## Requirements

- Python 3.9+
- [Pillow](https://pypi.org/project/Pillow/)
- [pillow-heif](https://pypi.org/project/pillow-heif/)

Install dependencies:

```bash
pip install pillow pillow-heif
```

## Usage

**Double-click** `Run Converter.bat`, or run directly:

```bash
py converter.py
```

1. Click **Browse…** next to "Source folder" and select the folder containing your photos
2. The output folder auto-fills as `<source>_converted` — change it if needed
3. Click **Convert**
4. A summary popup appears when finished

## Output

| File type | Action |
|-----------|--------|
| `.heic` / `.HEIC` | Converted to `.jpg` (95% quality) |
| `.jpg` / `.jpeg` / `.JPG` / `.JPEG` | Copied unchanged |

All output files are placed in the selected output folder (not in subfolders).
