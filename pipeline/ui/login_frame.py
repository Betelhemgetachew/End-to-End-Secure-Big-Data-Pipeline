import customtkinter as ctk
import gui_adapters
from ui import theme


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master, fg_color=theme.PAGE_BG)
        self.on_success = on_success

        self.grid_columnconfigure(0, weight=5)
        self.grid_columnconfigure(1, weight=6)
        self.grid_rowconfigure(0, weight=1)

        self._build_brand_panel()
        self._build_form_panel()

    # -----------------------------------------------------------------
    def _build_brand_panel(self):
        panel = ctk.CTkFrame(self, fg_color=theme.NAVY_900, corner_radius=0)
        panel.grid(row=0, column=0, sticky="nsew")

        center = ctk.CTkFrame(panel, fg_color="transparent")
        center.place(relx=0.5, rely=0.46, anchor="center")

        ctk.CTkLabel(center, text="🛡️", font=theme.font(56)).pack(pady=(0, 16))
        ctk.CTkLabel(
            center, text="Secure Big Data\nPipeline", justify="center",
            font=theme.font(26, "bold"), text_color="white"
        ).pack()

        # subtle accent line
        ctk.CTkFrame(panel, fg_color=theme.CYAN_ACCENT, width=4, height=90, corner_radius=2).place(
            relx=0.0, rely=0.46, anchor="w"
        )

    # -----------------------------------------------------------------
    def _build_form_panel(self):
        panel = ctk.CTkFrame(self, fg_color=theme.PAGE_BG, corner_radius=0)
        panel.grid(row=0, column=1, sticky="nsew")

        card = ctk.CTkFrame(panel, corner_radius=16, fg_color=theme.CARD_FG, width=360)
        card.place(relx=0.5, rely=0.5, anchor="center")

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(padx=40, pady=40)

        ctk.CTkLabel(
            inner, text="Welcome back", font=theme.heading(20), text_color=theme.TEXT_PRIMARY
        ).pack(anchor="w")
        ctk.CTkLabel(
            inner, text="Sign in to access the pipeline console",
            font=theme.font(14), text_color=theme.TEXT_MUTED
        ).pack(anchor="w", pady=(2, 24))

        ctk.CTkLabel(inner, text="Username", font=theme.font(13, "bold"), text_color=theme.TEXT_MUTED).pack(anchor="w", pady=(0, 4))
        self.username_entry = ctk.CTkEntry(inner, width=280, height=40, corner_radius=8, font=theme.font(14))
        self.username_entry.pack(pady=(0, 16))

        ctk.CTkLabel(inner, text="Password", font=theme.font(13, "bold"), text_color=theme.TEXT_MUTED).pack(anchor="w", pady=(0, 4))
        self.password_entry = ctk.CTkEntry(inner, width=280, height=40, corner_radius=8, show="•", font=theme.font(14))
        self.password_entry.pack(pady=(0, 8))
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())

        self.error_label = ctk.CTkLabel(
            inner, text="", text_color=theme.DANGER, font=theme.font(13), wraplength=280, justify="left"
        )
        self.error_label.pack(anchor="w", pady=(2, 8))

        self.login_button = ctk.CTkButton(
            inner, text="Sign In", width=280, height=42, corner_radius=8,
            fg_color=theme.BLUE_ACCENT, hover_color=theme.BLUE_ACCENT_HOVER,
            font=theme.font(14, "bold"), command=self._attempt_login
        )
        self.login_button.pack(pady=(6, 4))

    # -----------------------------------------------------------------
    def _attempt_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.error_label.configure(text="Please enter both fields")
            return

        self.login_button.configure(state="disabled", text="Signing in...")
        self.update_idletasks()

        success, role, message = gui_adapters.authenticate(username, password)

        self.login_button.configure(state="normal", text="Sign In")

        if success:
            self.error_label.configure(text="")
            self.on_success(username, role)
        else:
            self.error_label.configure(text=message)
            self.password_entry.delete(0, "end")
