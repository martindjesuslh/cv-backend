from typing import Dict


class Settings:
    API_BASE_URL: str = ""
    REQUEST_TIMEOUT: int = 30
    SCRAPED_TIMEOUT: int = 30

    MESSAGES_RESPONSE: Dict[str, str] = {
        "SUCCESS": "Operation completed successfully",
        "CREATED": "Resource created successfully",
        "UPDATED": "Resource updated successfully",
        "DELETED": "Resource deleted successfully",
        "NOT_FOUND": "Resource not found",
        "BAD_REQUEST": "Invalid request data",
        "UNAUTHORIZED": "Authentication required",
        "FORBIDDEN": "Access denied",
        "INTERNAL_ERROR": "Internal server error",
    }


settings = Settings()
