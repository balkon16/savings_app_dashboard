from modules.validator.validator import Validator


class TestValidator:

    def test_is_valid_currency(self):
        valid_curr = "EUR"
        invalid_curr = "polski złoty"
        assert (Validator.is_valid_currency(valid_curr) is True) \
            and (Validator.is_valid_currency(invalid_curr) is False)