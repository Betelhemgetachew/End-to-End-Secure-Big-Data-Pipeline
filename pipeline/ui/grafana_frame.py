import webbrowser
import customtkinter as ctk
from ui import theme

# Point this at your actual Grafana dashboard URL (Dashboard > Share > Link)
GRAFANA_URL = "http://localhost:3000"


class GrafanaFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")

        theme.page_header(
            self, "📊", "Security Monitoring",
            "Grafana visualizes audit logs and security events pulled directly from PostgreSQL, "
            "refreshing automatically for near real-time visibility."
        )

        card = ctk.CTkFrame(self, corner_radius=14, fg_color=theme.CARD_FG)
        card.pack(fill="x", padx=28)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=32, pady=36, fill="x")

        ctk.CTkLabel(inner, text="📊", font=theme.font(40)).pack(pady=(0, 10))
        ctk.CTkLabel(
            inner, text="Live Pipeline Dashboard",
            font=theme.font(16, "bold"), text_color=theme.TEXT_PRIMARY
        ).pack()
        ctk.CTkLabel(
            inner, text="Includes logins, imports, integrity checks, warnings, and bulk export alerts",
            font=theme.font(14), text_color=theme.TEXT_MUTED
        ).pack(pady=(2, 20))

        ctk.CTkButton(
            inner, text="🔗  Open Grafana Dashboard", height=44, width=260,
            font=theme.font(15, "bold"), corner_radius=8,
            fg_color=theme.BLUE_ACCENT, hover_color=theme.BLUE_ACCENT_HOVER,
            command=lambda: webbrowser.open(GRAFANA_URL)
        ).pack()
