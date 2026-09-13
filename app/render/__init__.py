"""
Render Engine for Math Motion
Handles Manim rendering and FFmpeg video processing.
"""

from .manim_renderer import ManimRenderer
from .ffmpeg import FFmpegProcessor

__all__ = ['ManimRenderer', 'FFmpegProcessor']
