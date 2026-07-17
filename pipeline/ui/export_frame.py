import os
import customtkinter as ctk
import gui_adapters
from ui import theme


class ExportFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role

        theme.page_header(
            self, "📤", "Export Customer Data",
            f"Exports over {gui_adapters.EXPORT_THRESHOLD:,} records are flagged as a bulk-export security event."
        )

        card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        card.pack(fill="x", padx=28)
        row = ctk.CTkFrame(card, fg_color="transparent")
        row.pack(fill="x", padx=24, pady=24)

        ctk.CTkLabel(row, text="Number of records", font=theme.font(14, "bold"), text_color=theme.TEXT_MUTED, width=160, anchor="w").pack(side="left")
        self.rows_entry = ctk.CTkEntry(row, placeholder_text="e.g. 1000", height=38, corner_radius=8)
        self.rows_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

        ctk.CTkButton(
            row, text="Export to CSV", width=150, height=38, corner_radius=8,
            fg_color=theme.BLUE_ACCENT, hover_color=theme.BLUE_ACCENT_HOVER,
            font=theme.font(14, "bold"), command=self._run_export
        ).pack(side="right")

        self.result_card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        self.result_card.pack(fill="x", padx=28, pady=(16, 0))
        self.result_inner = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.result_inner.pack(fill="x", padx=24, pady=20)

        self.status_label = ctk.CTkLabel(self.result_inner, text="No export run yet.", font=theme.font(15, "bold"), text_color=theme.TEXT_MUTED, wraplength=700, justify="left")
        self.status_label.pack(anchor="w")

        self.path_label = ctk.CTkLabel(self.result_inner, text="", font=theme.font(14, family="Consolas"), text_color=theme.TEXT_MUTED, wraplength=700, justify="left")
        self.path_label.pack(anchor="w", pady=(4, 0))

        self.warning_label = ctk.CTkLabel(self.result_inner, text="", font=theme.font(14, "bold"), text_color=theme.WARNING, wraplength=700, justify="left")
        self.warning_label.pack(anchor="w", pady=(8, 0))

    def _run_export(self):
        raw = self.rows_entry.get().strip()
        try:
            num_rows = int(raw)
        except ValueError:
            self.status_label.configure(text="🚫 Please enter a valid whole number.", text_color=theme.DANGER)
            self.path_label.configure(text="")
            self.warning_label.configure(text="")
            return

        result = gui_adapters.run_export(self.username, self.role, num_rows)

        if result["success"]:
            self.status_label.configure(text=f"✅ {result['message']}", text_color=theme.SUCCESS)
            abs_path = os.path.abspath(result["file_name"])
            self.path_label.configure(text=f"Saved to: {abs_path}")
        else:
            self.status_label.configure(text=f"🚫 {result['message']}", text_color=theme.DANGER)
            self.path_label.configure(text="")

        self.warning_label.configure(text=f"⚠️  {result.get('warning')}" if result.get("warning") else "")
