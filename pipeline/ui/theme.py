"""
ui/theme.py

Central design tokens so every screen shares one consistent look.
Colors are (light_mode, dark_mode) tuples, as CustomTkinter expects.
"""

import customtkinter as ctk

# --- Brand palette: deep navy + cyan accent (security / data theme) ---
NAVY_900 = "#0B1120"
NAVY_800 = "#111A2E"
NAVY_700 = "#1A2540"
NAVY_600 = "#243356"

CYAN_ACCENT = "#22D3EE"
CYAN_ACCENT_HOVER = "#0FB8D4"
BLUE_ACCENT = "#3B82F6"
BLUE_ACCENT_HOVER = "#2563EB"

SUCCESS = "#22C55E"
WARNING = "#F59E0B"
DANGER = "#EF4444"

TEXT_MUTED = ("#64748B", "#8B9BB4")
TEXT_PRIMARY = ("#0F172A", "#E7ECF5")

# Sidebar (always dark, regardless of app appearance mode — like most
# security/admin tools)
SIDEBAR_BG = NAVY_900
SIDEBAR_ACTIVE_BG = NAVY_700
SIDEBAR_HOVER_BG = NAVY_800
SIDEBAR_TEXT = "#CBD5E1"
SIDEBAR_TEXT_ACTIVE = "#FFFFFF"
SIDEBAR_MUTED = "#5B6B8C"

# Card / surface backgrounds
CARD_FG = ("gray95", "#161F33")
PAGE_BG = ("gray92", "#0E1526")

# Used for "granted" states (e.g. permission tiles) instead of green
GRANTED_BG = ("#E3EAF7", "#101B33")
GRANTED_TEXT = ("#1E3A6E", "#9DC0F5")

ROLE_BADGE_COLORS = {
    "ADMIN": ("#DBEAFE", "#1E3A5F"),
    "ANALYST": ("#DCFCE7", "#1E3F2B"),
    "AUDITOR": ("#FEF3C7", "#4A3A12"),
}
ROLE_BADGE_TEXT = {
    "ADMIN": ("#1D4ED8", "#93C5FD"),
    "ANALYST": ("#15803D", "#86EFAC"),
    "AUDITOR": ("#B45309", "#FCD34D"),
}


def font(size=14, weight="normal", family="Segoe UI"):
    return ctk.CTkFont(family=family, size=size, weight=weight)


def heading(size=22):
    return font(size=size, weight="bold")


def page_header(parent, icon, title, subtitle):
    """Consistent header block used at the top of every content screen."""
    header = ctk.CTkFrame(parent, fg_color="transparent")
    header.pack(fill="x", padx=28, pady=(28, 4))

    title_row = ctk.CTkFrame(header, fg_color="transparent")
    title_row.pack(fill="x")

    ctk.CTkLabel(title_row, text=icon, font=font(24)).pack(side="left", padx=(0, 10))
    ctk.CTkLabel(title_row, text=title, font=heading(22), text_color=TEXT_PRIMARY).pack(side="left")

    if subtitle:
        ctk.CTkLabel(
            parent, text=subtitle, font=font(14), text_color=TEXT_MUTED,
            wraplength=760, justify="left"
        ).pack(anchor="w", padx=28, pady=(4, 20))
    else:
        ctk.CTkFrame(parent, fg_color="transparent", height=12).pack()

    return header
