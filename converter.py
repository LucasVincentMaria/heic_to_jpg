import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import shutil
from pathlib import Path
from PIL import Image, ImageOps
from datetime import datetime
import pillow_heif

pillow_heif.register_heif_opener()


def capture_date(f: Path) -> datetime:
    """Return the EXIF capture date, falling back to filename then mtime."""
    try:
        img = Image.open(f)
        exif = img.getexif()
        # 0x9003 = DateTimeOriginal, 0x0132 = DateTime
        for tag in (0x9003, 0x0132):
            val = exif.get(tag)
            if val:
                return datetime.strptime(val, "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return datetime.fromtimestamp(f.stat().st_mtime)


VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".m4v", ".3gp", ".wmv"}


def find_files(source_dir: Path, copy_videos: bool) -> tuple[list[Path], list[Path]]:
    heic_files, other_files = [], []
    seen = set()
    all_found = []
    for f in source_dir.rglob("*"):
        if not f.is_file():
            continue
        key = f.resolve()
        if key in seen:
            continue
        seen.add(key)
        if not copy_videos and f.suffix.lower() in VIDEO_EXTENSIONS:
            continue
        all_found.append(f)

    all_found.sort(key=capture_date)

    for f in all_found:
        if f.suffix.lower() == ".heic":
            heic_files.append(f)
        else:
            other_files.append(f)
    return heic_files, other_files


def convert(source_dir: Path, output_dir: Path, log_fn, progress_fn, done_fn, copy_videos: bool = True):
    heic_files, other_files = find_files(source_dir, copy_videos)
    total = len(heic_files) + len(other_files)

    if total == 0:
        log_fn("No files found in the selected folder.")
        done_fn(0, 0, 0)
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    converted = 0
    copied = 0
    errors = 0

    all_files = sorted(
        [("heic", f) for f in heic_files] + [("other", f) for f in other_files],
        key=lambda x: capture_date(x[1]),
    )

    for i, (kind, src) in enumerate(all_files, 1):
        dest_suffix = ".jpg" if kind == "heic" else src.suffix
        dest = output_dir / (src.stem + dest_suffix)

        if dest.exists():
            counter = 1
            while dest.exists():
                dest = output_dir / f"{src.stem}_{counter}{dest_suffix}"
                counter += 1

        try:
            if kind == "heic":
                img = Image.open(src)
                img = ImageOps.exif_transpose(img)
                img.convert("RGB").save(dest, "JPEG", quality=95)
                log_fn(f"Converted: {src.name}")
                converted += 1
            else:
                shutil.copy2(src, dest)
                log_fn(f"Copied:    {src.name}")
                copied += 1
        except Exception as e:
            log_fn(f"ERROR {src.name}: {e}")
            errors += 1

        progress_fn(i / total * 100)

    done_fn(converted, copied, errors)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HEIC → JPG Converter")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 5}

        frame_top = ttk.Frame(self, padding=10)
        frame_top.pack(fill="x")

        # Source
        ttk.Label(frame_top, text="Source folder:").grid(row=0, column=0, sticky="w")
        self.src_var = tk.StringVar()
        ttk.Entry(frame_top, textvariable=self.src_var, width=50).grid(row=0, column=1, **pad)
        ttk.Button(frame_top, text="Browse…", command=self._pick_source).grid(row=0, column=2)

        # Output
        ttk.Label(frame_top, text="Output folder:").grid(row=1, column=0, sticky="w")
        self.out_var = tk.StringVar()
        ttk.Entry(frame_top, textvariable=self.out_var, width=50).grid(row=1, column=1, **pad)
        ttk.Button(frame_top, text="Browse…", command=self._pick_output).grid(row=1, column=2)

        # Options
        self.copy_videos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame_top, text="Copy video files (mp4, mov, …)", variable=self.copy_videos_var).grid(
            row=2, column=1, sticky="w", padx=10, pady=(2, 4)
        )

        # Progress
        self.progress = ttk.Progressbar(self, length=500, mode="determinate")
        self.progress.pack(padx=10, pady=(5, 0))

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self, textvariable=self.status_var, foreground="gray").pack()

        # Log
        frame_log = ttk.Frame(self, padding=(10, 0, 10, 5))
        frame_log.pack(fill="both", expand=True)
        self.log = tk.Text(frame_log, height=14, width=70, state="disabled", wrap="word")
        scroll = ttk.Scrollbar(frame_log, command=self.log.yview)
        self.log.configure(yscrollcommand=scroll.set)
        self.log.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        # Button
        self.btn = ttk.Button(self, text="Convert", command=self._start, width=20)
        self.btn.pack(pady=(0, 10))

    def _pick_source(self):
        d = filedialog.askdirectory(title="Select source folder")
        if d:
            self.src_var.set(d)
            if not self.out_var.get():
                self.out_var.set(str(Path(d).parent / (Path(d).name + "_converted")))

    def _pick_output(self):
        d = filedialog.askdirectory(title="Select output folder")
        if d:
            self.out_var.set(d)

    def _log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_progress(self, val: float):
        self.progress["value"] = val
        self.update_idletasks()

    def _done(self, converted: int, copied: int, errors: int):
        self.btn.configure(state="normal")
        self.status_var.set(
            f"Done — {converted} converted, {copied} copied, {errors} errors"
        )
        summary = (
            f"\n--- Finished ---\n"
            f"  Converted (HEIC→JPG): {converted}\n"
            f"  Copied (JPG):         {copied}\n"
            f"  Errors:               {errors}\n"
            f"  Output folder: {self.out_var.get()}"
        )
        self._log(summary)
        if errors == 0:
            messagebox.showinfo("Done", f"All done!\n{converted} converted, {copied} copied.")
        else:
            messagebox.showwarning("Done with errors", f"{converted} converted, {copied} copied, {errors} errors.\nCheck the log.")

    def _start(self):
        src = self.src_var.get().strip()
        out = self.out_var.get().strip()
        if not src:
            messagebox.showerror("Missing input", "Please select a source folder.")
            return
        if not out:
            messagebox.showerror("Missing output", "Please select an output folder.")
            return

        src_path = Path(src)
        if not src_path.exists():
            messagebox.showerror("Not found", f"Source folder does not exist:\n{src}")
            return

        self.btn.configure(state="disabled")
        self.progress["value"] = 0
        self.status_var.set("Working…")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

        threading.Thread(
            target=convert,
            args=(
                src_path,
                Path(out),
                lambda m: self.after(0, self._log, m),
                lambda v: self.after(0, self._set_progress, v),
                lambda c, cp, e: self.after(0, self._done, c, cp, e),
            ),
            kwargs={"copy_videos": self.copy_videos_var.get()},
            daemon=True,
        ).start()


if __name__ == "__main__":
    app = App()
    app.mainloop()
