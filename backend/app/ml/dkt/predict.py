from pathlib import Path
import numpy as np
from app.core.config import settings

def demo_mastery(topic, correct_history):
    vals=[1 if x else 0 for x in correct_history]
    if not vals: return .5
    return float(np.clip(.35 + .55*(sum(vals)/len(vals)) + .03*min(len(vals),5), .05, .98))

def predict_mastery(topic, history):
    # Trained mode is deliberately opt-in. The demo path is fully functional without torch.
    if settings.dkt_mode != "trained" or not Path(settings.model_path).exists():
        return demo_mastery(topic, history)
    try:
        # The current checkpoint contract is intentionally kept behind an optional import.
        from .model import DKTModel  # noqa: F401
    except Exception:
        return demo_mastery(topic, history)
    # A real checkpoint needs its topic vocabulary/feature mapping; until those are supplied,
    # use the documented fallback rather than producing an invalid prediction.
    return demo_mastery(topic, history)
