import tkinter as tk
import customtkinter as ctk

from tools.typing_tools import *
from tools.dictionary_tools import add_if_vacant
from tools.tkinter_tools import *
from tools.constants import DefaultTkInitOptions, ToggleState
from tools.logging_tools import *

from custom_tkinter.toggleable_button import ToggleableButton

class BaseFrame(tk.Frame, Loggable):
  def __init__(self, root, parent: tk.Misc, dimensions: Position = (1,1), is_logging_enabled: bool = False, label: Optional[str] = None, include_call_stack: bool = False, **kwargs) -> None:
    self.root = root
    self.parent = parent
    tk.Frame.__init__(self, master=self.parent, **kwargs)
    Loggable.__init__(self, is_logging_enabled=is_logging_enabled, label=label, include_call_stack=include_call_stack)

    self.default_frame = self
    self.dimensions = dimensions

  # widget creation methods

  ## general
  def create_widget[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Optional[Position] = None, container: Optional[tk.Frame] = None, placement_options: Optional[dict[str, Any]] = None, return_widget: bool = False, **kwargs) -> Optional[WidgetType]:
    """Creates a new widget of the type specified, either on a grid or to be packed."""
    if container == None: container = self.default_frame
    init_args = add_if_vacant(kwargs.copy(), DefaultTkInitOptions().WIDGET)
    if issubclass(widget_type, tk.Label):
      init_args = add_if_vacant(init_args, DefaultTkInitOptions().LABEL)
    if issubclass(widget_type, ctk.CTkScrollableFrame): # `CTkScrollableFrame.__init__` takes a different name for defining the border width: this block handles that
      init_args["border_width"] = init_args["borderwidth"]
      del init_args["borderwidth"]
    widget: WidgetType = widget_type(container, **init_args)
    if placement_options == None: placement_options = {}.copy()

    # adding the widget to the container
    if position == None: # using `pack`
      placement_args = add_if_vacant(placement_options, DefaultTkInitOptions().PACK).copy()
      widget.pack(**placement_args)
    else: # using `grid`
      (column, row) = position
      placement_args = add_if_vacant(placement_options, DefaultTkInitOptions().GRID).copy()
      widget.grid(column=column, row=row, **placement_args)
    if return_widget: return widget

  def create_widget_on_grid[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Position, container: Optional[tk.Frame] = None, return_widget: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[WidgetType]:
    """Creates a new widget of the type specified and adds it to a grid."""
    return self.create_widget(widget_type, position=position, container=container, return_widget=return_widget, placement_options=placement_options, **kwargs)
  
  def create_widget_on_self[WidgetType: tk.Widget](self, widget_type: Type[WidgetType], position: Optional[Position] = None, placement_options: Optional[dict[str, Any]] = None, return_widget: bool = False, **kwargs) -> Optional[WidgetType]:
    return self.create_widget(widget_type, position=position, container=self, return_widget=return_widget, placement_options=placement_options, **kwargs)

  ## buttons
  def create_button(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_button: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[tk.Button]:
    """
    Creates a new button widget, either being packed (if `position=None`) or placed on a grid (otherwise).

    :param position: Where the button should be placed on the grid. Defaults to `None`, implying the button will packed instead.
    :type position: Optional[Position]
    :param container: Defaults to `None`, implying \'self.default_frame\' will be used.
    :type container: Optional[Frame]
    :param return_button: Whether the created button object should be returned. Defaults to `False`.
    :type return_button: bool
    :param placement_options: Options passed into the \'Button.grid\' method. Defaults to `{}`, implying that no grid options should be used (besides the defaults).
    :type placement_options: Optional[dict[str, Any]]
    :param kwargs: Keyword arguments. Passed into the initialisation function for the button instance.
    """
    try: kwargs["command"]
    except: kwargs["command"] = lambda: None
    if placement_options == None: placement_options = {}.copy()
    kwargs = add_if_vacant(kwargs, DefaultTkInitOptions().BUTTON).copy()
    return self.create_widget(tk.Button, position=position, container=container, placement_options=placement_options, return_widget=return_button, **kwargs)
  
  def create_toggleable_button(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_button: bool = False, initially_toggled: ToggleState = ToggleState.OFF, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ToggleableButton]:
    """Creates a new toggleable button, either being packed (if `position=None`) or placed on a grid (otherwise)."""
    if container == None: container = self.default_frame
    try: kwargs["command"]
    except: kwargs["command"] = lambda: None
    button: Optional[ToggleableButton] = self.create_widget(ToggleableButton, position=position, container=container, placement_options=placement_options, return_widget=return_button, **kwargs)
    if button == None: return None
    button.is_toggled = initially_toggled
    return button
  
  def create_toggleable_button_on_self(self, position: Optional[Position] = None, return_button: bool = False, initially_toggled: ToggleState = ToggleState.OFF, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ToggleableButton]:
    return self.create_toggleable_button(position=position, container=self, return_button=return_button, initially_toggled=initially_toggled, placement_options=placement_options, **kwargs)
  
  ## frames
  def create_frame(self, position: Optional[Position] = None, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: Optional[dict[str, Any]] = None, **kwargs) -> Optional[tk.Frame]:
    """Creates a new frame, either being packed (if `position=None`) or placed on a grid (otherwise)."""
    kwargs = add_if_vacant(kwargs, DefaultTkInitOptions().FRAME)
    if placement_options == None: placement_options = {}.copy()
    if position == None: placement_options = add_if_vacant(placement_options, DefaultTkInitOptions().FRAME_PACK) # add frame-specific packing options if the frame is being packed
    frame: tk.Frame = unpack_optional(self.create_widget(tk.Frame, position=position, container=container, return_widget=True, placement_options=placement_options, **kwargs)) # as `return_widget` is always `True`, `unpack_optional` will never raise an error
    if dimensions != None:
      configure_grid(frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid)
    if return_frame: return frame

  def create_frame_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Frame]:
    """Creates a new frame and places it to a grid."""
    return self.create_frame(position=position, container=container, return_frame=return_frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid, placement_options=placement_options, **kwargs)
  
  def create_frame_on_root(self, position: Position, return_frame: bool = False, dimensions: Optional[Position] = None, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Frame]:
    return self.create_frame_on_grid(position=position, container=self, return_frame=return_frame, dimensions=dimensions, is_main_grid=True, placement_options=placement_options, **kwargs)

  def create_ctk_scrollable_frame_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_frame: bool = False, dimensions: Optional[Position] = None, exclude_columns: list[int] = [], exclude_rows: list[int] = [], is_main_grid: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[ctk.CTkScrollableFrame]:
    """Creates a new scrollable frame on a grid."""
    kwargs = add_if_vacant(kwargs, DefaultTkInitOptions().CTK_SCROLLABLE_FRAME)
    scrollable_frame = unpack_optional(self.create_widget(ctk.CTkScrollableFrame, position=position, container=container, return_widget=True, placement_options=placement_options, **kwargs))
    if dimensions != None:
      configure_grid(scrollable_frame, dimensions=dimensions, exclude_columns=exclude_columns, exclude_rows=exclude_rows, is_main_grid=is_main_grid)
    if return_frame: return scrollable_frame

  ## other
  def create_scrollbar_on_grid(self, position: Position, container: Optional[tk.Frame] = None, return_scrollbar: bool = False, placement_options: dict[str, Any] = {}, **kwargs) -> Optional[tk.Scrollbar]:
    """Creates a new scrollbar on a grid."""
    scrollbar: Optional[tk.Scrollbar] = self.create_widget(tk.Scrollbar, position=position, container=container, return_widget=return_scrollbar, placement_options=placement_options, **kwargs)
    if scrollbar == None: return
    return scrollbar

  # creating and loading self

  def load(self, **kwargs) -> None: pass
  def create(self, **kwargs) -> None: pass