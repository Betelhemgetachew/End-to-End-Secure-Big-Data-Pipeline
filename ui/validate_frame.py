import os
import customtkinter as ctk
from tkinter import filedialog

import gui_adapters


class ValidateFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.selected_path = None

        ctk.CTkLabel(
            self, text="Validate Dataset", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(
            self,
            text="Check a CSV for missing values, duplicate emails/account numbers, invalid account types, and negative balances.",
            font=ctk.CTkFont(size=13), text_color="gray60", wraplength=700, justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))

        picker_card = ctk.CTkFrame(self, corner_radius=12)
        picker_card.pack(fill="x", padx=24, pady=(0, 16))
        row = ctk.CTkFrame(picker_card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=20)

        self.file_label = ctk.CTkLabel(row, text="No file selected", text_color="gray60", anchor="w")
        self.file_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(row, text="📁 Choose CSV File", width=160, command=self._choose_file).pack(side="right")

        self.run_button = ctk.CTkButton(
            self, text="Run Validation", height=42, state="disabled",
            font=ctk.CTkFont(size=14, weight="bold"), command=self._run_validate
        )
        self.run_button.pack(fill="x", padx=24, pady=(0, 16))

        self.result_text = ctk.CTkTextbox(self, font=ctk.CTkFont(size=12, family="Courier"))
        self.result_text.pack(fill="both", expand=True, padx=24, pady=(0, 24))
        self.result_text.insert("1.0", "Validation results will appear here.")
        self.result_text.configure(state="disabled")

    def _choose_file(self):
        path = filedialog.askopenfilename(
            title="Select CSV to validate", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return
        self.selected_path = path
        self.file_label.configure(text=os.path.basename(path), text_color=("black", "white"))
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
