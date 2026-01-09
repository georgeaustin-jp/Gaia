import tkinter as tk

from tools.constants import ScreenName

from interface.selection import Selection
from stored.user import User
from game_data import GameData

class UserSelection(Selection):
  def __init__(self, root, parent: tk.Frame, game_data: GameData, **kwargs) -> None:
    self.existing_user_buttons: list[str] = []
    super().__init__(root, parent, game_data, **kwargs)
    self.load(**kwargs)

  def load(self, **kwargs) -> None:
    users: list[User] = list(self.game_data.users.values())
    for user in users: # loads buttons for new users
      user_name: str = user.name
      if not user_name in self.existing_user_buttons:
        command = lambda user_instance: self.root.show_screen(screen_name=ScreenName.USER_LOGIN, user=user_instance)
        self.create_widget(tk.Button, text=user_name, command=command(user))
        self.existing_user_buttons.append(user_name)

    widgets: list = self.winfo_children()
    special_button_texts = ["Create user", "Quit"]
    buttons: list = list(filter(lambda widget: (type(widget) == tk.Button) and (not widget["text"] in special_button_texts), widgets))

    user_names: list = [user.name for user in users]
    for (index, button) in enumerate(buttons): # removes buttons for deleted users
      button_name: str = button["text"]
      if not button_name in user_names:
        buttons[index].destroy()
        self.users =list(filter(lambda user: user.name != button_name, users))

  def create(self, **kwargs) -> None:
    super().create(title="User selection", dimensions=(1,1), **kwargs)
    #self.create_widget(tk.Button, text="Create user", command = lambda: self.root.show_screen("user_creation"))
    #self.create_widget(tk.Button, text="Quit", command = lambda: kwargs["quit_command"]())