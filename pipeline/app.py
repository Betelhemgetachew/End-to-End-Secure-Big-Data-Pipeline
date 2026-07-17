"""
app.py

Desktop GUI entry point for the End-to-End Secure Big Data Pipeline
(Phase 16 of the project). Run this instead of main.py to use the
CustomTkinter interface. The original CLI (main.py) still works
unchanged -- both share the same backend modules.

    python app.py
"""

import customtkinter as ctk

from ui.login_frame import LoginFrame
from ui.main_frame import MainFrame

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Secure Big Data Pipeline")
        self.geometry("1000x680")
        self.minsize(860, 600)

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.current_screen = None
        self._show_login()

    def _show_login(self):
        self._clear()
        self.current_screen = LoginFrame(self.container, on_success=self._on_login_success)
        self.current_screen.pack(fill="both", expand=True)

    def _on_login_success(self, username, role):
        self._clear()
        self.current_screen = MainFrame(
            self.container, username, role, on_logout=self._show_login
        )
        self.current_screen.pack(fill="both", expand=True)

    def _clear(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None


if __name__ == "__main__":
    app = App()
    app.mainloop()
