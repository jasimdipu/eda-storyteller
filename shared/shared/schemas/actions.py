from __future__ import annotations
from typing import List, Literal, Optional, Dict, Any
from pydantic import BaseModel, Field

SCHEMA_VERSION = "0.1.1"

SuggestionType = Literal[
    "fix_dtype", "impute", "drop_outliers", "encode", "normalize",
    "ts_model_hint", "data_quality_check", "deduplicate"
]


class CodeSnippet(BaseModel):
    lang: Literal["python", "sql"]
    stage: Literal["cleaning", "eda", "feature", "model"]
    body: str


class Suggestion(BaseModel):
    type: SuggestionType
    column: Optional[str] = None
    strategy: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    reason: Optional[str] = None


class Actions(BaseModel):
    schema_version: str = Field(default=SCHEMA_VERSION)
    priority: Literal["high", "medium", "low"] = "medium"
    suggestions: List[Suggestion] = Field(default_factory=list)
    code_snippets: List[CodeSnippet] = Field(default_factory=list)
