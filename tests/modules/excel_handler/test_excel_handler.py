import pandas as pd

from modules.excel_handler.excel_handler import ExcelHandler


class TestExcelHandler:

    def test_convert_excel_date_to_date(self):
        input_series = pd.Series([44400, 44399, 43607, 38046, 44920])
        expected_output = pd.DatetimeIndex(['2021-07-25', '2021-07-24', '2019-05-24', '2004-03-02', '2022-12-27'])
        output_series = ExcelHandler.convert_excel_date_to_datetime(input_series)
        assert expected_output.equals(output_series)
