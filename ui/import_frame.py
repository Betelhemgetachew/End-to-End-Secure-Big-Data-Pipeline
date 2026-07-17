import os
import threading
import customtkinter as ctk
from tkinter import filedialog

import gui_adapters


class ImportFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.selected_path = None

        ctk.CTkLabel(
            self, text="Import Dataset", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(
            self,
            text="Upload a CSV file to validate, hash, encrypt sensitive fields, and load into PostgreSQL.",
            font=ctk.CTkFont(size=13), text_color="gray60"
        ).pack(anchor="w", padx=24, pady=(0, 20))

        # --- File picker card ---
        picker_card = ctk.CTkFrame(self, corner_radius=12)
        picker_card.pack(fill="x", padx=24, pady=(0, 16))

        row = ctk.CTkFrame(picker_card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=20)

        self.file_label = ctk.CTkLabel(
            row, text="No file selected", font=ctk.CTkFont(size=13), text_color="gray60", anchor="w"
        )
        self.file_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            row, text="📁 Choose CSV File", width=160, command=self._choose_file
        ).pack(side="right")

        # --- Run import button ---
        self.import_button = ctk.CTkButton(
            self, text="Run Secure Import Pipeline", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._run_import, state="disabled"
        )
        self.import_button.pack(fill="x", padx=24, pady=(0, 16))

        # --- Progress ---
        self.progress_bar = ctk.CTkProgressBar(self)
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=24, pady=(0, 4))

        self.status_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), text_color="gray60")
        self.status_label.pack(anchor="w", padx=24)

        # --- Result panel ---
        self.result_frame = ctk.CTkFrame(self, corner_radius=12, fg_color="transparent")
        self.result_frame.pack(fill="both", expand=True, padx=24, pady=(12, 24))
        self.result_text = ctk.CTkTextbox(self.result_frame, font=ctk.CTkFont(size=12, family="Courier"))
        self.result_text.pack(fill="both", expand=True)
        self.result_text.insert("1.0", "Import results will appear here.")
        self.result_text.configure(state="disabled")

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Select customer dataset CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        self.selected_path = path
        self.file_label.configure(text=os.path.basename(path), text_color=("black", "white"))
        self.import_button.configure(state="normal")
        self.progress_bar.set(0)
        self.status_label.configure(text="")

    def _run_import(self):
        if not self.selected_path:
            return

        self.import_button.configure(state="disabled", text="Importing...")
        self.progress_bar.set(0)
        self._set_result("Running import pipeline...\n")

        thread = threading.Thread(target=self._import_worker, daemon=True)
        thread.start()

    def _import_worker(self):
        def progress_cb(step, pct):
            self.after(0, lambda: self._update_progress(step, pct))

        result = gui_adapters.run_import_pipeline(
            self.username, self.role, self.selected_path, progress_cb=progress_cb
        )
        self.after(0, lambda: self._show_result(result))

    def _update_progress(self, step, pct):
        self.progress_bar.set(pct / 100)
        self.status_label.configure(text=step)

    def _show_result(self, result):
        self.import_button.configure(state="normal", text="Run Secure Import Pipeline")

        lines = []
        if result["success"]:
            lines.append("✅ IMPORT SUCCESSFUL")
            lines.append(f"Batch ID       : {result['batch_id']}")
            lines.append(f"Upload ID      : {result['upload_id']}")
            lines.append(f"Records loaded : {result['record_count']:,}")
            lines.append(f"SHA-256 hash   : {result['file_hash']}")
            lines.append(f"Hash saved to  : {result['hash_file']}")
            self.status_label.configure(text="Import complete.")
        else:
            lines.append("❌ IMPORT FAILED")
            lines.append(f"Stage   : {result.get('stage')}")
            lines.append(f"Message : {result.get('message')}")
            if result.get("trace"):
                lines.append("")
                lines.append(result["trace"])
            self.status_label.configure(text=result.get("message", "Import failed."))

        self._set_result("\n".join(lines))

    def _set_result(self, text):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")
