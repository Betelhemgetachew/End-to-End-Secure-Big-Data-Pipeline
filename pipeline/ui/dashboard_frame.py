import customtkinter as ctk
from authorization import PERMISSIONS
from ui import theme

PERMISSION_LABELS = {
    "validate": ("🧪", "Validate datasets"),
    "import": ("⬆️", "Run secure import pipeline"),
    "encrypt": ("🔐", "Encrypt sensitive data"),
    "verify_hash": ("🔍", "Verify dataset integrity"),
    "view_logs": ("📜", "View audit logs"),
    "view_security_events": ("🚨", "View security events"),
    "export": ("📤", "Export customer data"),
}

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")

        theme.page_header(self, "🏠", f"Welcome back, {username}", None)

        badge_bg = theme.ROLE_BADGE_COLORS.get(role, ("gray85", "gray30"))
        badge_fg = theme.ROLE_BADGE_TEXT.get(role, ("black", "white"))
        ctk.CTkLabel(
            self, text=f"  {role} ROLE  ", font=theme.font(14, "bold"),
            fg_color=badge_bg, text_color=badge_fg, corner_radius=8
        ).pack(anchor="w", padx=28, pady=(0, 20))

        card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        card.pack(fill="x", padx=28)

        ctk.CTkLabel(
            card, text="Your permissions", font=theme.font(17, "bold"), text_color=theme.TEXT_PRIMARY
        ).pack(anchor="w", padx=24, pady=(20, 12))

        grid = ctk.CTkFrame(card, fg_color="transparent")
        grid.pack(fill="x", padx=24, pady=(0, 24))
        grid.grid_columnconfigure((0, 1), weight=1, uniform="col")

        role_perms = PERMISSIONS.get(role, [])
        for i, (key, (icon, label)) in enumerate(PERMISSION_LABELS.items()):
            granted = key in role_perms
            self._permission_tile(grid, icon, label, granted).grid(
                row=i // 2, column=i % 2, sticky="ew", padx=6, pady=6
            )

    def _permission_tile(self, parent, icon, label, granted):
        bg = theme.GRANTED_BG if granted else ("gray94", "#1A2540")
        text_color = theme.GRANTED_TEXT if granted else theme.TEXT_MUTED

        tile = ctk.CTkFrame(parent, corner_radius=10, fg_color=bg)
        inner = ctk.CTkFrame(tile, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=14)

        ctk.CTkLabel(inner, text=icon, font=theme.font(18)).pack(side="left", padx=(0, 12))
        ctk.CTkLabel(
            inner, text=label, font=theme.font(14, "bold" if granted else "normal"),
            text_color=text_color, anchor="w", justify="left", wraplength=220
        ).pack(side="left", fill="x", expand=True)

        status = "✅" if granted else "🚫"
        ctk.CTkLabel(inner, text=status, font=theme.font(14)).pack(side="right")

        return tile
