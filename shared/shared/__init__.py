from .schemas import DatasetProfile, Actions, Suggestion, CodeSnippet
from .schemas.profile import SCHEMA_VERSION as PROFILE_SCHEMA_VERSION
from .schemas.actions import SCHEMA_VERSION as ACTIONS_SCHEMA_VERSION

__all__ = [
    "DatasetProfile",
    "Actions",
    "Suggestion",
    "CodeSnippet",
    "PROFILE_SCHEMA_VERSION",
    "ACTIONS_SCHEMA_VERSION",
]

# Package version (bump on breaking changes to contracts)
__version__ = "0.1.1"
