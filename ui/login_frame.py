import customtkinter as ctk
import gui_adapters


class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, on_success):
        super().__init__(master, fg_color="transparent")
        self.on_success = on_success

        card = ctk.CTkFrame(self, corner_radius=16, width=380, height=400)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.pack_propagate(False)

        ctk.CTkLabel(card, text="🔒", font=ctk.CTkFont(size=40)).pack(pady=(36, 4))
        ctk.CTkLabel(
            card, text="Secure Big Data Pipeline",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(0, 2))
        ctk.CTkLabel(
            card, text="Sign in to continue",
            font=ctk.CTkFont(size=12), text_color="gray60"
        ).pack(pady=(0, 24))

        self.username_entry = ctk.CTkEntry(card, placeholder_text="Username", width=280, height=38)
        self.username_entry.pack(pady=(0, 12))

        self.password_entry = ctk.CTkEntry(card, placeholder_text="Password", show="•", width=280, height=38)
        self.password_entry.pack(pady=(0, 8))
        self.password_entry.bind("<Return>", lambda e: self._attempt_login())

        self.error_label = ctk.CTkLabel(card, text="", text_color="#e74c3c", font=ctk.CTkFont(size=12), wraplength=280)
        self.error_label.pack(pady=(4, 8))

        self.login_button = ctk.CTkButton(card, text="Sign In", width=280, height=38, command=self._attempt_login)
        self.login_button.pack(pady=(4, 0))

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
