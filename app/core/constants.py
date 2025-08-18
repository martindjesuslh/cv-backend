from enum import Enum


class SelectorsIndeed(Enum):
    BUTTON_SKILLS = "button.js-match-insights-provider-7yw9u9 e19afand0"


class ResponseMessages:
    SUCCESS = "Operation completed successfully"
    CREATED = "Resource created successfully"
    UPDATED = "Resource updated successfully"
    DELETED = "Resource deleted successfully"
    NOT_FOUND = "Resource not found"
    BAD_REQUEST = "Invalid request data"
    UNAUTHORIZED = "Authentication required"
    FORBIDDEN = "Access denied"
    INTERNAL_ERROR = "Internal server error"
