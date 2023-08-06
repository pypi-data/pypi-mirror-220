================================
Payload Validator
================================

To validate the payload data.


Quick Start
============

pip install payload-validator


Example Code
=============
CodeSandBox Link:

https://codesandbox.io/p/sandbox/payload-validator-zngckp?file=%2Fmain.py%3A1%2C1



Explain
============

Normal ValidatorErrorContext Usage

using_this_payload.py::

    from datetime import datetime
    from payload_validator.exceptions import (
        InvalidValueError,
        ValidationException,
    )
    from utils import validate_date_parsing
    from payload_validator.validators import PayloadValidator


    def validate_date_parsing(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except (TypeError, ValueError):
            return False


    # [ Examples of using validators ]
    # 1. Inherit 'PayloadValidator' and define 'Meta class'
    # 2. Define 'DEFAULT_MANDATORY_ERROR_MESSAGE' in 'PayloadValidator'
    # 3-1. Define 'mandatory_keys' and 'type_of_keys' in 'Meta class'
    # 3-2. 'mandatory_keys' is a 'dictionary' that contains key and error message
    # 3-3. 'type_of_keys' is a 'dictionary' that contains key and type of key
    # 3-4. 'type_of_keys' value of first index can contain 'function' returning 'boolean' accepted
    # 4-1. Define 'validate_{key}' method in 'PayloadValidator'
    # 4-2. 'validate_{key}' validating sequence is top to bottom code written in 'PayloadValidator'
    # 4-3. If 'validate_{key}' raise 'InvalidValueError', it will be added to 'error_context'
    # 4-4. 'InvalidValueError' 'error_value_by_key' input should be 'dictionary' that contains payload key and error message (this message could be iterator)
    # 4-5. 'InvalidValueError' input can contain 'add_skip_validation_keys' which skip if there is already payload key of error
    # 5. Can override 'common_validate' method to add 'common_validation'
    # 6. Validating Sequence: Mandatory Check -> Type Check -> validate_{key} (top from bottom code) -> common_validate
    # 7. Use 'validate()' method to validate payload or execute 'is_valid()' method to check validation even once
    # 8. 'ValidationException' will raise when error exists

    # [ Extra Information ]
    # you can use 'add_error_context' or 'add_error_and_skip_validation_key'
    # instead of 'InvalidValueError' to define errors

    # 1
    class NewPayloadValidator(PayloadValidator):
        # 2
        DEFAULT_MANDATORY_ERROR_MESSAGE = 'mandatory data missing2'

        class Meta:
            # 3-1, 3-2
            mandatory_keys = {
                'displayable': 'displayable is required',
                'mode': 'mode is always required',
                'amount': 'why are you not setting amount?',
                'minimum_order_value': 'minimum order value is required',
                'applicable_order_types': 'really you are not setting applicable order types?',
                'start_date': 'start date is required',
                'end_date': 'end date is required for your job',
            }
            # 3-1, 3-3
            type_of_keys = {
                'amount': [int, 'integer_type_needs'],
                'minimum_order_value': [int, 'integer_type_needs'],
                'maximum_download_count': [(int, type(None)), 'integer_type_needs or NoneType'],
                # 3-4
                'start_date': [validate_date_parsing, 'need to be date type'],
                'end_date': [validate_date_parsing, 'need to be date type'],
            }

        # 4-1, 4-2
        def validate_hello_world(self):
            if not self.payload['displayable']:
                # 4-3, 4-4
                raise InvalidValueError({'displayable': 'displayable is false'})

        # 4-1, 4-2
        def validate_max_length(self):
            if self.payload['max_length'] <= 0:
                # 4-3, 4-4, 4-5
                raise InvalidValueError(
                    {
                        'max_length': 'min_length should be greater than 0'
                    },
                    add_skip_validation_keys=['max_length']
                )

        # 5
        def common_validate(self):
            if self.payload['max_length'] < self.payload['min_length']:
                raise InvalidValueError(
                    {
                        'max_length': 'max_length should be greater than min_length',
                        'min_length': 'min_length should be lesser than max_length'
                    },
                )



    validator = NewPayloadValidator({'displayable': True, 'start_date': 1, 'min_length': 10, 'max_length': 0})

    try:
        # 7
        validator.validate()
    except ValidationException as e:
        print(validator.error_context)

    # 8
    if not validator.is_valid():
        print(validator.error_context)

    # [ Result ]
    # {
    #     'mode': ['mode is always required'],
    #     'amount': ['why are you not setting amount?'],
    #     'minimum_order_value': ['minimum order value is required'],
    #     'applicable_order_types': ['really you are not setting applicable order types?'],
    #     'end_date': ['end date is required for your job'],
    #     'start_date': ['need to be date type'],
    #     'max_length': ['min_length should be greater than 0'],
    #     'min_length': ['min_length should be lesser than max_length']
    # }


Custom ValidatorErrorContext Usage

custom_using_this_payload.py::

    from datetime import datetime
    from payload_validator.exceptions import (
        InvalidValueError,
        ValidationException,
    )
    from utils import validate_date_parsing
    from payload_validator.validators import PayloadValidator, ValidatorErrorContext

    def validate_date_parsing(date_str):
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except (TypeError, ValueError):
            return False

    # [ Examples of using validators ]
    # 1. Inherit 'PayloadValidator' and define 'Meta class'
    # 2. Define 'DEFAULT_MANDATORY_ERROR_MESSAGE' in 'PayloadValidator'
    # 3-1. Define 'mandatory_keys' and 'type_of_keys' in 'Meta class'
    # 3-2. 'mandatory_keys' is a 'dictionary' that contains key and error message
    # 3-3. 'type_of_keys' is a 'dictionary' that contains key and type of key
    # 3-4. 'type_of_keys' value of first index can contain 'function' returning 'boolean' accepted
    # 4-1. Define 'validate_{key}' method in 'PayloadValidator'
    # 4-2. 'validate_{key}' validating sequence is top to bottom code written in 'PayloadValidator'
    # 4-3. If 'validate_{key}' raise 'InvalidValueError', it will be added to 'error_context'
    # 4-4. 'InvalidValueError' 'error_value_by_key' input should be 'dictionary' that contains payload key and error message (this message could be iterator)
    # 4-5. 'InvalidValueError' input can contain 'add_skip_validation_keys' which skip if there is already payload key of error
    # 5. Can override 'common_validate' method to add 'common_validation'
    # 6. Validating Sequence: Mandatory Check -> Type Check -> validate_{key} (top from bottom code) -> common_validate
    # 7. Use 'validate()' method to validate payload or execute 'is_valid()' method to check validation even once
    # 8. 'ValidationException' will raise when error exists

    # [ Extra Information ]
    # you can use 'add_error_context' or 'add_error_and_skip_validation_key'
    # instead of 'InvalidValueError' to define errors

    # Extra: Customize Error Context
    # 'ColorValidatorErrorContext' is a 'PayloadValidator' can return error message with color
    class ColorValidatorErrorContext(ValidatorErrorContext):
        DEFAULT_COLOR = '#FFFFFF'

        def add_error(self, field: str, error: str):
            value = self.setdefault(field, [])
            try:
                error, color = error.split(',')
            except (IndexError, ValueError):
                color = self.DEFAULT_COLOR
            value.append([error, color])


    # 1
    class ColorPayloadValidator(PayloadValidator):
        # 2
        DEFAULT_MANDATORY_ERROR_MESSAGE = 'mandatory data missing2'

        class Meta:
            # 3-1, 3-2
            mandatory_keys = {
                'displayable': 'displayable is required',
                'mode': 'mode is always required',
                'amount': 'why are you not setting amount?',
                'minimum_order_value': 'minimum order value is required',
                'applicable_order_types': 'really you are not setting applicable order types?',
                'start_date': 'start date is required',
                'end_date': 'end date is required for your job',
            }
            # 3-1, 3-3
            type_of_keys = {
                'amount': [int, 'integer_type_needs'],
                'minimum_order_value': [int, 'integer_type_needs'],
                'maximum_download_count': [(int, type(None)), 'integer_type_needs or NoneType'],
                # 3-4
                'start_date': [validate_date_parsing, 'need to be date type'],
                'end_date': [validate_date_parsing, 'need to be date type'],
            }

        # 4-1, 4-2
        def validate_hello_world(self):
            if not self.payload['displayable']:
                # 4-3, 4-4
                raise InvalidValueError({'displayable': 'displayable is false,#123456'})

        # 4-1, 4-2
        def validate_max_length(self):
            if self.payload['max_length'] <= 0:
                # 4-3, 4-4, 4-5
                raise InvalidValueError(
                    {
                        'max_length': 'min_length should be greater than 0,#000000'
                    },
                    add_skip_validation_keys=['max_length']
                )

        # 5
        def common_validate(self):
            if self.payload['max_length'] < self.payload['min_length']:
                raise InvalidValueError(
                    {
                        'max_length': 'max_length should be greater than min_length,#000000',
                        'min_length': 'min_length should be lesser than max_length,#123123'
                    },
                )


    validator = ColorPayloadValidator(
        {'displayable': True, 'start_date': 1, 'min_length': 10, 'max_length': 0},
        ColorValidatorErrorContext(),
    )

    try:
        # 7
        validator.validate()
    except ValidationException as e:
        print(validator.error_context)

    # 8
    if not validator.is_valid():
        print(validator.error_context)

    # [ Result ]
    # {
    #     'mode': [['mode is always required', '#FFFFFF']],
    #     'amount': [['why are you not setting amount?', '#FFFFFF']],
    #     'minimum_order_value': [['minimum order value is required', '#FFFFFF']],
    #     'applicable_order_types': [['really you are not setting applicable order types?', '#FFFFFF']],
    #     'end_date': [['end date is required for your job', '#FFFFFF']],
    #     'start_date': [['need to be date type', '#FFFFFF']],
    #     'max_length': [['min_length should be greater than 0', '#000000']],
    #     'min_length': [['min_length should be lesser than max_length', '#123123']]
    # }



Extra
========

Issue or Pull Request are welcome.
