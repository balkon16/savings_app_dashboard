# TODO: wyjątki -> sprawdź czy można ograniczyć stack trace
#  (https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st)
import datetime
import json
import os
import re
from typing import Dict, List, Any, Tuple, Set
import pandas as pd
import datetime as dt
from pandas.core.series import Series

from modules.validator.validator import Validator


class ExcelHandler:

    def __init__(self, configuration: Dict[str, Any]) -> None:
        self.configuration = configuration

    @staticmethod
    def get_entity_and_date(file_name: str, supported_entities: List[str]) -> Tuple[str, datetime.datetime]:
        regex = f"(?P<entity>{'|'.join(supported_entities)})_(?P<date>[0-9]{{8}}).xlsx"
        match = re.search(regex, file_name)
        if not match:
            raise ValueError(f"{file_name} contains an unsupported entity.")
        return match.group("entity"), dt.datetime.strptime(match.group("date"), "%Y%m%d")

    def read_excel_file_as_dataframe(self, file_name: str) -> pd.DataFrame:
        if not Validator.is_excel_file(file_name):
            raise ValueError(f"Not an Excel file: {file_name}")

        entity, date_obj = ExcelHandler.get_entity_and_date(file_name, self.configuration['entities'].keys())
        entity_settings = self.configuration['entities'][entity]

        data_file_path = os.path.join(self.configuration['directory'], file_name)

        df = pd.read_excel(data_file_path, dtype=entity_settings['dtype'])

        # convert Excel dates such as 44402 to 2021-07-25
        date_columns = entity_settings.get("date_columns") or []
        for date_column in date_columns:
            df[date_column] = ExcelHandler.convert_excel_date_to_date(df[date_column])

        return df

    @staticmethod
    def get_dataframe_as_json(dataframe: pd.DataFrame) -> List[Dict[str, Any]]:
        return json.loads(dataframe.to_json(orient="records"))

    @staticmethod
    def convert_excel_date_to_date(column: Series) -> Series:
        return pd.TimedeltaIndex(column, unit="d") + dt.datetime(1899, 12, 30)
