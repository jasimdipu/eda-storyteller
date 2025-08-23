from __future__ import annotations
from typing import List, Dict, Optional, Any
from pydantic import BaseModel


class ColumnProfile(BaseModel):
    dtype: str
    missing_rate: float | None = None
    unique_rate: float | None = None
    skew: float | None = None
    outlier_rate: float | None = None
    cardinality: int | None = None


class DatasetSection(BaseModel):
    rows: int
    cols: int
    memory_bites: int | None = None


class TimeseriesSection(BaseModel):
    detected: bool = False
    index: Optional[str] = None
    freq: Optional[str] = None
    seasonality: List[str] = []


class QualitySection(BaseModel):
    duplicates_rate: float | None = None


class DatasetProfile(BaseModel):
    dataset: DatasetSection
    columns: Dict[str, ColumnProfile]
    relationships: Dict[str, Any] | None = None
    timeseries: TimeseriesSection | None = None
    quality: QualitySection | None = None