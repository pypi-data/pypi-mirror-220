from typing import List, Optional

from .ctypes import Action, Config


def trace(actions: List[Action], config: Optional[Config] = None) -> None:
    config = config if config else Config()
    for action in actions:
        action.execute(config=config)


__all__ = [
    "trace",
]
