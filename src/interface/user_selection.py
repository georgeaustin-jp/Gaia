import tkinter as tk

from interface.selection import Selection
from user import User

class UserSelection(Selection):
  def __init__(self, root, parent: tk.Frame, **kwargs) -> None:
    self.existing_user_buttons: list[str] = []
    super().__init__(root, parent, **kwargs)
    self.load(**kwargs)

  def load(self, **kwargs) -> None:
    print(kwargs)
    users: list[User] = kwargs["users"]
    print(f"UserSelection.load(): users=`{users}`")
    for user in users: # loads buttons for new users
      user_name: str = user.name
      if not user_name in self.existing_user_buttons:
        self.create_widget(tk.Button, text=user_name, command=lambda: self.root.show_screen("user_login", user=user))
        self.existing_user_buttons.append(user_name)

    widgets: list[tk.Widget] = self.winfo_children()
    print(f"UserSelection.load() widgets=`{widgets}`")
    buttons: list[tk.Widget] = list(filter(lambda widget: type(widget) == tk.Button and widget["text"] != "Create user", widgets))

    user_names: list = [user.name for user in users]
    for (index, button) in enumerate(buttons): # deletes buttons for deleted users
      button_name: str = button["text"]
      print(f"UserSelection.load(): button_name=`{button_name}`")
      if not button_name in user_names:
        print(f"UserSelection.load(): destroyed")
        buttons[index].destroy()

  def create(self, **kwargs) -> None:
    super().create("User selection", **kwargs)
    self.create_widget(tk.Button, text="Create user", command = lambda: self.root.show_screen("user_creation"))