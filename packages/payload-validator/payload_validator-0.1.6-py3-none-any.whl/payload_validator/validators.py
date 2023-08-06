from abc import (
    ABC,
    abstractmethod,
)
from types import FunctionType
from typing import (
    Callable,
    Iterable,
    Optional,
    TypeVar,
    Union,
)

from payload_validator.exceptions import (
    InvalidValueError,
    ValidationException,
    ValidationNotRunException,
)


T = TypeVar("T")  # Use TypeVar for arbitrary object types


class ValidatorErrorContext(ABC, dict):
    @abstractmethod
    def add_error(self, field: str, error: str):
        pass


class NormalValidatorErrorContext(ValidatorErrorContext):
    def add_error(self, field: str, error: str):
        value = self.setdefault(field, [])
        value.append(error)


class PayloadValidator(object):
    DEFAULT_MANDATORY_ERROR_MESSAGE = "mandatory data missing"

    def __init__(self, payload: dict, error_context: ValidatorErrorContext = None) -> None:
        self.payload = payload
        self._skip_validate_keys = set()
        self._validate_called = False
        self._error_context = (
            error_context
            if error_context is not None
            else NormalValidatorErrorContext()
        )

        self.mandatory_keys = getattr(self._get_meta_attribute(), "mandatory_keys", {})
        self.type_of_keys = getattr(self._get_meta_attribute(), "type_of_keys", {})

    def add_error_context(self, key: str, errors: Union[str, Iterable]) -> None:
        if key not in self._skip_validate_keys:
            if isinstance(errors, str):
                self._error_context.add_error(key, errors)
            else:
                for error in errors:
                    self._error_context.add_error(key, error)

    def add_error_and_skip_validation_key(self, key: str, errors: Union[str, Iterable]) -> None:
        """
        add only main error so other errors cannot add
        """
        self.add_error_context(key, errors)
        self._skip_validate_keys.add(key)

    def _get_meta_attribute(self) -> Optional[T]:
        return getattr(self, "Meta", None)

    def _validate_mandatory_payloads(self) -> None:
        """
        mandatory_keys example:
        {
            "displayable": "displayable is required",  # if error message is not provided, default message will be used
        }
        """
        for key, error_message in self.mandatory_keys.items():
            if self.payload.get(key) is None:
                self.add_error_and_skip_validation_key(key, error_message or self.DEFAULT_MANDATORY_ERROR_MESSAGE)

    def _validate_payloads_type(self) -> None:
        for key, value in self.type_of_keys.items():
            type_or_funcs, error_msg = value

            if not isinstance(type_or_funcs, Iterable):
                type_or_funcs = [type_or_funcs]

            if not self._is_payload_type_valid(key, type_or_funcs):
                self.add_error_and_skip_validation_key(key, error_msg)

    def _is_payload_type_valid(self, key: str, type_or_funcs: Union[Iterable, Callable]) -> bool:
        payload_value = self.payload.get(key)

        for type_or_func in type_or_funcs:
            if isinstance(type_or_func, FunctionType):
                if type_or_func(payload_value):
                    return True
            elif isinstance(payload_value, type_or_func):
                return True
        return False

    def _common_validate(self) -> None:
        try:
            self.common_validate()
        except InvalidValueError as e:
            for key, value in e.error_value_by_key.items():
                if key in e.add_skip_validation_keys:
                    self.add_error_and_skip_validation_key(key, value)
                else:
                    self.add_error_context(key, value)

    def common_validate(self) -> None:
        """
        override this method to add custom validation
        """
        pass

    def _validate_methods(self) -> None:
        for x, y in self.__class__.__dict__.items():
            if type(y) == FunctionType and x.startswith("validate"):
                try:
                    y(self)
                except InvalidValueError as e:
                    for key, value in e.error_value_by_key.items():
                        if key in e.add_skip_validation_keys:
                            self.add_error_and_skip_validation_key(key, value)
                        else:
                            self.add_error_context(key, value)

    def validate(self) -> None:
        if not self._validate_called:
            self._validate_mandatory_payloads()
            self._validate_payloads_type()
            self._validate_methods()
            self._common_validate()
            self._validate_called = True
        if self._error_context:
            raise ValidationException()

    @property
    def error_context(self) -> ValidatorErrorContext:
        if not self._validate_called:
            raise ValidationNotRunException("validate method should run before accessing error_context")
        return self._error_context

    def is_valid(self) -> bool:
        try:
            self.validate()
        except ValidationException:
            return False
        return True
