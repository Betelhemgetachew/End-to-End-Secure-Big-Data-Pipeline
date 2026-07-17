import customtkinter as ctk


class LogTableFrame(ctk.CTkFrame):
    """
    Generic read-only table for rows shaped like:
    (log_id, username, action, status, log_time)
    """

    STATUS_COLORS = {
        "SUCCESS": "#2ecc71",
        "FAILED": "#e74c3c",
        "WARNING": "#f39c12",
    }

    def __init__(self, master, title, subtitle, fetch_fn, empty_message="No entries yet."):
        super().__init__(master, fg_color="transparent")
        self.fetch_fn = fetch_fn
        self.empty_message = empty_message

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=24, pady=(24, 4))

        ctk.CTkLabel(header, text=title, font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="⟳ Refresh", width=100, command=self.refresh).pack(side="right")

        ctk.CTkLabel(
            self, text=subtitle, font=ctk.CTkFont(size=13), text_color="gray60"
        ).pack(anchor="w", padx=24, pady=(0, 16))

        self.scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # column headers
        col_widths = (60, 140, 320, 110, 180)
        headers = ("ID", "Username", "Action", "Status", "Time")
        header_row = ctk.CTkFrame(self.scroll, fg_color="transparent")
        header_row.pack(fill="x", pady=(0, 4))
        for text, w in zip(headers, col_widths):
            ctk.CTkLabel(
                header_row, text=text, width=w, anchor="w",
                font=ctk.CTkFont(size=12, weight="bold"), text_color="gray50"
            ).pack(side="left", padx=4)

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
                text_color="#e74c3c"
            ).pack(anchor="w", pady=12)
            return

        if not rows:
            ctk.CTkLabel(
                self.rows_container, text=self.empty_message, text_color="gray60"
            ).pack(anchor="w", pady=12)
            return

        for row in rows:
            log_id, username, action, status, log_time = row
            row_frame = ctk.CTkFrame(self.rows_container, fg_color="transparent")
            row_frame.pack(fill="x", pady=2)

            values = (str(log_id), username, action, status, str(log_time))
            for i, (value, w) in enumerate(zip(values, self.col_widths)):
                color = self.STATUS_COLORS.get(status) if i == 3 else None
                ctk.CTkLabel(
                    row_frame, text=value, width=w, anchor="w",
                    text_color=color, font=ctk.CTkFont(size=12)
                ).pack(side="left", padx=4)
