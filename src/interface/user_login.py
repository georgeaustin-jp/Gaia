import tkinter as tk
from hashlib import sha256

from interface.abstract_interface import AbstractInterface
from stored.user import User
from game_data import GameData

class UserLogin(AbstractInterface):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.user: User
    self.user_name_text = tk.StringVar()
    self.password = tk.StringVar()
    self.message = tk.StringVar()
    self.message.set("...")
    super().__init__(root, parent, game_data, **kwargs)

  def login(self) -> None:
    entered_password = self.password.get()
    entered_password_hash = sha256(entered_password.encode("utf-8")).hexdigest()
    password_hash = self.user.password_hash
    if password_hash != entered_password_hash:
      self.fail_user_login("Password is incorrect")
    else:
      self.root.show_screen("character_selection")

  def fail_user_login(self, message: str) -> None:
    self.message.set(message)

  def load(self, **kwargs) -> None:
    try:
      self.user = kwargs["user"]
      self.user_name_text.set(f"User: {self.user.name}")
    except: pass

  def create(self, **kwargs) -> None:
    super().create(**kwargs)
    self.create_widget(tk.Label, textvariable=self.user_name_text)
    self.create_widget(tk.Label, text="Enter password: ")
    self.create_widget(tk.Entry, textvariable=self.password)
    self.create_widget(tk.Label, textvariable=self.message)
    #self.create_widget(tk.Button, text="Return", command = lambda: self.root.show_screen("user_selection"))
    self.create_widget(tk.Button, text="Confirm", command = lambda: self.login())