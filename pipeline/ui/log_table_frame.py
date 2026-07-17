import customtkinter as ctk
from ui import theme


class LogTableFrame(ctk.CTkFrame):
    """
    Generic read-only table for rows shaped like:
    (log_id, username, action, status, log_time)
    """

    STATUS_COLORS = {
        "SUCCESS": theme.SUCCESS,
        "FAILED": theme.DANGER,
        "WARNING": theme.WARNING,
    }

    def __init__(self, master, icon, title, subtitle, fetch_fn, empty_message="No entries yet."):
        super().__init__(master, fg_color="transparent")
        self.fetch_fn = fetch_fn
        self.empty_message = empty_message

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=28, pady=(28, 4))
        title_row = ctk.CTkFrame(header, fg_color="transparent")
        title_row.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_row, text=icon, font=theme.font(24)).pack(side="left", padx=(0, 10))
        ctk.CTkLabel(title_row, text=title, font=theme.heading(22), text_color=theme.TEXT_PRIMARY).pack(side="left")

        ctk.CTkButton(
            header, text="⟳  Refresh", width=110, height=34, corner_radius=8,
            fg_color=("gray80", "#243356"), hover_color=("gray70", "#2E3F66"),
            text_color=theme.TEXT_PRIMARY, font=theme.font(14, "bold"), command=self.refresh
        ).pack(side="right")

        ctk.CTkLabel(
            self, text=subtitle, font=theme.font(15), text_color=theme.TEXT_MUTED,
            wraplength=760, justify="left"
        ).pack(anchor="w", padx=28, pady=(4, 16))

        table_card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        table_card.pack(fill="both", expand=True, padx=28, pady=(0, 28))

        self.scroll = ctk.CTkScrollableFrame(table_card, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=16, pady=16)

        col_widths = (55, 130, 300, 100, 170)
        headers = ("ID", "Username", "Action", "Status", "Time")
        header_row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 8))
        for text, w in zip(headers, col_widths):
            ctk.CTkLabel(
                header_row, text=text, width=w, anchor="w",
                font=theme.font(15, "bold"), text_color=theme.TEXT_MUTED
            ).pack(side="left", padx=4)

        ctk.CTkFrame(self.scroll, fg_color=("gray85", "#243356"), height=1).pack(fill="x", pady=(0, 6))

        self.col_widths = col_widths
        self.rows_container = ctk.CTkFrame(self.scroll, fg_color="transparent")
        self.rows_container.pack(fill="both", expand=True)

        self.refresh()

    def refresh(self):
        for widget in self.rows_container.winfo_children():
            widget.destroy()

        rows = self.fetch_fn()

        if rows is None:
            ctk.CTkLabel(
                self.rows_container, text="🚫 You are not authorized to view this.",
                text_color=theme.DANGER, font=theme.font(14, "bold")
            ).pack(anchor="w", pady=12)
            return

        if not rows:
            ctk.CTkLabel(
                self.rows_container, text=self.empty_message, text_color=theme.TEXT_MUTED
            ).pack(anchor="w", pady=12)
            return

        for i, row in enumerate(rows):
            log_id, username, action, status, log_time = row
            row_bg = ("gray96", "#1A2540") if i % 2 == 0 else "transparent"
            row_frame = ctk.CTkFrame(self.rows_container, fg_color=row_bg, corner_radius=6)
            row_frame.pack(fill="x", pady=1)

            values = (str(log_id), username, action, status, str(log_time))
            for j, (value, w) in enumerate(zip(values, self.col_widths)):
                color = self.STATUS_COLORS.get(status) if j == 3 else theme.TEXT_PRIMARY
                weight = "bold" if j == 3 else "normal"
                ctk.CTkLabel(
                    row_frame, text=value, width=w, anchor="w",
                    text_color=color, font=theme.font(14, weight)
                ).pack(side="left", padx=4, pady=6)
