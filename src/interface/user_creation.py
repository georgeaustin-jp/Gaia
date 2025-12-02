import tkinter as tk
from hashlib import sha256

from interface.abstract_frame import AbstractFrame

class UserCreation(AbstractFrame):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    self.entered_user_name = tk.StringVar()
    self.entered_password = tk.StringVar()
    self.re_entered_password = tk.StringVar()
    self.entry_information = tk.StringVar()
    self.entry_information.set("...")
    super().__init__(root, parent, **kwargs)
    self.load(**kwargs)

  def load(self, **kwargs) -> None:
    self.users: list = kwargs["users"]
  
  def create_user(self) -> None:
    user_name = self.entered_user_name.get()
    password = self.entered_password.get()
    password_hash = sha256(password.encode("utf-8"))
    re_entered_password = self.re_entered_password.get()
    re_entered_password_hash = sha256(re_entered_password.encode("utf-8"))
    if user_name == "":
      self.fail_creation("User name cannot be null")
    elif password == "" or re_entered_password == "":
      self.fail_creation("Password cannot be null")
    elif password_hash != re_entered_password_hash:
      self.fail_creation("Passwords are not the same")
  
  def fail_creation(self, message: str) -> None:
    self.entry_information.set(message)
    
  def create(self, **kwargs) -> None:
    super().create("Create new user", **kwargs)

    self.create_widget(tk.Label, text="Enter user name:")
    self.create_widget(tk.Entry, textvariable=self.entered_user_name)

    self.create_widget(tk.Label, text="Enter password:")
    self.create_widget(tk.Entry, textvariable=self.entered_password)

    self.create_widget(tk.Label, text="Re-enter password:")
    self.create_widget(tk.Entry, textvariable=self.re_entered_password)

    self.create_widget(tk.Label, textvariable=self.entry_information)

    self.create_widget(tk.Button, text="Return", command = lambda: self.root.show_screen("user_selection"))
    self.create_widget(tk.Button, text="Confirm",command = lambda: self.create_user())
    