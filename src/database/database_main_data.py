from tools.typing_tools import *

@dataclass
class DatabaseMainData():
  table_names: list[str]
  version: str

  def to_dict(self) -> dict[str, Any]:
    return {"table_names": self.table_names, "version": self.version}