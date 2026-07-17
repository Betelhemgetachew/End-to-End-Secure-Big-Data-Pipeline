import customtkinter as ctk
from authorization import PERMISSIONS

PERMISSION_LABELS = {
    "validate": "Validate datasets",
    "import": "Run secure import pipeline",
    "encrypt": "Encrypt sensitive data",
    "verify_hash": "Verify dataset integrity",
    "view_logs": "View audit logs",
    "view_security_events": "View security events",
    "export": "Export customer data",
}


class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, username, role):
        super().__init__(master, fg_color="transparent")

        ctk.CTkLabel(
            self, text=f"Welcome, {username} 👋", font=ctk.CTkFont(size=24, weight="bold")
        ).pack(anchor="w", padx=24, pady=(24, 2))
        ctk.CTkLabel(
            self, text=f"Role: {role}", font=ctk.CTkFont(size=14), text_color="gray60"
        ).pack(anchor="w", padx=24, pady=(0, 24))

        card = ctk.CTkFrame(self, corner_radius=12)
        card.pack(fill="x", padx=24)

        ctk.CTkLabel(
            card, text="Your permissions", font=ctk.CTkFont(size=15, weight="bold")
        ).pack(anchor="w", padx=20, pady=(20, 8))

        role_perms = PERMISSIONS.get(role, [])
        for key, label in PERMISSION_LABELS.items():
            granted = key in role_perms
            row = ctk.CTkFrame(card, fg_color="transparent")
            row.pack(fill="x", padx=20, pady=4)
            icon = "✅" if granted else "—"
            color = "#2ecc71" if granted else "gray50"
            ctk.CTkLabel(row, text=icon, width=24, text_color=color).pack(side="left")
            ctk.CTkLabel(row, text=label, anchor="w", text_color=("black", "white") if granted else "gray50").pack(side="left")

        ctk.CTkLabel(card, text="", height=8).pack()  # bottom padding
