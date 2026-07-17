import os
import customtkinter as ctk
from tkinter import filedialog

import gui_adapters
from ui import theme


class ValidateFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.selected_path = None

        theme.page_header(
            self, "🧪", "Validate Dataset",
            "Check a CSV for missing values, duplicate emails/account numbers, invalid account "
            "types, and negative balances. This does not import the data."
        )

        picker_card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        picker_card.pack(fill="x", padx=28, pady=(0, 16))
        row = ctk.CTkFrame(picker_card, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=22)

        self.file_label = ctk.CTkLabel(row, text="No file selected", font=theme.font(15), text_color=theme.TEXT_MUTED, anchor="w")
        self.file_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            row, text="📁  Choose CSV File", width=170, height=38, corner_radius=8,
            fg_color=("gray80", "#243356"), hover_color=("gray70", "#2E3F66"),
            text_color=theme.TEXT_PRIMARY, font=theme.font(14, "bold"),
            command=self._choose_file
        ).pack(side="right")

        self.run_button = ctk.CTkButton(
            self, text="Run Validation", height=46, corner_radius=10, state="disabled",
            font=theme.font(14, "bold"), fg_color=theme.BLUE_ACCENT, hover_color=theme.BLUE_ACCENT_HOVER,
            command=self._run_validate
        )
        self.run_button.pack(fill="x", padx=28, pady=(0, 16))

        result_card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        result_card.pack(fill="both", expand=True, padx=28, pady=(0, 28))
        self.result_text = ctk.CTkTextbox(result_card, font=theme.font(14, family="Consolas"), fg_color="transparent")
        self.result_text.pack(fill="both", expand=True, padx=16, pady=16)
        self.result_text.insert("1.0", "Validation results will appear here.")
        self.result_text.configure(state="disabled")

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Select CSV to validate", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        self.selected_path = path
        self.file_label.configure(text=f"📄  {os.path.basename(path)}", text_color=theme.TEXT_PRIMARY)
        self.run_button.configure(state="normal")

    def _run_validate(self):
        result = gui_adapters.run_validate(self.username, self.role, self.selected_path)

        lines = [f"{'✅' if result['success'] else '❌'} {result['message']}"]
        if result["success"] and result["df"] is not None:
            df = result["df"]
            lines.append(f"Rows: {len(df):,}")
            lines.append(f"Columns: {len(df.columns)}")
            lines.append(f"Columns present: {', '.join(df.columns)}")

        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", "\n".join(lines))
        self.result_text.configure(state="disabled")
