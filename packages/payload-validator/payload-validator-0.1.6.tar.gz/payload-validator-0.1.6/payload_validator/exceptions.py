from typing import (
    Dict,
    Iterable,
    Union,
)


class ValidationException(Exception):
    def __init__(self):
        super().__init__(self, "Validation failed")


class ValidationNotRunException(Exception):
    pass


class MismatchedErrorKeysException(Exception):
    pass


class InvalidValueError(Exception):
    def __init__(self, error_value_by_key: Dict[str, Union[str, Iterable]], add_skip_validation_keys: list = None):
        if add_skip_validation_keys is None:
            add_skip_validation_keys = []
        result = [key for key in add_skip_validation_keys if key not in error_value_by_key.keys()]
        if result:
            raise MismatchedErrorKeysException(
                "In add_skip_validation_keys {} not in error_value_by_key".format(', '.join(result))
            )
        self.error_value_by_key = error_value_by_key
        self.add_skip_validation_keys = add_skip_validation_keys
