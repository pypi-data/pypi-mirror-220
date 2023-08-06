import unittest

from payload_validator.exceptions import (
    InvalidValueError,
    MismatchedErrorKeysException,
    ValidationException,
    ValidationNotRunException,
)
from payload_validator.validators import (
    NormalValidatorErrorContext,
    PayloadValidator,
)


class TestNormalValidatorErrorContext(unittest.TestCase):
    def test_add_error_should_add_errors_when_new_error_add_to_field(self):
        # Given:
        context = NormalValidatorErrorContext()

        # When:
        context.add_error("field1", "error1")

        # Then:
        self.assertEqual(context["field1"], ["error1"])
        self.assertEqual(len(context), 1)

    def test_add_error_should_add_errors_when_old_error_exists(self):
        # Given: Add default error
        context = NormalValidatorErrorContext()
        context.add_error("field1", "error1")

        # When: Adding errors to a field
        context.add_error("field1", "error2")

        # Then:
        self.assertEqual(context["field1"], ["error1", "error2"])
        self.assertEqual(len(context), 1)

    def test_add_error_should_add_errors_when_different_fields_are_set(self):
        # Given: Add default error
        context = NormalValidatorErrorContext()
        context.add_error("field1", "error1")
        self.assertEqual(context["field1"], ["error1"])

        # When: Adding errors to a field
        context.add_error("field2", "error2")

        # Then:
        self.assertEqual(context["field2"], ["error2"])
        self.assertEqual(len(context), 2)

    def test_validation_error_context_constructor_add_error_should_add_errors_when_new_error_add_to_field(self):
        # Given: Existing errors are preserved
        context = NormalValidatorErrorContext({"field1": ["error1"]})
        self.assertEqual(context["field1"], ["error1"])

        # When:
        context.add_error("field2", "error2")
        self.assertEqual(context["field2"], ["error2"])


class TestPayloadValidator(unittest.TestCase):
    def test_payload_validator_should_return_error_context_when_is_valid_method_missing_keys_error_exists(self):
        # Given: Mandatory payload
        class MandatoryPayloadValidator(PayloadValidator):
            class Meta:
                mandatory_keys = {"displayable": "displayable is required"}
        # And: Payload is missing mandatory key
        payload = {"another_key": "value"}

        # When:
        validator = MandatoryPayloadValidator(payload)

        # Then: is_valid() should return False
        self.assertEqual(validator.is_valid(), False)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context["displayable"]), 1)
        self.assertEqual(
            validator.error_context["displayable"][0],
            MandatoryPayloadValidator.Meta.mandatory_keys["displayable"],
        )

    def test_payload_validator_should_not_return_error_context_when_is_valid_method_missing_keys_error_not_exists(self):
        # Given: Mandatory payload
        class MandatoryPayloadValidator(PayloadValidator):
            class Meta:
                mandatory_keys = {"displayable": "displayable is required"}
        # And:
        payload = {"displayable": True}

        # When:
        validator = MandatoryPayloadValidator(payload)

        # Then: is_valid() should return True
        self.assertEqual(validator.is_valid(), True)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_payload_validator_should_return_error_context_when_validate_method_missing_keys_error_exists(self):
        # Given: Mandatory payload
        class MandatoryPayloadValidator(PayloadValidator):
            class Meta:
                mandatory_keys = {"displayable": "displayable is required"}
        # And: Payload is missing mandatory key
        payload = {"another_key": "value"}

        # When:
        with self.assertRaises(ValidationException):
            validator = MandatoryPayloadValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context["displayable"]), 1)
        self.assertEqual(
            validator.error_context["displayable"][0],
            MandatoryPayloadValidator.Meta.mandatory_keys["displayable"],
        )

    def test_payload_validator_should_not_return_error_context_when_validate_method_missing_keys_error_not_exists(self):
        # Given: Mandatory payload
        class MandatoryPayloadValidator(PayloadValidator):
            class Meta:
                mandatory_keys = {"displayable": "displayable is required"}
        # And:
        payload = {"displayable": True}

        # When:
        validator = MandatoryPayloadValidator(payload)
        validator.validate()

        # Then: there is no errors
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_payload_validator_should_return_error_context_when_validate_method_type_error_exists(self):
        # Given: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "displayable": [bool, "displayable must be a boolean"],
                    "count": [int, "count must be a integer"],
                    "amount": [float, "amount must be a float"],
                    "body": [str, "body must be a string"],
                }
        # And: Payload data type is invalid
        fail_payload = {
            "displayable": "not boolean",
            "count": "not integer",
            "amount": "not float",
            "body": 1,
        }

        # When:
        with self.assertRaises(ValidationException):
            validator = TypeValidPayloadValidator(fail_payload)
            validator.validate()

        # Then: 4 keys should be in error context
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 4)
        # And:
        self.assertEqual(
            validator.error_context["displayable"],
            [TypeValidPayloadValidator.Meta.type_of_keys["displayable"][1]],
        )
        self.assertEqual(
            validator.error_context["count"],
            [TypeValidPayloadValidator.Meta.type_of_keys["count"][1]],
        )
        self.assertEqual(
            validator.error_context["amount"],
            [TypeValidPayloadValidator.Meta.type_of_keys["amount"][1]],
        )
        self.assertEqual(
            validator.error_context["body"],
            [TypeValidPayloadValidator.Meta.type_of_keys["body"][1]],
        )

    def test_payload_validator_should_return_error_context_when_validate_method_missing_keys_and_type_error_exists(self):
        # Given: Type Error Validator with type
        class MandatoryAndTypeValidPayloadValidator(PayloadValidator):
            class Meta:
                mandatory_keys = {
                    "displayable": "displayable is required",
                    "count": None,
                }
                type_of_keys = {
                    "displayable": [bool, "displayable must be a boolean"],
                    "count": [int, "count must be a integer"],
                    "amount": [float, "amount must be a float"],
                    "body": [str, "body must be a string"],
                }
        # And: Payload data is invalid
        fail_payload = {
            "amount": "not float",
            "body": 1,
        }

        # When:
        with self.assertRaises(ValidationException):
            validator = MandatoryAndTypeValidPayloadValidator(fail_payload)
            validator.validate()

        # Then: 4 keys should be in error context
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 4)
        # And: if mandatory key is missing, error message should be only mandatory due to _skip_validate_keys
        self.assertIn("displayable", validator._skip_validate_keys)
        self.assertEqual(
            validator.error_context["displayable"],
            [MandatoryAndTypeValidPayloadValidator.Meta.mandatory_keys["displayable"]],
        )
        self.assertIn("count", validator._skip_validate_keys)
        self.assertEqual(
            validator.error_context["count"],
            [MandatoryAndTypeValidPayloadValidator.DEFAULT_MANDATORY_ERROR_MESSAGE],
        )
        self.assertEqual(
            validator.error_context["amount"],
            [MandatoryAndTypeValidPayloadValidator.Meta.type_of_keys["amount"][1]],
        )
        self.assertEqual(
            validator.error_context["body"],
            [MandatoryAndTypeValidPayloadValidator.Meta.type_of_keys["body"][1]],
        )

    def test_payload_validator_should_not_return_error_context_when_validate_method_type_error_not_exists(self):
        # Given: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "displayable": [bool, "displayable must be a boolean"],
                    "count": [int, "count must be a integer"],
                    "amount": [(float, int), "amount must be a float"],
                    "body": [str, "body must be a string"],
                }
        # And: Payload data type is valid
        valid_payloads = [
            {
                "displayable": True,
                "count": 1,
                "amount": 1.0,
                "body": "valid string",
            },
            {
                "displayable": True,
                "count": 1,
                "amount": 1,
                "body": "valid string",
            }
        ]

        for valid_payload in valid_payloads:
            # When:
            validator = TypeValidPayloadValidator(valid_payload)
            validator.validate()

            # Then: all valid
            self.assertEqual(validator._validate_called, True)
            self.assertEqual(len(validator.error_context), 0)

    def test_payload_validator_should_return_error_context_when_is_valid_method_type_error_exists(self):
        # Given: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "displayable": [bool, "displayable must be a boolean"],
                    "count": [int, "count must be a integer"],
                    "amount": [float, "amount must be a float"],
                    "body": [str, "body must be a string"],
                }
        # And: Payload data type is invalid
        fail_payload = {
            "displayable": "not boolean",
            "count": "not integer",
            "amount": "not float",
            "body": 1,
        }

        # When:
        validator = TypeValidPayloadValidator(fail_payload)

        # Then:
        self.assertEqual(validator.is_valid(), False)
        self.assertEqual(validator._validate_called, True)
        # And: 4 keys should be in error context
        self.assertEqual(len(validator.error_context), 4)
        # And:
        self.assertEqual(
            validator.error_context["displayable"],
            [TypeValidPayloadValidator.Meta.type_of_keys["displayable"][1]],
        )
        self.assertEqual(
            validator.error_context["count"],
            [TypeValidPayloadValidator.Meta.type_of_keys["count"][1]],
        )
        self.assertEqual(
            validator.error_context["amount"],
            [TypeValidPayloadValidator.Meta.type_of_keys["amount"][1]],
        )
        self.assertEqual(
            validator.error_context["body"],
            [TypeValidPayloadValidator.Meta.type_of_keys["body"][1]],
        )

    def test_payload_validator_should_not_return_error_context_when_is_valid_method_type_error_not_exists(self):
        # Given: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "displayable": [bool, "displayable must be a boolean"],
                    "count": [int, "count must be a integer"],
                    "amount": [(float, int), "amount must be a float or integer"],
                    "body": [str, "body must be a string"],
                }
        # And: Payload data type is valid
        valid_payloads = [
            {
                "displayable": True,
                "count": 1,
                "amount": 1.0,
                "body": "valid string",
            },
            {
                "displayable": True,
                "count": 1,
                "amount": 1,
                "body": "valid string",
            }
        ]

        for valid_payload in valid_payloads:
            # When:
            validator = TypeValidPayloadValidator(valid_payload)

            # Then: all valid
            self.assertEqual(validator.is_valid(), True)
            self.assertEqual(validator._validate_called, True)
            self.assertEqual(len(validator.error_context), 0)

    def test_payload_validator_should_return_error_context_when_is_valid_method_type_error_exists_with_function_validate(self):
        # Given: Define a function to validate date parsing
        def validate_date_parsing(date_str):
            return False

        # And: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "start_date": [validate_date_parsing, "start_date %Y-%m-%d type"],
                }
        # And: Payload data type is invalid
        invalid_payload = {
            "start_date": "invalid",
        }

        # When:
        validator = TypeValidPayloadValidator(invalid_payload)

        # Then: invalid
        self.assertEqual(validator.is_valid(), False)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date %Y-%m-%d type"],
        )

    def test_payload_validator_should_not_return_error_context_when_is_valid_method_type_error_not_exists_with_function_validate(self):
        # Given: Define a function to validate date parsing
        def validate_date_parsing(date_str):
            return True

        # And: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "start_date": [validate_date_parsing, "start_date %Y-%m-%d type"],
                }
        # And: Payload data type is valid
        valid_payload = {
            "start_date": "2023-01-01",
        }

        # When:
        validator = TypeValidPayloadValidator(valid_payload)

        # Then: valid
        self.assertEqual(validator.is_valid(), True)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_payload_validator_should_return_error_context_when_validate_method_type_error_exists_with_function_validate(self):
        # Given: Define a function to validate date parsing
        def validate_date_parsing(date_str):
            return False

        # And: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "start_date": [validate_date_parsing, "start_date %Y-%m-%d type"],
                }
        # And: Payload data type is invalid
        invalid_payload = {
            "start_date": "invalid",
        }

        # When:
        with self.assertRaises(ValidationException):
            validator = TypeValidPayloadValidator(invalid_payload)
            validator.validate()

        # Then: invalid
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date %Y-%m-%d type"],
        )

    def test_payload_validator_should_not_return_error_context_when_validate_method_type_error_not_exists_with_function_validate(self):
        # Given: Define a function to validate date parsing
        def validate_date_parsing(date_str):
            return True

        # And: Type Error Validator with type
        class TypeValidPayloadValidator(PayloadValidator):
            class Meta:
                type_of_keys = {
                    "start_date": [validate_date_parsing, "start_date %Y-%m-%d type"],
                }
        # And: Payload data type is valid
        valid_payload = {
            "start_date": "2023-01-01",
        }

        # When:
        validator = TypeValidPayloadValidator(valid_payload)
        validator.validate()

        # Then: valid
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_custom_validate_method_should_return_error_context_when_invalid_at_is_valid_method(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                raise InvalidValueError({"start_date": "start_date error"})
        # And:
        payload = {"start_date": "2023-07-01"}

        validator = CustomValidator(payload)

        # Then:
        self.assertEqual(validator.is_valid(), False)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error"],
        )

    def test_custom_validate_method_should_not_return_error_context_when_valid_at_is_valid_method(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                pass
        # And:
        payload = {"start_date": "2023-07-01"}

        validator = CustomValidator(payload)

        # Then:
        self.assertEqual(validator.is_valid(), True)
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_custom_validate_method_should_return_error_context_when_invalid_at_validate_method(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                raise InvalidValueError({"start_date": "start_date error"})
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error"],
        )

    def test_custom_validate_method_should_return_error_context_when_invalid_at_validate_method_value_with_iterable(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                raise InvalidValueError({"start_date": ["start_date error1", "start_date error2"]})
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error1", "start_date error2"],
        )

    def test_custom_validate_method_should_not_return_error_context_when_valid_at_validate_method(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                pass
        # And:
        payload = {"start_date": "2023-07-01"}

        validator = CustomValidator(payload)
        validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 0)

    def test_custom_validate_method_should_raise_error_when_skip_key_is_not_exists(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date(self):
                raise InvalidValueError({"start_date": "start_date error"}, add_skip_validation_keys=["end_date"])
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(MismatchedErrorKeysException):
            validator = CustomValidator(payload)
            validator.validate()

    def test_custom_validate_method_should_not_return_error_context_when_skip_key_is_exists(self):
        # Given: Custom validate method validation
        class CustomValidator(PayloadValidator):
            def validate_start_date1(self):
                raise InvalidValueError({"start_date": "start_date error1"}, add_skip_validation_keys=["start_date"])

            def validate_start_date2(self):
                raise InvalidValueError({"start_date": "start_date error2"})
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertIn("start_date", validator._skip_validate_keys)
        self.assertEqual(len(validator.error_context), 1)
        # And: Due to add_skip_validation_keys, validate_start_date1 error is not exists
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error1"],
        )

    def test_common_validate_method_should_return_error_context_when_invalid_by_validate_method(self):
        # Given: common_validate method validation
        class CustomValidator(PayloadValidator):
            def common_validate(self):
                raise InvalidValueError({"start_date": "start_date error"})
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error"],
        )

    def test_common_validate_method_should_not_return_error_context_when_skip_key_is_exists(self):
        # Given: common_validate method validation
        class CustomValidator(PayloadValidator):
            def common_validate(self):
                raise InvalidValueError({"start_date": "start_date error"}, add_skip_validation_keys=["start_date"])
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertIn("start_date", validator._skip_validate_keys)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error"],
        )

    def test_add_error_context_method_should_return_error_context(self):
        # Given: common_validate method validation
        class CustomValidator(PayloadValidator):
            def common_validate(self):
                self.add_error_context("start_date", "start_date error1")
                self.add_error_context("start_date", ["start_date error2", "start_date error3"])
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertEqual(len(validator.error_context), 1)
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error1", "start_date error2", "start_date error3"],
        )

    def test_add_error_and_skip_validation_key_method_should_return_error_context(self):
        # Given: common_validate method validation
        class CustomValidator(PayloadValidator):
            def common_validate(self):
                self.add_error_and_skip_validation_key("start_date", "start_date error1")
                self.add_error_and_skip_validation_key("start_date", ["start_date error2", "start_date error3"])
        # And:
        payload = {"start_date": "2023-07-01"}

        with self.assertRaises(ValidationException):
            validator = CustomValidator(payload)
            validator.validate()

        # Then:
        self.assertEqual(validator._validate_called, True)
        self.assertIn("start_date", validator._skip_validate_keys)
        self.assertEqual(len(validator.error_context), 1)
        # And: Due to add_skip_validation_keys error is not exists
        self.assertEqual(
            validator.error_context["start_date"],
            ["start_date error1"],
        )

    def test_error_context_without_validation(self):
        # Given:
        payload = {"displayable": "example"}
        validator = PayloadValidator(payload)

        # Excepted: validate or is_valid method not called
        with self.assertRaises(ValidationNotRunException):
            _ = validator.error_context
