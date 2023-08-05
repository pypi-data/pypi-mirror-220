from __future__ import annotations

import time
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional

import pyautogui

from .tween import get_tween_function


@dataclass
class Point:
    x: float = 0.0
    y: float = 0.0
    duration: float = 0.0
    tween: Optional[str] = None
    button: Optional[str] = None
    delay: bool = False
    drag: bool = False
    relative: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def create_delay(delay: float = 1.0) -> Point:
        return Point(duration=delay, delay=True)

    @staticmethod
    def create_from_dict(dikt: Dict[str, Any]) -> Point:
        return Point(**dikt)


def trace(points: List[Point]) -> None:
    for point in points:
        tween = get_tween_function(point.tween)
        button = point.button if point.button else "primary"

        if point.delay:
            time.sleep(point.duration)
            continue

        if point.drag and point.relative:
            pyautogui.dragRel(
                xOffset=point.x,
                yOffset=point.y,
                duration=point.duration,
                tween=tween,
                button=button,
            )
            continue

        if point.drag and not point.relative:
            pyautogui.dragTo(
                x=point.x,
                y=point.y,
                duration=point.duration,
                tween=tween,
                button=button,
            )
            continue

        if not point.drag and point.relative:
            pyautogui.moveRel(
                xOffset=point.x,
                yOffset=point.y,
                duration=point.duration,
                tween=tween,
            )
            continue

        if not point.drag and not point.relative:
            pyautogui.moveTo(
                x=point.x,
                y=point.y,
                duration=point.duration,
                tween=tween,
            )
            continue


__all__ = [
    "Point",
    "trace",
]
