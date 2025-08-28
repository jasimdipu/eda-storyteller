from __future__ import annotations
import json, os
from pathlib import Path
from logging import getLogger
from shared.schemas import DatasetProfile, Actions

logger = getLogger(__name__)

OUT_DIR = Path(os.path.dirname(__file__)).resolve().parents[1] / "dist" / "schemas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def dump(name:str, model, version:str):
    schema = model.model_json_schema()
    schema["$id"] = f"https://eda-storyteller.com/schemas/{name}_v{version}.json"
    out = OUT_DIR / f"{name}_v{version}.json"
    out.write_text(json.dumps(schema, indent=2))
    logger.info(f"Wrote {out}")


if __name__ == "__main__":
    v_profile = "0.1.1"
    v_actions = Actions.model_fields["schema_version"].default
    dump("profile", DatasetProfile, v_profile)
    dump("actions", Actions, v_actions)