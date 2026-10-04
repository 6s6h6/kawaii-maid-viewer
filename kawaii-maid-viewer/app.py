"""Kawaii Maid Viewer - SFW anime image viewer for Windows 11.

Pulls safe-for-work images from Safebooru, shows them in a pastel GUI with
Generate / Slideshow / Save controls.
"""
import io
import random
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import requests
from PIL import Image, ImageTk

API = "https://safebooru.org/index.php"
IMG_BASE = "https://safebooru.org/images"
HEADERS = {"User-Agent": "KawaiiMaidViewer/1.0"}
# Positive tags + exclusions to keep results SFW and adult-looking.
TAGS = "otoko_no_ko maid solo -loli -shota -child -toddler -baby -chibi"
SLIDESHOW_MS = 5000

BG = "#ffe4f0"
PANEL = "#ffd0e6"
BTN = "#ff9ecb"
BTN_ACTIVE = "#ff7ab8"
TEXT = "#7a2e5a"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kawaii Maid Viewer")
        self.geometry("900x760")
        self.minsize(560, 520)
        self.configure(bg=BG)

        self.pool = []
        self.current_pil = None
        self.current_tk = None
        self.slideshow_on = False
        self.slideshow_job = None
        self.loading = False

        tk.Label(self, text="\u2661 Kawaii Maid Viewer \u2661", bg=BG, fg=TEXT,
                 font=("Comic Sans MS", 22, "bold")).pack(pady=(14, 6))

        self.canvas = tk.Label(self, bg=PANEL, fg=TEXT,
                               text="Press \u201cGenerate\u201d to start \u2728",
                               font=("Comic Sans MS", 14))
        self.canvas.pack(fill="both", expand=True, padx=18, pady=6)
        self.canvas.bind("<Configure>", lambda e: self.render())

        self.status = tk.Label(self, text="", bg=BG, fg=TEXT,
                               font=("Comic Sans MS", 10))
        self.status.pack()

        bar = tk.Frame(self, bg=BG)
        bar.pack(pady=14)
        self.gen_btn = self.make_btn(bar, "\u2728 Generate New", self.generate)
        self.show_btn = self.make_btn(bar, "\u25B6 Slideshow", self.toggle_slideshow)
        self.save_btn = self.make_btn(bar, "\U0001F4BE Save Image", self.save)
        for b in (self.gen_btn, self.show_btn, self.save_btn):
            b.pack(side="left", padx=10)

        self.bind("<space>", lambda e: self.generate())
        self.after(300, self.generate)

    def make_btn(self, parent, text, cmd):
        return tk.Button(parent, text=text, command=cmd, bg=BTN, fg="white",
                         activebackground=BTN_ACTIVE, activeforeground="white",
                         relief="flat", bd=0, padx=18, pady=10, cursor="hand2",
                         font=("Comic Sans MS", 12, "bold"))

    # ---------- fetching ----------
    def generate(self):
        if self.loading:
            return
        self.loading = True
        self.status.config(text="Fetching a cutie... \u2661")
        threading.Thread(target=self._fetch, daemon=True).start()

    def _refill_pool(self):
        for pid in (random.randint(0, 40), 0):
            r = requests.get(API, headers=HEADERS, timeout=15, params={
                "page": "dapi", "s": "post", "q": "index", "json": 1,
                "limit": 100, "pid": pid, "tags": TAGS})
            r.raise_for_status()
            try:
                posts = r.json()
            except ValueError:
                posts = []
            posts = [p for p in posts if p.get("rating") == "general"
                     or p.get("rating") == "safe"]
            if posts:
                random.shuffle(posts)
                self.pool = posts
                return

    def _fetch(self):
        try:
            if not self.pool:
                self._refill_pool()
            if not self.pool:
                raise RuntimeError("No images found.")
            post = self.pool.pop()
            url = f"{IMG_BASE}/{post['directory']}/{post['image']}"
            data = requests.get(url, headers=HEADERS, timeout=30).content
            img = Image.open(io.BytesIO(data)).convert("RGB")
            self.after(0, lambda: self._show(img))
        except Exception as exc:
            self.after(0, lambda: self._error(str(exc)))

    def _show(self, img):
        self.current_pil = img
        self.loading = False
        self.status.config(text="")
        self.render()

    def _error(self, msg):
        self.loading = False
        self.status.config(text=f"Oops: {msg}")

    # ---------- display ----------
    def render(self):
        if self.current_pil is None:
            return
        w = max(self.canvas.winfo_width() - 8, 50)
        h = max(self.canvas.winfo_height() - 8, 50)
        img = self.current_pil.copy()
        img.thumbnail((w, h), Image.LANCZOS)
        self.current_tk = ImageTk.PhotoImage(img)
        self.canvas.config(image=self.current_tk, text="")

    # ---------- slideshow ----------
    def toggle_slideshow(self):
        self.slideshow_on = not self.slideshow_on
        if self.slideshow_on:
            self.show_btn.config(text="\u23F8 Stop Slideshow")
            self._tick()
        else:
            self.show_btn.config(text="\u25B6 Slideshow")
            if self.slideshow_job:
                self.after_cancel(self.slideshow_job)
                self.slideshow_job = None

    def _tick(self):
        if not self.slideshow_on:
            return
        self.generate()
        self.slideshow_job = self.after(SLIDESHOW_MS, self._tick)

    # ---------- save ----------
    def save(self):
        if self.current_pil is None:
            messagebox.showinfo("Nothing yet", "Generate an image first!")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if path:
            self.current_pil.save(path)
            self.status.config(text="Saved! \u2661")


if __name__ == "__main__":
    App().mainloop()
