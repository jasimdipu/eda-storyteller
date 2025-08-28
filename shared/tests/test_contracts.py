from __future__ import annotations
import json
from pathlib import Path
import pytest

# Use your structure: shared.shared.schemas
from shared.shared.schemas import DatasetProfile, Actions

EX = Path(__file__).parent / "examples"

def _load(name: str):
    return json.loads((EX / name).read_text())

def test_profile_valid_passes():
    payload = _load("profile_valid.json")
    obj = DatasetProfile.model_validate(payload)
    assert obj.dataset.rows == 1000

def test_profile_invalid_fails():
    payload = _load("profile_invalid.json")
    with pytest.raises(Exception) as e:
        DatasetProfile.model_validate(payload)
    assert "dataset" in str(e.value) and "rows" in str(e.value)

def test_actions_valid_passes():
    payload = _load("actions_valid.json")
    obj = Actions.model_validate(payload)
    assert obj.priority in {"high", "medium", "low"}
