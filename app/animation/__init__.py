"""
Animation Engine for Math Motion
Handles scene composition, timeline management, and visual effects.
"""

from .scene import MathScene
from .timeline import AnimationTimeline
from .transitions import TransitionManager
from .effects import EffectManager

__all__ = ['MathScene', 'AnimationTimeline', 'TransitionManager', 'EffectManager']
