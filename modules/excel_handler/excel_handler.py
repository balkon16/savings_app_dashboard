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

    def _is_entity_supported(self, entity: str) -> None:
        supported_entities = set(self.configuration['entities'].keys())
        if entity not in supported_entities:
            raise NotImplementedError(f"Entity '{entity}' not supported")

    # TODO: testy do metody `get_entity_and_date
    @staticmethod
    def get_entity_and_date(file_name: str, supported_entities: List[str]) -> Tuple[str, datetime.datetime]:
        regex = f"(?P<entity>{'|'.join(supported_entities)})_(?P<date>[0-9]{{8}}).xlsx"
        match = re.search(regex, file_name)
        return match.group("entity"), dt.datetime.strptime(match.group("date"), "%Y%m%d")

    # TODO: testy do metody `read_excel_file_as_dataframe`
    def read_excel_file_as_dataframe(self, file_name: str) -> pd.DataFrame:
        if not Validator.is_excel_file(file_name):
            raise ValueError(f"Not an Excel file: {file_name}")  # TODO: test na wyjątek

        entity = os.path.basename(file_name).split(".")[0]

        # self._is_entity_supported()

        # TODO: sprawdzić rozszerzenie pliku -> jeżeli inne niż xlsx -> wyjątek -> napisać test
        # TODO: sprawdzić entity -> w konfiguracji wypisać te wspierane -> napisać test
        # entity_settings = self.configuration[entity]
        data_file_path = os.path.join(self.configuration['directory'], file_name)
        df = pd.read_excel(data_file_path
                           # , dtype=entity_settings['dtype']
                           ) #TODO: dodać argument dtypes
        df['date'] = ExcelHandler.convert_excel_date_to_date(df['date'])
        return df

    @staticmethod
    def get_dataframe_as_json(dataframe: pd.DataFrame) -> List[Dict[str, Any]]:
        return json.loads(dataframe.to_json(orient="records"))

    @staticmethod
    def convert_excel_date_to_date(column: Series) -> Series:
        return pd.TimedeltaIndex(column, unit="d") + dt.datetime(1900, 1, 1)
