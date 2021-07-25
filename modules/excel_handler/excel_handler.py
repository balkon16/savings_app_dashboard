# TODO: wyjątki -> sprawdź czy można ograniczyć stack trace
#  (https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st)

import os
import typing
import pandas as pd
import datetime as dt
from pandas.core.series import Series


class ExcelHandler:

    def __init__(self, configuration: typing.Dict[str, typing.Any]) -> None:
        self.configuration = configuration

    def read_excel_file_as_dataframe(self, file_name: str, entity: str) -> pd.DataFrame:
        # TODO: sprawdzić rozszerzenie pliku -> jeżeli inne niż xlsx -> wyjątek
        # TODO: sprawdzić entity -> w konfiguracji wypisać te wspierane
        entity_settings = self.configuration[entity]
        data_file_path = os.path.join(self.configuration['directory'], file_name)
        df = pd.read_excel(data_file_path, dtype=entity_settings['dtype'])
        df['date'] = ExcelHandler.convert_excel_date_to_date(df['date'])
        return df

    @staticmethod
    def convert_excel_date_to_date(column: Series) -> Series:
        return pd.TimedeltaIndex(column, unit="d") + dt.datetime(1900, 1, 1)
