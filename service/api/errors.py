class SchemaValidationError(Exception):
    pass


class InvalidDateTimeFormatError(Exception):
    pass


class InvalidIntegerFormatError(Exception):
    pass


class DuplicateIdError(Exception):
    pass


errors = {
    "SchemaValidationError": {
        "message": "Request is missing required fields",
        "status": 400,
    },
    "InvalidDateTimeFormatError": {
        "message": "Invalid input syntax for type timestamp with time zone",
        "status": 400,
    },
    "InvalidIntegerFormatError": {
        "message": "Invalid input syntax for type integer",
        "status": 400,
    },
    "DuplicateIdError": {
        "message": "Request Parameter(user_id) is duplicated",
        "status": 400,
    },
}