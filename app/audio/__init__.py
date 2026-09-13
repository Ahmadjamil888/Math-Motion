"""
Audio Engine for Math Motion
Handles music loading, beat detection, energy analysis, and synchronization.
"""

from .loader import AudioLoader
from .beat_detection import BeatDetector
from .energy import EnergyAnalyzer
from .sync import AudioSync

__all__ = ['AudioLoader', 'BeatDetector', 'EnergyAnalyzer', 'AudioSync']
