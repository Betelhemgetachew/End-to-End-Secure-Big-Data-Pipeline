import webbrowser
import customtkinter as ctk

# Point this at your actual Grafana dashboard URL (Dashboard > Share > Link)
GRAFANA_URL = "http://localhost:3000"


class GrafanaFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")

        ctk.CTkLabel(
            self, text="Security Monitoring Dashboard", font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 4))
        ctk.CTkLabel(
            self,
            text="Grafana visualizes audit logs and security events pulled directly from PostgreSQL.",
            font=ctk.CTkFont(size=13), text_color="gray60", wraplength=700, justify="left"
        ).pack(anchor="w", padx=24, pady=(0, 20))

        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=24, pady=(0, 16))
        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=24, pady=24, fill="x")

        ctk.CTkLabel(inner, text="📊", font=ctk.CTkFont(size=36)).pack(pady=(0, 8))
        ctk.CTkLabel(
            inner, text="Dashboards refresh automatically, providing near real-time\nmonitoring of pipeline and security activity.",
            font=ctk.CTkFont(size=13), text_color="gray60", justify="center"
        ).pack(pady=(0, 16))

        ctk.CTkButton(
            inner, text="🔗 Open Grafana Dashboard", height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=lambda: webbrowser.open(GRAFANA_URL)
        ).pack()

        ctk.CTkLabel(
            self,
            text=(
                "Note: this opens Grafana in your default browser. For a fully embedded, "
                "in-app panel instead, install `pywebview` and swap the button's command "
                "for an embedded browser widget pointed at this same URL — the rest of the "
                "app doesn't need to change."
            ),
            font=ctk.CTkFont(size=11), text_color="gray50", wraplength=700, justify="left"
        ).pack(anchor="w", padx=24, pady=(8, 24))
