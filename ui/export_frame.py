import customtkinter as ctk

import gui_adapters


class ExportFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role

        ctk.CTkLabel(
            self, text="Export Customer Data", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(
            self,
            text=f"Exports over {gui_adapters.EXPORT_THRESHOLD:,} records are flagged as a security event (bulk export monitoring).",
            font=ctk.CTkFont(size=13), text_color="gray60", wraplength=700, justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))

        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=24, pady=(0, 16))
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=20, pady=20)

        ctk.CTkLabel(row, text="Number of records:", width=160, anchor="w").pack(side="left")
        self.rows_entry = ctk.CTkEntry(row, placeholder_text="e.g. 1000")
        self.rows_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ctk.CTkButton(row, text="Export to CSV", width=140, command=self._run_export).pack(side="right")

        self.result_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14, weight="bold"), wraplength=700)
        self.result_label.pack(anchor="w", padx=24)

        self.warning_label = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13), text_color="#f39c12", wraplength=700)
        self.warning_label.pack(anchor="w", padx=24, pady=(4, 0))

    def _run_export(self):
        raw = self.rows_entry.get().strip()
        try:
            num_rows = int(raw)
        except ValueError:
            self.result_label.configure(text="🚫 Please enter a valid whole number.", text_color="#e74c3c")
            return

        result = gui_adapters.run_export(self.username, self.role, num_rows)

        if result["success"]:
            self.result_label.configure(text=f"✅ {result['message']}", text_color="#2ecc71")
        else:
            self.result_label.configure(text=f"🚫 {result['message']}", text_color="#e74c3c")

        self.warning_label.configure(text=f"⚠️ {result.get('warning')}" if result.get("warning") else "")
