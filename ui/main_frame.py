import customtkinter as ctk

from authorization import has_permission
from ui.dashboard_frame import DashboardFrame
from ui.validate_frame import ValidateFrame
from ui.import_frame import ImportFrame
from ui.verify_frame import VerifyFrame
from ui.export_frame import ExportFrame
from ui.grafana_frame import GrafanaFrame
from ui.log_table_frame import LogTableFrame
import gui_adapters


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, username, role, on_logout):
        super().__init__(master, fg_color="transparent")
        self.username = username
        self.role = role
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self.content_container = ctk.CTkFrame(self, fg_color="transparent")
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.current_frame = None

        self._show("dashboard")

    # -----------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(
            sidebar, text="🔒 Secure Pipeline", font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=20, pady=(24, 4))
        ctk.CTkLabel(
            sidebar, text=f"{self.username} · {self.role}",
            font=ctk.CTkFont(size=11), text_color="gray60"
        ).pack(anchor="w", padx=20, pady=(0, 24))

        nav_items = [
            ("dashboard", "🏠  Dashboard", None),
            ("validate", "🧪  Validate Dataset", "validate"),
            ("import", "⬆️  Import Data", "import"),
            ("verify", "🔍  Verify Integrity", "verify_hash"),
            ("audit", "📜  Audit Logs", "view_logs"),
            ("security", "🚨  Security Events", "view_security_events"),
            ("export", "📤  Export Data", "export"),
            ("grafana", "📊  Monitoring", None),
        ]

        self.nav_buttons = {}
        for key, label, permission in nav_items:
            if permission and not has_permission(self.role, permission):
                continue
            btn = ctk.CTkButton(
                sidebar, text=label, anchor="w", fg_color="transparent",
                text_color=("black", "white"), hover_color=("gray85", "gray25"),
                command=lambda k=key: self._show(k)
            )
            btn.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = btn

        ctk.CTkFrame(sidebar, fg_color="transparent", height=1).pack(fill="x", expand=True)

        ctk.CTkButton(
            sidebar, text="🚪  Log Out", fg_color="#e74c3c", hover_color="#c0392b",
            command=self.on_logout
        ).pack(fill="x", padx=12, pady=20, side="bottom")

    # -----------------------------------------------------------------
    def _show(self, key):
        if self.current_frame is not None:
            self.current_frame.destroy()

        for k, btn in self.nav_buttons.items():
            btn.configure(fg_color=("gray80", "gray30") if k == key else "transparent")

        builders = {
            "dashboard": lambda: DashboardFrame(self.content_container, self.username, self.role),
            "validate": lambda: ValidateFrame(self.content_container, self.username, self.role),
            "import": lambda: ImportFrame(self.content_container, self.username, self.role),
            "verify": lambda: VerifyFrame(self.content_container, self.username, self.role),
            "audit": lambda: LogTableFrame(
                self.content_container, "Audit Logs",
                "Every login, validation, import, export, and permission check performed in the system.",
                fetch_fn=lambda: gui_adapters.get_audit_logs(self.username, self.role),
            ),
            "security": lambda: LogTableFrame(
                self.content_container, "Security Events",
                "Failed operations, warnings, permission denials, integrity failures, and bulk export alerts.",
                fetch_fn=lambda: gui_adapters.get_security_events(self.username, self.role),
            ),
            "export": lambda: ExportFrame(self.content_container, self.username, self.role),
            "grafana": lambda: GrafanaFrame(self.content_container, self.username, self.role),
        }

        self.current_frame = builders[key]()
        self.current_frame.pack(fill="both", expand=True)
