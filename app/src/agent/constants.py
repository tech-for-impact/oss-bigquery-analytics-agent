from typing import Final

# API Configuration
API_VERSION: Final[str] = "v1"
DEFAULT_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3

# Database Configuration
DB_HOST: Final[str] = "localhost"
DB_PORT: Final[int] = 5432
DB_NAME: Final[str] = "analytics"
DB_POOL_SIZE: Final[int] = 20

# Prompt Configuration
PROMPT_TEMPLATE_PATH: Final[str] = "prompts/categorized/categorized.yml"
FEW_SHOT_EXAMPLES_PATH: Final[str] = "prompts/categorized/few_shot_examples.yml"

# Response Types
class ResponseType:
    SQL: Final[str] = "SQL"
    GENERAL: Final[str] = "GENERAL"

# Error Messages
class ErrorMessages:
    INVALID_INPUT: Final[str] = "Invalid input provided"
    DATABASE_ERROR: Final[str] = "Database connection error"
    PROMPT_LOAD_ERROR: Final[str] = "Failed to load prompt template"

# Export specific constants
__all__ = [
    'API_VERSION',
    'DEFAULT_TIMEOUT',
    'MAX_RETRIES',
    'DB_HOST',
    'DB_PORT',
    'DB_NAME',
    'DB_POOL_SIZE',
    'PROMPT_TEMPLATE_PATH',
    'FEW_SHOT_EXAMPLES_PATH',
    'ResponseType',
    'ErrorMessages'
] 