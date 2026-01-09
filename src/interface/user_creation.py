import tkinter as tk
from hashlib import sha256

from interface.creation import Creation
from stored.user import User
from game_data import GameData

class UserCreation(Creation):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.entered_user_name = tk.StringVar()
    self.entered_password = tk.StringVar()
    self.re_entered_password = tk.StringVar()
    self.user_creator = kwargs["user_creator"]
    super().__init__(root, parent, game_data, **kwargs)

  def load_users(self) -> None:
    self.users: list[User] = list(self.game_data.users.values())

  def load(self, **kwargs) -> None:
    self.load_users()
  
  def create_user(self, **kwargs) -> None:
    self.load_users()

    user_names: list[str] = [user.name for user in self.users]
    user_name = self.entered_user_name.get()
    password = self.entered_password.get()
    password_hash = sha256(password.encode("utf-8")).hexdigest()
    re_entered_password = self.re_entered_password.get()
    re_entered_password_hash = sha256(re_entered_password.encode("utf-8")).hexdigest()
    if user_name == "":
      self.fail_creation("User name cannot be null")
    elif password == "" or re_entered_password == "":
      self.fail_creation("Password cannot be null")
    elif password_hash != re_entered_password_hash:
      self.fail_creation("Passwords are not the same")
    elif user_name in user_names:
      self.fail_creation("User name already exists")
    else:
      self.user_creator(user_name, password_hash)
    
  def create(self, **kwargs) -> None:
    super().create("Create new user", **kwargs)

    self.create_widget(tk.Label, text="Enter user name:")
    self.create_widget(tk.Entry, textvariable=self.entered_user_name)

    self.create_widget(tk.Label, text="Enter password:")
    self.create_widget(tk.Entry, textvariable=self.entered_password)

    self.create_widget(tk.Label, text="Re-enter password:")
    self.create_widget(tk.Entry, textvariable=self.re_entered_password)

    self.create_message()

    self.create_confirm(self.create_user)
    #self.create_return("user_selection", **kwargs)
    