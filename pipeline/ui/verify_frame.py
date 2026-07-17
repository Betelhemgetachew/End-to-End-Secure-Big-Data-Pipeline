import os
import customtkinter as ctk
from tkinter import filedialog

import gui_adapters
from ui import theme


class VerifyFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.file_path = None
        self.hash_path = None

        theme.page_header(
            self, "🔍", "Verify Dataset Integrity",
            "Compare a dataset's current SHA-256 hash against a previously stored hash to detect tampering."
        )

        card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        card.pack(fill="x", padx=28, pady=(0, 16))

        self.dataset_label = self._picker_row(card, "Dataset CSV", "Choose CSV", lambda: self._choose(is_hash=False))
        self.hash_label = self._picker_row(card, "Stored hash file", "Choose .sha256", lambda: self._choose(is_hash=True))

        self.run_button = ctk.CTkButton(
            self, text="Verify Integrity", height=46, corner_radius=10, state="disabled",
            font=theme.font(14, "bold"), fg_color=theme.BLUE_ACCENT, hover_color=theme.BLUE_ACCENT_HOVER,
            command=self._run_verify
        )
        self.run_button.pack(fill="x", padx=28, pady=(4, 16))

        result_card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        result_card.pack(fill="x", padx=28)
        self.result_label = ctk.CTkLabel(
            result_card, text="No check run yet.", font=theme.font(14, "bold"),
            text_color=theme.TEXT_MUTED, wraplength=700, justify="left"
        )
        self.result_label.pack(anchor="w", padx=24, pady=20)

    def _picker_row(self, parent, label_text, button_text, command):
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=14)
        ctk.CTkLabel(row, text=label_text, width=140, anchor="w", font=theme.font(14, "bold"), text_color=theme.TEXT_MUTED).pack(side="left")
        value_label = ctk.CTkLabel(row, text="Not selected", text_color=theme.TEXT_MUTED, anchor="w", font=theme.font(14))
        value_label.pack(side="left", fill="x", expand=True)
        ctk.CTkButton(
            row, text=button_text, width=150, height=34, corner_radius=8,
            fg_color=("gray80", "#243356"), hover_color=("gray70", "#2E3F66"),
            text_color=theme.TEXT_PRIMARY, font=theme.font(14, "bold"), command=command
        ).pack(side="right")
        return value_label

    def _choose(self, is_hash):
        if is_hash:
            path = filedialog.askopenfilename(title="Select hash file", filetypes=[("SHA-256 hash", "*.sha256"), ("All files", "*.*")])
            if path:
                self.hash_path = path
                self.hash_label.configure(text=f"📄  {os.path.basename(path)}", text_color=theme.TEXT_PRIMARY)
        else:
            path = filedialog.askopenfilename(title="Select dataset CSV", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if path:
                self.file_path = path
                self.dataset_label.configure(text=f"📄  {os.path.basename(path)}", text_color=theme.TEXT_PRIMARY)

        if self.file_path and self.hash_path:
            self.run_button.configure(state="normal")

    def _run_verify(self):
        result = gui_adapters.run_verify_integrity(self.username, self.role, self.file_path, self.hash_path)

        if not result["success"]:
            self.result_label.configure(text=f"🚫 {result['message']}", text_color=theme.DANGER)
        elif result["match"]:
            self.result_label.configure(text=f"✅ {result['message']}", text_color=theme.SUCCESS)
        else:
            self.result_label.configure(text=f"⚠️ {result['message']}", text_color=theme.WARNING)
