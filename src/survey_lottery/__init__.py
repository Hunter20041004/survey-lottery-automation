"""Privacy-safe survey lottery automation."""

from .domain import Participant
from .draw import draw_winners

__all__ = ["Participant", "draw_winners"]
