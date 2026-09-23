import json
import re
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image, ImageTk, ImageFilter


# ============================================================
# GENERIC SPRITE CROPPER v3
#
# Requisiti:
#   pip install pillow numpy
#
# Opzionale per DDS:
#   texconv.exe nella stessa cartella dello script oppure nel PATH
#
# Funzioni:
# - numero illimitato di selezioni
# - nome manuale o automatico per ogni riquadro
# - crop comune modificabile a runtime
# - output modificabile a runtime
# - rimozione background
# - preview
# - rinomina / elimina selezioni
# - salvataggio e caricamento progetto JSON
# - export PNG
# - export DDS DXT5 automatico con texconv
# ============================================================


DEFAULT_CROP_W = 190
DEFAULT_CROP_H = 190

# Comodo per icone HOI4, ma completamente modificabile
DEFAULT_OUTPUT_W = 70
DEFAULT_OUTPUT_H = 70


# ============================================================
# HELPERS
# ============================================================

def sanitize_filename(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", name)
    name = re.sub(r"\s+", "_", name)
    name = name.strip("._ ")
    return name or "unnamed"


def find_texconv():
    local = Path(__file__).resolve().parent / "texconv.exe"
    if local.exists():
        return str(local)

    return shutil.which("texconv.exe") or shutil.which("texconv")


def estimate_border_color(img_rgba, border=5):
    rgb = np.asarray(img_rgba.convert("RGB"))
    h, w, _ = rgb.shape
    b = max(1, min(border, h // 4, w // 4))

    pixels = np.concatenate([
        rgb[:b, :, :].reshape(-1, 3),
        rgb[-b:, :, :].reshape(-1, 3),
        rgb[:, :b, :].reshape(-1, 3),
        rgb[:, -b:, :].reshape(-1, 3),
    ], axis=0)

    med = np.median(pixels, axis=0)
    return tuple(int(x) for x in med)


def connected_background_mask(candidate):
    h, w = candidate.shape
    visited = np.zeros((h, w), dtype=bool)
    q = deque()

    def push(y, x):
        if 0 <= y < h and 0 <= x < w:
            if candidate[y, x] and not visited[y, x]:
                visited[y, x] = True
                q.append((y, x))

    for x in range(w):
        push(0, x)
        push(h - 1, x)

    for y in range(h):
        push(y, 0)
        push(y, w - 1)

    while q:
        y, x = q.popleft()
        push(y - 1, x)
        push(y + 1, x)
        push(y, x - 1)
        push(y, x + 1)

    return visited


def remove_background(img_rgba, bg_rgb, tolerance=55, feather=1.5):
    arr = np.asarray(img_rgba.convert("RGBA")).copy()
    rgb = arr[:, :, :3].astype(np.int16)

    bg = np.array(bg_rgb, dtype=np.int16).reshape(1, 1, 3)
    dist = np.sqrt(np.sum((rgb - bg) ** 2, axis=2))

    candidate = dist <= float(tolerance)
    bg_mask = connected_background_mask(candidate)

    alpha = np.full(bg_mask.shape, 255, dtype=np.uint8)
    alpha[bg_mask] = 0

    alpha_img = Image.fromarray(alpha, mode="L")

    if feather > 0:
        alpha_img = alpha_img.filter(
            ImageFilter.GaussianBlur(radius=float(feather))
        )

    original_alpha = Image.fromarray(arr[:, :, 3], mode="L")

    alpha_arr = np.minimum(
        np.asarray(alpha_img, dtype=np.uint8),
        np.asarray(original_alpha, dtype=np.uint8)
    )

    out = Image.fromarray(arr, mode="RGBA")
    out.putalpha(Image.fromarray(alpha_arr, mode="L"))
    return out


def fit_to_canvas(img, width, height, keep_aspect=True):
    if not keep_aspect:
        return img.resize((width, height), Image.Resampling.LANCZOS)

    copy = img.copy()
    copy.thumbnail((width, height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    x = (width - copy.width) // 2
    y = (height - copy.height) // 2
    canvas.alpha_composite(copy, (x, y))
    return canvas


def convert_png_to_dds(png_file, dds_dir):
    texconv = find_texconv()

    if not texconv:
        return False, "texconv.exe non trovato"

    dds_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        texconv,
        "-y",
        "-f", "DXT5",
        "-m", "1",
        "-o", str(dds_dir.resolve()),
        str(png_file.resolve()),
    ]

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    if result.returncode != 0:
        return False, result.stdout

    return True, ""


# ============================================================
# APP
# ============================================================

class GenericSpriteCropper:
    def __init__(self, root):
        self.root = root
        self.root.title("Generic Sprite Cropper v3")
        self.root.geometry("1450x880")

        self.image_path = None
        self.original = None
        self.display = None
        self.tk_image = None
        self.scale = 1.0

        # Ogni selezione:
        # {
        #   "name": str,
        #   "cx": int,
        #   "cy": int
        # }
        self.items = []
        self.selected_index = None

        self.mode = "add"
        self.drag_start = None
        self.temp_rect = None
        self.hover_rect = None

        self.sampled_bg = None
        self.output_root = Path.cwd() / "export"

        # Runtime vars
        self.crop_w_var = tk.IntVar(value=DEFAULT_CROP_W)
        self.crop_h_var = tk.IntVar(value=DEFAULT_CROP_H)

        self.out_w_var = tk.IntVar(value=DEFAULT_OUTPUT_W)
        self.out_h_var = tk.IntVar(value=DEFAULT_OUTPUT_H)

        self.keep_aspect_var = tk.BooleanVar(value=True)

        self.remove_bg_var = tk.BooleanVar(value=True)
        self.bg_mode_var = tk.StringVar(value="Auto dai bordi")
        self.tolerance_var = tk.IntVar(value=55)
        self.feather_var = tk.DoubleVar(value=1.5)

        self.ask_name_var = tk.BooleanVar(value=True)
        self.auto_prefix_var = tk.StringVar(value="icon")
        self.auto_counter_var = tk.IntVar(value=1)
        self.auto_digits_var = tk.IntVar(value=3)

        self.export_png_var = tk.BooleanVar(value=True)
        self.export_dds_var = tk.BooleanVar(value=True)

        self.build_ui()
        self.update_status()

    # --------------------------------------------------------
    # UI
    # --------------------------------------------------------

    def build_ui(self):
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)

        left = ttk.Frame(outer, padding=10)
        left.pack(side="left", fill="y")

        center = ttk.Frame(outer)
        center.pack(side="left", fill="both", expand=True)

        right = ttk.Frame(outer, padding=8)
        right.pack(side="right", fill="y")

        # ----------------------------------------------------
        # LEFT
        # ----------------------------------------------------

        ttk.Label(
            left,
            text="GENERIC SPRITE CROPPER",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ttk.Button(
            left,
            text="Apri immagine",
            command=self.open_image
        ).pack(fill="x", pady=(8, 3))

        ttk.Button(
            left,
            text="Salva progetto",
            command=self.save_project
        ).pack(fill="x", pady=2)

        ttk.Button(
            left,
            text="Carica progetto",
            command=self.load_project
        ).pack(fill="x", pady=(2, 10))

        # Crop
        crop_box = ttk.LabelFrame(left, text="Crop comune", padding=8)
        crop_box.pack(fill="x", pady=5)

        row = ttk.Frame(crop_box)
        row.pack(fill="x")

        ttk.Label(row, text="W").pack(side="left")
        ttk.Entry(
            row,
            textvariable=self.crop_w_var,
            width=7
        ).pack(side="left", padx=(4, 10))

        ttk.Label(row, text="H").pack(side="left")
        ttk.Entry(
            row,
            textvariable=self.crop_h_var,
            width=7
        ).pack(side="left", padx=4)

        ttk.Button(
            crop_box,
            text="Misura col mouse",
            command=self.start_measure_crop
        ).pack(fill="x", pady=(8, 3))

        ttk.Button(
            crop_box,
            text="Applica / ridisegna",
            command=self.redraw
        ).pack(fill="x")

        # Output
        out_box = ttk.LabelFrame(left, text="Dimensione output", padding=8)
        out_box.pack(fill="x", pady=5)

        row = ttk.Frame(out_box)
        row.pack(fill="x")

        ttk.Label(row, text="W").pack(side="left")
        ttk.Entry(
            row,
            textvariable=self.out_w_var,
            width=7
        ).pack(side="left", padx=(4, 10))

        ttk.Label(row, text="H").pack(side="left")
        ttk.Entry(
            row,
            textvariable=self.out_h_var,
            width=7
        ).pack(side="left", padx=4)

        ttk.Checkbutton(
            out_box,
            text="Mantieni proporzioni",
            variable=self.keep_aspect_var
        ).pack(anchor="w", pady=(6, 0))

        ttk.Label(
            out_box,
            text="Default: 70 × 70 px"
        ).pack(anchor="w", pady=(4, 0))

        # Naming
        name_box = ttk.LabelFrame(left, text="Nomi dei riquadri", padding=8)
        name_box.pack(fill="x", pady=5)

        ttk.Checkbutton(
            name_box,
            text="Chiedi il nome ad ogni click",
            variable=self.ask_name_var
        ).pack(anchor="w")

        ttk.Label(
            name_box,
            text="Prefisso automatico"
        ).pack(anchor="w", pady=(7, 0))

        ttk.Entry(
            name_box,
            textvariable=self.auto_prefix_var
        ).pack(fill="x")

        row = ttk.Frame(name_box)
        row.pack(fill="x", pady=(5, 0))

        ttk.Label(row, text="Contatore").pack(side="left")
        ttk.Entry(
            row,
            textvariable=self.auto_counter_var,
            width=6
        ).pack(side="left", padx=(5, 10))

        ttk.Label(row, text="Cifre").pack(side="left")
        ttk.Spinbox(
            row,
            from_=1,
            to=8,
            textvariable=self.auto_digits_var,
            width=4
        ).pack(side="left", padx=5)

        ttk.Label(
            name_box,
            text="Esempio: icon_001, icon_002..."
        ).pack(anchor="w", pady=(5, 0))

        # Background
        bg_box = ttk.LabelFrame(left, text="Rimozione background", padding=8)
        bg_box.pack(fill="x", pady=5)

        ttk.Checkbutton(
            bg_box,
            text="Rimuovi background",
            variable=self.remove_bg_var
        ).pack(anchor="w")

        ttk.Combobox(
            bg_box,
            textvariable=self.bg_mode_var,
            values=["Auto dai bordi", "Colore campionato"],
            state="readonly"
        ).pack(fill="x", pady=(5, 0))

        ttk.Button(
            bg_box,
            text="Campiona colore con click",
            command=self.start_sample_background
        ).pack(fill="x", pady=(5, 0))

        self.bg_swatch = tk.Label(
            bg_box,
            text="nessun colore campionato",
            bg="#303030",
            fg="white",
            relief="sunken"
        )
        self.bg_swatch.pack(fill="x", pady=(4, 0))

        ttk.Label(bg_box, text="Tolleranza").pack(anchor="w", pady=(6, 0))

        tk.Scale(
            bg_box,
            from_=0,
            to=180,
            orient="horizontal",
            variable=self.tolerance_var,
            resolution=1
        ).pack(fill="x")

        ttk.Label(bg_box, text="Feather").pack(anchor="w")

        tk.Scale(
            bg_box,
            from_=0,
            to=5,
            orient="horizontal",
            variable=self.feather_var,
            resolution=0.5
        ).pack(fill="x")

        # Export
        export_box = ttk.LabelFrame(left, text="Export", padding=8)
        export_box.pack(fill="x", pady=5)

        ttk.Checkbutton(
            export_box,
            text="PNG",
            variable=self.export_png_var
        ).pack(anchor="w")

        ttk.Checkbutton(
            export_box,
            text="DDS DXT5",
            variable=self.export_dds_var
        ).pack(anchor="w")

        ttk.Button(
            export_box,
            text="Scegli cartella output",
            command=self.choose_output_folder
        ).pack(fill="x", pady=(5, 0))

        self.output_label = ttk.Label(
            export_box,
            text=str(self.output_root),
            wraplength=220
        )
        self.output_label.pack(anchor="w", pady=(4, 0))

        ttk.Button(
            left,
            text="ESPORTA TUTTO",
            command=self.export_all
        ).pack(fill="x", pady=(10, 0), ipady=6)

        self.status_label = ttk.Label(
            left,
            text="",
            wraplength=230
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

        # ----------------------------------------------------
        # CENTER CANVAS
        # ----------------------------------------------------

        self.canvas = tk.Canvas(
            center,
            bg="#202020",
            cursor="cross"
        )
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # ----------------------------------------------------
        # RIGHT LIST
        # ----------------------------------------------------

        ttk.Label(
            right,
            text="RIQUADRI",
            font=("Segoe UI", 11, "bold")
        ).pack(anchor="w")

        self.tree = ttk.Treeview(
            right,
            columns=("name", "x", "y"),
            show="headings",
            height=28,
            selectmode="browse"
        )

        self.tree.heading("name", text="Nome")
        self.tree.heading("x", text="X")
        self.tree.heading("y", text="Y")

        self.tree.column("name", width=180)
        self.tree.column("x", width=55, anchor="center")
        self.tree.column("y", width=55, anchor="center")

        self.tree.pack(fill="both", expand=True, pady=(5, 5))

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.rename_selected())

        ttk.Button(
            right,
            text="Rinomina",
            command=self.rename_selected
        ).pack(fill="x", pady=2)

        ttk.Button(
            right,
            text="Anteprima",
            command=self.preview_selected
        ).pack(fill="x", pady=2)

        ttk.Button(
            right,
            text="Elimina",
            command=self.delete_selected
        ).pack(fill="x", pady=2)

        ttk.Button(
            right,
            text="Elimina tutti",
            command=self.clear_all
        ).pack(fill="x", pady=(2, 10))

        ttk.Label(
            right,
            text="Doppio click su una voce = rinomina",
            wraplength=260
        ).pack(anchor="w")

    # --------------------------------------------------------
    # STATUS / TREE
    # --------------------------------------------------------

    def update_status(self):
        self.status_label.config(
            text=(
                f"Riquadri: {len(self.items)}\n"
                f"Modalità: {self.mode}\n"
                f"Crop: {self.crop_w_var.get()} × {self.crop_h_var.get()}\n"
                f"Output: {self.out_w_var.get()} × {self.out_h_var.get()}"
            )
        )

    def refresh_tree(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        for idx, item in enumerate(self.items):
            self.tree.insert(
                "",
                "end",
                iid=str(idx),
                values=(item["name"], item["cx"], item["cy"])
            )

        if self.selected_index is not None:
            if 0 <= self.selected_index < len(self.items):
                self.tree.selection_set(str(self.selected_index))
                self.tree.focus(str(self.selected_index))

        self.update_status()

    def on_tree_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return

        try:
            self.selected_index = int(sel[0])
        except Exception:
            return

        self.redraw()

    # --------------------------------------------------------
    # OPEN / PROJECT
    # --------------------------------------------------------

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Seleziona immagine",
            filetypes=[
                ("Immagini", "*.png *.jpg *.jpeg *.bmp *.webp"),
                ("Tutti i file", "*.*"),
            ]
        )

        if not path:
            return

        self.image_path = Path(path)
        self.original = Image.open(path).convert("RGBA")
        self.items.clear()
        self.selected_index = None
        self.sampled_bg = None
        self.mode = "add"

        self.fit_image()
        self.redraw()
        self.refresh_tree()

    def save_project(self):
        if self.image_path is None:
            messagebox.showwarning(
                "Nessuna immagine",
                "Apri prima un'immagine."
            )
            return

        path = filedialog.asksaveasfilename(
            title="Salva progetto",
            defaultextension=".json",
            filetypes=[("Progetto JSON", "*.json")]
        )

        if not path:
            return

        data = {
            "image_path": str(self.image_path),
            "crop_w": self.crop_w_var.get(),
            "crop_h": self.crop_h_var.get(),
            "output_w": self.out_w_var.get(),
            "output_h": self.out_h_var.get(),
            "keep_aspect": self.keep_aspect_var.get(),
            "remove_bg": self.remove_bg_var.get(),
            "bg_mode": self.bg_mode_var.get(),
            "sampled_bg": self.sampled_bg,
            "tolerance": self.tolerance_var.get(),
            "feather": self.feather_var.get(),
            "auto_prefix": self.auto_prefix_var.get(),
            "auto_counter": self.auto_counter_var.get(),
            "auto_digits": self.auto_digits_var.get(),
            "items": self.items,
        }

        Path(path).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )

        messagebox.showinfo("Progetto", "Progetto salvato.")

    def load_project(self):
        path = filedialog.askopenfilename(
            title="Carica progetto",
            filetypes=[("Progetto JSON", "*.json")]
        )

        if not path:
            return

        try:
            data = json.loads(
                Path(path).read_text(encoding="utf-8")
            )

            img_path = Path(data["image_path"])

            if not img_path.exists():
                messagebox.showerror(
                    "Immagine non trovata",
                    f"Il progetto punta a:\n{img_path}"
                )
                return

            self.image_path = img_path
            self.original = Image.open(img_path).convert("RGBA")

            self.crop_w_var.set(data.get("crop_w", DEFAULT_CROP_W))
            self.crop_h_var.set(data.get("crop_h", DEFAULT_CROP_H))

            self.out_w_var.set(data.get("output_w", DEFAULT_OUTPUT_W))
            self.out_h_var.set(data.get("output_h", DEFAULT_OUTPUT_H))

            self.keep_aspect_var.set(data.get("keep_aspect", True))

            self.remove_bg_var.set(data.get("remove_bg", True))
            self.bg_mode_var.set(data.get("bg_mode", "Auto dai bordi"))

            sampled = data.get("sampled_bg")
            self.sampled_bg = tuple(sampled) if sampled else None

            self.tolerance_var.set(data.get("tolerance", 55))
            self.feather_var.set(data.get("feather", 1.5))

            self.auto_prefix_var.set(data.get("auto_prefix", "icon"))
            self.auto_counter_var.set(data.get("auto_counter", 1))
            self.auto_digits_var.set(data.get("auto_digits", 3))

            self.items = data.get("items", [])
            self.selected_index = None
            self.mode = "add"

            self.update_swatch()
            self.fit_image()
            self.redraw()
            self.refresh_tree()

        except Exception as exc:
            messagebox.showerror(
                "Errore progetto",
                str(exc)
            )

    # --------------------------------------------------------
    # CANVAS HELPERS
    # --------------------------------------------------------

    def fit_image(self):
        if self.original is None:
            return

        self.root.update_idletasks()

        cw = max(self.canvas.winfo_width(), 700)
        ch = max(self.canvas.winfo_height(), 600)

        iw, ih = self.original.size

        self.scale = min(
            cw / iw,
            ch / ih,
            1.0
        )

        dw = max(1, int(iw * self.scale))
        dh = max(1, int(ih * self.scale))

        self.display = self.original.resize(
            (dw, dh),
            Image.Resampling.LANCZOS
        )

        self.tk_image = ImageTk.PhotoImage(self.display)

    def image_xy(self, canvas_x, canvas_y):
        return (
            int(canvas_x / self.scale),
            int(canvas_y / self.scale)
        )

    def canvas_xy(self, image_x, image_y):
        return (
            int(image_x * self.scale),
            int(image_y * self.scale)
        )

    def crop_box_from_center(self, cx, cy):
        w = max(1, int(self.crop_w_var.get()))
        h = max(1, int(self.crop_h_var.get()))

        x1 = int(round(cx - w / 2))
        y1 = int(round(cy - h / 2))

        return (
            x1,
            y1,
            x1 + w,
            y1 + h
        )

    def valid_box(self, box):
        if self.original is None:
            return False

        x1, y1, x2, y2 = box
        iw, ih = self.original.size

        return (
            x1 >= 0 and
            y1 >= 0 and
            x2 <= iw and
            y2 <= ih
        )

    # --------------------------------------------------------
    # DRAW
    # --------------------------------------------------------

    def redraw(self):
        if self.original is None:
            return

        try:
            if self.crop_w_var.get() <= 0:
                raise ValueError
            if self.crop_h_var.get() <= 0:
                raise ValueError
        except Exception:
            return

        self.fit_image()

        self.canvas.delete("all")

        self.canvas.create_image(
            0, 0,
            anchor="nw",
            image=self.tk_image
        )

        for idx, item in enumerate(self.items):
            box = self.crop_box_from_center(
                item["cx"],
                item["cy"]
            )

            x1, y1, x2, y2 = box
            ax1, ay1 = self.canvas_xy(x1, y1)
            ax2, ay2 = self.canvas_xy(x2, y2)

            selected = idx == self.selected_index

            self.canvas.create_rectangle(
                ax1, ay1, ax2, ay2,
                outline="#ffcc33" if selected else "#55ff55",
                width=3 if selected else 2
            )

            self.canvas.create_text(
                ax1 + 5,
                ay1 + 5,
                anchor="nw",
                text=item["name"],
                fill="#ffff66",
                font=("Segoe UI", 9, "bold")
            )

    # --------------------------------------------------------
    # MODES
    # --------------------------------------------------------

    def start_measure_crop(self):
        if self.original is None:
            messagebox.showwarning(
                "Nessuna immagine",
                "Apri prima un'immagine."
            )
            return

        self.mode = "measure_crop"
        self.update_status()

    def start_sample_background(self):
        if self.original is None:
            messagebox.showwarning(
                "Nessuna immagine",
                "Apri prima un'immagine."
            )
            return

        self.mode = "sample_bg"
        self.update_status()

    # --------------------------------------------------------
    # MOUSE
    # --------------------------------------------------------

    def on_mouse_down(self, event):
        if self.original is None:
            return

        if self.mode == "measure_crop":
            self.drag_start = (event.x, event.y)

    def on_mouse_drag(self, event):
        if self.mode != "measure_crop":
            return

        if self.drag_start is None:
            return

        if self.temp_rect:
            self.canvas.delete(self.temp_rect)

        x1, y1 = self.drag_start

        self.temp_rect = self.canvas.create_rectangle(
            x1, y1,
            event.x, event.y,
            outline="#ff5555",
            width=2
        )

    def on_mouse_up(self, event):
        if self.original is None:
            return

        if self.mode == "measure_crop":
            self.finish_measure_crop(event)
            return

        if self.mode == "sample_bg":
            self.finish_sample_background(event)
            return

        if self.mode == "add":
            self.add_item_at_click(event)
            return

    def on_mouse_move(self, event):
        if self.original is None:
            return

        if self.mode != "add":
            return

        if self.hover_rect:
            self.canvas.delete(self.hover_rect)

        ix, iy = self.image_xy(event.x, event.y)
        box = self.crop_box_from_center(ix, iy)

        x1, y1, x2, y2 = box
        ax1, ay1 = self.canvas_xy(x1, y1)
        ax2, ay2 = self.canvas_xy(x2, y2)

        self.hover_rect = self.canvas.create_rectangle(
            ax1, ay1, ax2, ay2,
            outline="#55ddff",
            dash=(4, 3)
        )

    def finish_measure_crop(self, event):
        if self.drag_start is None:
            return

        x1, y1 = self.drag_start

        ix1, iy1 = self.image_xy(
            min(x1, event.x),
            min(y1, event.y)
        )

        ix2, iy2 = self.image_xy(
            max(x1, event.x),
            max(y1, event.y)
        )

        w = max(1, ix2 - ix1)
        h = max(1, iy2 - iy1)

        self.crop_w_var.set(w)
        self.crop_h_var.set(h)

        self.drag_start = None
        self.mode = "add"

        self.redraw()
        self.update_status()

    def finish_sample_background(self, event):
        ix, iy = self.image_xy(event.x, event.y)

        iw, ih = self.original.size

        if not (
            0 <= ix < iw and
            0 <= iy < ih
        ):
            return

        r, g, b, a = self.original.getpixel((ix, iy))

        self.sampled_bg = (r, g, b)
        self.bg_mode_var.set("Colore campionato")

        self.update_swatch()

        self.mode = "add"
        self.update_status()

    def update_swatch(self):
        if self.sampled_bg is None:
            self.bg_swatch.config(
                text="nessun colore campionato",
                bg="#303030",
                fg="white"
            )
            return

        r, g, b = self.sampled_bg

        hexcol = f"#{r:02x}{g:02x}{b:02x}"

        brightness = (
            r * 299 +
            g * 587 +
            b * 114
        ) / 1000

        fg = "black" if brightness > 150 else "white"

        self.bg_swatch.config(
            text=f"RGB {self.sampled_bg}",
            bg=hexcol,
            fg=fg
        )

    # --------------------------------------------------------
    # ITEMS
    # --------------------------------------------------------

    def next_auto_name(self):
        prefix = sanitize_filename(
            self.auto_prefix_var.get() or "icon"
        )

        counter = int(self.auto_counter_var.get())
        digits = int(self.auto_digits_var.get())

        return f"{prefix}_{counter:0{digits}d}"

    def unique_name(self, base_name):
        existing = {
            item["name"].lower()
            for item in self.items
        }

        candidate = sanitize_filename(base_name)

        if candidate.lower() not in existing:
            return candidate

        n = 2

        while True:
            alt = f"{candidate}_{n}"

            if alt.lower() not in existing:
                return alt

            n += 1

    def add_item_at_click(self, event):
        ix, iy = self.image_xy(
            event.x,
            event.y
        )

        box = self.crop_box_from_center(
            ix,
            iy
        )

        if not self.valid_box(box):
            messagebox.showwarning(
                "Crop fuori immagine",
                "Il crop uscirebbe dai limiti dell'immagine."
            )
            return

        suggested = self.next_auto_name()

        if self.ask_name_var.get():
            entered = simpledialog.askstring(
                "Nome riquadro",
                "Nome del nuovo riquadro:",
                initialvalue=suggested,
                parent=self.root
            )

            if entered is None:
                return

            name = self.unique_name(entered)

        else:
            name = self.unique_name(suggested)

        self.items.append({
            "name": name,
            "cx": ix,
            "cy": iy,
        })

        self.selected_index = len(self.items) - 1

        self.auto_counter_var.set(
            int(self.auto_counter_var.get()) + 1
        )

        self.redraw()
        self.refresh_tree()

    def rename_selected(self):
        if self.selected_index is None:
            return

        if not (
            0 <= self.selected_index < len(self.items)
        ):
            return

        current = self.items[self.selected_index]["name"]

        new = simpledialog.askstring(
            "Rinomina",
            "Nuovo nome:",
            initialvalue=current,
            parent=self.root
        )

        if new is None:
            return

        # ignora sé stesso nel controllo duplicati
        others = {
            item["name"].lower()
            for idx, item in enumerate(self.items)
            if idx != self.selected_index
        }

        new = sanitize_filename(new)

        base = new
        n = 2

        while new.lower() in others:
            new = f"{base}_{n}"
            n += 1

        self.items[self.selected_index]["name"] = new

        self.redraw()
        self.refresh_tree()

    def delete_selected(self):
        if self.selected_index is None:
            return

        if not (
            0 <= self.selected_index < len(self.items)
        ):
            return

        del self.items[self.selected_index]

        if not self.items:
            self.selected_index = None
        else:
            self.selected_index = min(
                self.selected_index,
                len(self.items) - 1
            )

        self.redraw()
        self.refresh_tree()

    def clear_all(self):
        if not self.items:
            return

        if not messagebox.askyesno(
            "Conferma",
            "Eliminare tutti i riquadri?"
        ):
            return

        self.items.clear()
        self.selected_index = None

        self.redraw()
        self.refresh_tree()

    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------

    def process_item(self, item):
        box = self.crop_box_from_center(
            item["cx"],
            item["cy"]
        )

        if not self.valid_box(box):
            raise ValueError(
                f"Crop fuori immagine: {item['name']}"
            )

        crop = self.original.crop(box).convert("RGBA")

        if self.remove_bg_var.get():
            if self.bg_mode_var.get() == "Colore campionato":
                if self.sampled_bg is None:
                    raise ValueError(
                        "Hai scelto 'Colore campionato' "
                        "ma non hai campionato alcun colore."
                    )

                bg_rgb = self.sampled_bg

            else:
                bg_rgb = estimate_border_color(crop)

            crop = remove_background(
                crop,
                bg_rgb,
                tolerance=int(self.tolerance_var.get()),
                feather=float(self.feather_var.get())
            )

        return fit_to_canvas(
            crop,
            int(self.out_w_var.get()),
            int(self.out_h_var.get()),
            keep_aspect=self.keep_aspect_var.get()
        )

    def preview_selected(self):
        if self.selected_index is None:
            messagebox.showinfo(
                "Anteprima",
                "Seleziona prima un riquadro dalla lista."
            )
            return

        item = self.items[self.selected_index]

        try:
            img = self.process_item(item)
        except Exception as exc:
            messagebox.showerror(
                "Errore anteprima",
                str(exc)
            )
            return

        zoom = max(
            3,
            min(
                8,
                420 // max(img.width, img.height)
            )
        )

        prev = img.resize(
            (
                img.width * zoom,
                img.height * zoom
            ),
            Image.Resampling.NEAREST
        )

        tile = 16

        bg = Image.new(
            "RGBA",
            prev.size,
            (80, 80, 80, 255)
        )

        arr = np.asarray(bg).copy()

        for y in range(0, prev.height, tile):
            for x in range(0, prev.width, tile):
                if (
                    (x // tile) +
                    (y // tile)
                ) % 2 == 0:
                    arr[
                        y:y + tile,
                        x:x + tile,
                        :3
                    ] = (125, 125, 125)

        bg = Image.fromarray(arr, mode="RGBA")
        bg.alpha_composite(prev)

        top = tk.Toplevel(self.root)
        top.title(f"Anteprima - {item['name']}")

        tkprev = ImageTk.PhotoImage(bg)

        label = tk.Label(
            top,
            image=tkprev
        )
        label.image = tkprev
        label.pack(padx=10, pady=10)

        ttk.Label(
            top,
            text=(
                f"{item['name']}\n"
                f"Crop: {self.crop_w_var.get()} × "
                f"{self.crop_h_var.get()}\n"
                f"Output: {self.out_w_var.get()} × "
                f"{self.out_h_var.get()}"
            )
        ).pack(pady=(0, 10))

    # --------------------------------------------------------
    # EXPORT
    # --------------------------------------------------------

    def choose_output_folder(self):
        path = filedialog.askdirectory(
            title="Cartella output"
        )

        if not path:
            return

        self.output_root = Path(path)
        self.output_label.config(
            text=str(self.output_root)
        )

    def export_all(self):
        if self.original is None:
            messagebox.showwarning(
                "Nessuna immagine",
                "Apri prima un'immagine."
            )
            return

        if not self.items:
            messagebox.showwarning(
                "Nessun riquadro",
                "Aggiungi almeno un riquadro."
            )
            return

        if not (
            self.export_png_var.get() or
            self.export_dds_var.get()
        ):
            messagebox.showwarning(
                "Formato",
                "Seleziona almeno PNG o DDS."
            )
            return

        png_dir = self.output_root / "png"
        dds_dir = self.output_root / "dds"

        png_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        dds_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        texconv_missing = (
            self.export_dds_var.get() and
            not find_texconv()
        )

        errors = []
        exported = 0

        for item in self.items:
            try:
                img = self.process_item(item)

                filename = (
                    sanitize_filename(item["name"]) +
                    ".png"
                )

                png_path = png_dir / filename

                # PNG temporaneo serve comunque per texconv
                img.save(png_path)

                if self.export_dds_var.get():
                    ok, msg = convert_png_to_dds(
                        png_path,
                        dds_dir
                    )

                    if not ok:
                        errors.append(
                            f"{item['name']}: {msg}"
                        )

                if not self.export_png_var.get():
                    try:
                        png_path.unlink()
                    except Exception:
                        pass

                exported += 1

            except Exception as exc:
                errors.append(
                    f"{item['name']}: {exc}"
                )

        message = (
            f"Esportati: {exported}/{len(self.items)}\n\n"
            f"Cartella:\n{self.output_root}"
        )

        if texconv_missing:
            message += (
                "\n\nATTENZIONE: texconv.exe non trovato, "
                "quindi i DDS non sono stati creati."
            )

        if errors:
            message += (
                "\n\nErrori:\n" +
                "\n".join(errors[:10])
            )

            messagebox.showwarning(
                "Export completato con avvisi",
                message
            )

        else:
            messagebox.showinfo(
                "Export completato",
                message
            )


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    root = tk.Tk()
    app = GenericSpriteCropper(root)
    root.mainloop()
