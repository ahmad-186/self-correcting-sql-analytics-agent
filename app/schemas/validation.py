from pydantic import BaseModel, Field

from enum import Enum


class ValidationCheck(str, Enum):
    """
    Represents the different validation checks
    performed on generated SQL.
    """

    READ_ONLY = "read_only"
    SYNTAX = "syntax"
    SCHEMA = "schema"
    EXECUTION = "execution"

class SQLValidationResult(BaseModel):
    """
    Result returned by the SQL validation layer.
    """

    is_valid: bool = Field(description="Whether the SQL passed all validation checks.")
    failed_Check: ValidationCheck | None = Field(default=None, description="The validation check that failed.")
    error_message: str | None = Field(default=None, description="Human readable validation error.")
