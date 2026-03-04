from typing import Any
from reporting.dataclasses import table_elements as te


class NotebookFieldTableElement(te.StringTableElement):
    def get_value(self, obj: Any) -> Any:
        return obj.data_row.get(self.attr)
