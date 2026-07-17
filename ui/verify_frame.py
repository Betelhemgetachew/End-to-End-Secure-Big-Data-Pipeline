import os
import customtkinter as ctk
from tkinter import filedialog

import gui_adapters


class VerifyFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.file_path = None
        self.hash_path = None

        ctk.CTkLabel(
            self, text="Verify Dataset Integrity", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(
            self,
            text="Compare a dataset's current SHA-256 hash against a previously stored hash to detect tampering.",
            font=ctk.CTkFont(size=13), text_color="gray60", wraplength=700, justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))

        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=24, pady=(0, 16))

        self.dataset_label = self._picker_row(
            card, "Dataset CSV:", "Choose CSV",
            lambda: self._choose(is_hash=False)
        )
        self.hash_label = self._picker_row(
            card, "Stored hash file:", "Choose .sha256",
            lambda: self._choose(is_hash=True)
        )

        self.run_button = ctk.CTkButton(
            self, text="Verify Integrity", height=42, state="disabled",
            font=ctk.CTkFont(size=14, weight="bold"), command=self._run_verify
        )
        self.run_button.pack(fill="x", padx=24, pady=(4, 16))

        self.result_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14, weight="bold"), wraplength=700)
        self.result_label.pack(anchor="w", padx=24)

    def _picker_row(self, parent, label_text, button_text, command):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=12)
        ctk.CTkLabel(row, text=label_text, width=130, anchor="w").pack(side="left")
        value_label = ctk.CTkLabel(row, text="Not selected", text_color="gray60", anchor="w")
        value_label.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(row, text=button_text, width=140, command=command).pack(side="right")
        return value_label

    def _choose(self, is_hash):
        if is_hash:
            path = filedialog.askopenfilename(title="Select hash file", filetypes=[("SHA-256 hash", "*.sha256"), ("All files", "*.*")])
            if path:
                self.hash_path = path
                self.hash_label.configure(text=os.path.basename(path), text_color=("black", "white"))
        else:
            path = filedialog.askopenfilename(title="Select dataset CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if path:
                self.file_path = path
                self.dataset_label.configure(text=os.path.basename(path), text_color=("black", "white"))

        if self.file_path and self.hash_path:
            self.run_button.configure(state="normal")

    def _run_verify(self):
        result = gui_adapters.run_verify_integrity(self.username, self.role, self.file_path, self.hash_path)

        if not result["success"]:
            self.result_label.configure(text=f"🚫 {result['message']}", text_color="#e74c3c")
        elif result["match"]:
            self.result_label.configure(text=f"✅ {result['message']}", text_color="#2ecc71")
        else:
            self.result_label.configure(text=f"⚠️ {result['message']}", text_color="#f39c12")
