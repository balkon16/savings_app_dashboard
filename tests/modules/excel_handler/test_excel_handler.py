import datetime
import pandas as pd
import pytest

from modules.excel_handler.excel_handler import ExcelHandler


class TestExcelHandler:

    def test_convert_excel_date_to_date(self):
        input_series = pd.Series([44402, 44400, 43973])
        expected_output = pd.DatetimeIndex(['2021-07-25', '2021-07-23', '2020-05-22'])
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

    def test_get_entity_and_date_w_pass(self):
        input_args = {"file_name": "cheese_20210520.xlsx", "supported_entities": ["apple", "cheese", "banana"]}
        output = ExcelHandler.get_entity_and_date(**input_args)
        expected_output = ("cheese", datetime.datetime(2021, 5, 20, 0, 0, 0))
        assert output == expected_output

    def test_get_entity_and_date_w_error(self):
        input_args = {"file_name": "cheese_20210520.xlsx", "supported_entities": ["apple", "banana"]}
        with pytest.raises(ValueError):
            _ = ExcelHandler.get_entity_and_date(**input_args)

    def test_read_excel_file_as_dataframe_raises(self, get_test_configuration):
        excel_handler = ExcelHandler(configuration=get_test_configuration)
        with pytest.raises(ValueError):
            excel_handler.read_excel_file_as_dataframe("some_file.png")

    def test_read_excel_file_as_dataframe_exchange_rates(self, get_test_configuration):
        excel_handler = ExcelHandler(configuration=get_test_configuration)
        expected_output = pd.DataFrame({
            "Base": ["EUR", "USD"],
            "Quote": ["PLN", "PLN"],
            "Value": [4.5747, 3.8851],
            "Multiplier": [1, 1],
            "Date": ['2001-07-23', '2020-01-31']
        })
        expected_output = expected_output.astype(get_test_configuration['entities']['exchange_rates']['dtype'])
        expected_output['Date'] = pd.to_datetime(expected_output['Date'])

        output = excel_handler.read_excel_file_as_dataframe("exchange_rates_20210725.xlsx")

        assert expected_output.equals(output)

    def test_read_excel_file_as_dataframe_exchange_assets(self, get_test_configuration):
        excel_handler = ExcelHandler(configuration=get_test_configuration)
        expected_output = pd.DataFrame({
            "Ticker": ["TST", "PCC"],
            "Value": [10.01, 100.12],
            "Currency": ["EUR", "USD"],
            "Timestamp": ["2021-07-25 12:21:29", "2021-07-25 12:21:29"],
            "Full name": ["Test Company Ltd.", pd.NA],
            "Stock exchange": ["Wonderland Stock Exchange", pd.NA],
            "Liable party": ["Wonderperson & Co.", pd.NA],
            "Type": ["Stock", pd.NA],
            "Is first insert?": [True, False],
            "Tags": ["wonder, stock", "paper_investment"]
        })
        expected_output = expected_output.astype(get_test_configuration['entities']['assets']['dtype'])
        expected_output['Timestamp'] = pd.to_datetime(expected_output['Timestamp'])

        output = excel_handler.read_excel_file_as_dataframe("assets_20210705.xlsx")

        assert expected_output.equals(output)
