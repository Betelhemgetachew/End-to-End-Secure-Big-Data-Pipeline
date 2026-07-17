import customtkinter as ctk

from authorization import has_permission
from ui.dashboard_frame import DashboardFrame
from ui.validate_frame import ValidateFrame
from ui.import_frame import ImportFrame
from ui.verify_frame import VerifyFrame
from ui.export_frame import ExportFrame
from ui.grafana_frame import GrafanaFrame
from ui.log_table_frame import LogTableFrame
from ui import theme
import gui_adapters


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, username, role, on_logout):
        super().__init__(master, fg_color=theme.PAGE_BG)
        self.username = username
        self.role = role
        self.on_logout = on_logout

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()

        self.content_container = ctk.CTkFrame(self, fg_color=theme.PAGE_BG, corner_radius=0)
        self.content_container.grid(row=0, column=1, sticky="nsew")
        self.current_frame = None

        self._show("dashboard")

    # -----------------------------------------------------------------
    def _build_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=theme.SIDEBAR_BG)
        sidebar.grid(row=0, column=0, sticky="nsw")
        sidebar.grid_propagate(False)

        # --- Brand ---
        brand = ctk.CTkFrame(sidebar, fg_color="transparent")
        brand.pack(fill="x", padx=20, pady=(26, 18))
        ctk.CTkLabel(brand, text="🛡️", font=theme.font(22)).pack(side="left", padx=(0, 8))
        ctk.CTkLabel(
            brand, text="SecurePipeline", font=theme.font(16, "bold"), text_color="white"
        ).pack(side="left")

        # --- User / role badge ---
        user_card = ctk.CTkFrame(sidebar, fg_color=theme.SIDEBAR_ACTIVE_BG, corner_radius=10)
        user_card.pack(fill="x", padx=16, pady=(0, 20))
        inner = ctk.CTkFrame(user_card, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=10)

        ctk.CTkLabel(
            inner, text=self.username, font=theme.font(15, "bold"), text_color="white", anchor="w"
        ).pack(fill="x")

        badge_bg = theme.ROLE_BADGE_COLORS.get(self.role, ("gray80", "gray30"))
        badge_fg = theme.ROLE_BADGE_TEXT.get(self.role, ("black", "white"))
        badge = ctk.CTkLabel(
            inner, text=f"  {self.role}  ", font=theme.font(14, "bold"),
            fg_color=badge_bg, text_color=badge_fg, corner_radius=6
        )
        badge.pack(anchor="w", pady=(6, 0))

        ctk.CTkFrame(sidebar, fg_color=theme.SIDEBAR_MUTED, height=1).pack(fill="x", padx=16, pady=(0, 12))

        # --- Nav items ---
        # (key, icon, label, required permission or None if always visible)
        nav_items = [
            ("dashboard", "🏠", "Dashboard", None),
            ("validate", "🧪", "Validate Dataset", "validate"),
            ("import", "⬆️", "Import Data", "import"),
            ("verify", "🔍", "Verify Integrity", "verify_hash"),
            ("audit", "📜", "Audit Logs", "view_logs"),
            ("security", "🚨", "Security Events", "view_security_events"),
            ("export", "📤", "Export Data", "export"),
            # Grafana requires the same visibility as security monitoring —
            # Analysts don't get view_logs/view_security_events, so they
            # don't get the monitoring dashboard either.
            ("grafana", "📊", "Monitoring", "view_security_events"),
        ]

        self.nav_buttons = {}
        nav_container = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_container.pack(fill="both", expand=True, padx=12)

        for key, icon, label, permission in nav_items:
            if permission and not has_permission(self.role, permission):
                continue

            btn = ctk.CTkButton(
                nav_container, text=f"{icon}   {label}", anchor="w",
                fg_color="transparent", text_color=theme.SIDEBAR_TEXT,
                hover_color=theme.SIDEBAR_HOVER_BG,
                font=theme.font(15), height=38, corner_radius=8,
                command=lambda k=key: self._show(k)
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[key] = btn

        # --- Logout ---
        ctk.CTkButton(
            sidebar, text="🚪  Log Out", fg_color=theme.DANGER, hover_color="#C0392B",
            font=theme.font(15, "bold"), height=38, corner_radius=8,
            command=self.on_logout
        ).pack(fill="x", padx=16, pady=20, side="bottom")

    # -----------------------------------------------------------------
    def _show(self, key):
        if self.current_frame is not None:
            self.current_frame.destroy()

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=theme.SIDEBAR_ACTIVE_BG, text_color=theme.SIDEBAR_TEXT_ACTIVE)
            else:
                btn.configure(fg_color="transparent", text_color=theme.SIDEBAR_TEXT)

        builders = {
            "dashboard": lambda: DashboardFrame(self.content_container, self.username, self.role),
            "validate": lambda: ValidateFrame(self.content_container, self.username, self.role),
            "import": lambda: ImportFrame(self.content_container, self.username, self.role),
            "verify": lambda: VerifyFrame(self.content_container, self.username, self.role),
            "audit": lambda: LogTableFrame(
                self.content_container, "📜", "Audit Logs",
                "Every login, validation, import, export, and permission check performed in the system.",
                fetch_fn=lambda: gui_adapters.get_audit_logs(self.username, self.role),
            ),
            "security": lambda: LogTableFrame(
                self.content_container, "🚨", "Security Events",
                "Failed operations, warnings, permission denials, integrity failures, and bulk export alerts.",
                fetch_fn=lambda: gui_adapters.get_security_events(self.username, self.role),
            ),
            "export": lambda: ExportFrame(self.content_container, self.username, self.role),
            "grafana": lambda: GrafanaFrame(self.content_container, self.username, self.role),
        }

        self.current_frame = builders[key]()
        self.current_frame.pack(fill="both", expand=True)
