import json
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA_DIR, "mitre_attack.json")) as f:
    _TECHNIQUES = json.load(f)

_INDEX = {t["technique_id"]: t for t in _TECHNIQUES}


def get_technique(technique_id: str):
    return _INDEX.get(technique_id)


def all_techniques():
    return _TECHNIQUES


def techniques_as_prompt_context():
    """Compact string representation fed to the LLM for mapping decisions."""
    return "\n".join(
        f"{t['technique_id']} ({t['tactic']}): {t['name']} - {t['description']}"
        for t in _TECHNIQUES
    )
