import pandas as pd

from modules.excel_handler.excel_handler import ExcelHandler


class TestExcelHandler:

    def test_convert_excel_date_to_date(self):
        input_series = pd.Series([44400, 44399, 43607, 38046, 44920])
        expected_output = pd.DatetimeIndex(['2021-07-25', '2021-07-24', '2019-05-24', '2004-03-02', '2022-12-27'])
        output_series = ExcelHandler.convert_excel_date_to_date(input_series)
        assert expected_output.equals(output_series)

    def test_get_dataframe_as_json(self):
        input_df = pd.DataFrame(data={
            "int_column": [1, 2, 3],
            "text_column": ["środa", "text", "😁"],
            "number_column": [float(4.1), float(-1.01), float(0.0)],
            "date_column": pd.Series(['2021-07-25', '2021-07-24', "2021-07-23"], dtype='datetime64[ns]')
        })
        expected_output = [
            {"int_column": 1, "text_column": "środa", "number_column": 4.1, "date_column": 1627171200000},
            {"int_column": 2, "text_column": "text", "number_column": -1.01, "date_column": 1627084800000},
            {"int_column": 3, "text_column": "😁", "number_column": 0.0, "date_column": 1626998400000}
        ]
        output_json = ExcelHandler.get_dataframe_as_json(input_df)
        assert expected_output == output_json
