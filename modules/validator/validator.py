# TODO: jeżeli będziesz potrzebował bardziej zaawansowanych funkcjonalności sprawdź
#  -> https://pypi.org/project/validator-collection/

class Validator:

    @staticmethod
    def is_valid_currency(curr: str) -> bool:
        return curr.isupper() and len(curr) == 3

    @staticmethod
    def is_excel_file(file_name: str) -> bool:
        return file_name.endswith("xlsx")
