import numpy as np
from trajectopy.gui.models.entry import PropertyEntry
from trajectopy.gui.models.table_model import RequestTableModel
from trajectopy.gui.requests.property_request import PropertyModelRequest, PropertyModelRequestType
import pandas as pd


class PropertyTableModel(RequestTableModel):
    def __init__(self, num_cols: int = 2):
        REQUEST_MAPPING = {
            PropertyModelRequestType.EXPORT: self.export,
        }

        header_list = ["Name"]
        header_list.extend(["Value"] * (num_cols - 1))
        super().__init__(
            headers=header_list,
            REQUEST_MAPPING=REQUEST_MAPPING,
        )
        self.items: list[PropertyEntry] = []

    def get_request(self) -> PropertyModelRequest:
        return super().get_request()

    def export(self) -> None:
        columns = [item.name for item in self.items]
        data = np.array([list(item.values) for item in self.items]).T
        dataframe = pd.DataFrame(data=data, columns=columns)
        dataframe.to_csv(self.get_request().file, index=False, sep=",", float_format="%.6f")
