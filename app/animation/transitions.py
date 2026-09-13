"""
Transition Manager
Handles smooth transitions between animation states.
"""

import numpy as np
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class TransitionType(Enum):
    """Types of transitions."""
    FADE = "fade"
    SLIDE = "slide"
    ZOOM = "zoom"
    ROTATE = "rotate"
    SCALE = "scale"
    DISSOLVE = "dissolve"
    WIPE = "wipe"
    MORPH = "morph"
    ELASTIC = "elastic"
    BOUNCE = "bounce"


class TransitionDirection(Enum):
    """Direction of transitions."""
    LEFT_TO_RIGHT = "left_to_right"
    RIGHT_TO_LEFT = "right_to_left"
    TOP_TO_BOTTOM = "top_to_bottom"
    BOTTOM_TO_TOP = "bottom_to_top"
    CENTER_OUT = "center_out"
    CENTER_IN = "center_in"


@dataclass
class Transition:
    """Transition configuration."""
    transition_type: TransitionType
    duration: float = 1.0
    direction: TransitionDirection = TransitionDirection.LEFT_TO_RIGHT
    easing: str = "ease_in_out"
    parameters: Dict = None


class TransitionManager:
    """Manages transitions between animation states."""
    
    def __init__(self):
        self.active_transitions: List[Transition] = []
        self.transition_callbacks: Dict[str, Callable] = {}
        self.default_duration = 1.0
        self.default_easing = "ease_in_out"
    
    def create_transition(self, transition_type: TransitionType, 
                         duration: float = None,
                         direction: TransitionDirection = None,
                         easing: str = None,
                         parameters: Dict = None) -> Transition:
        """
        Create a transition configuration.
        
        Args:
            transition_type: Type of transition
            duration: Duration in seconds
            direction: Direction of transition
            easing: Easing function name
            parameters: Additional parameters
            
        Returns:
            Transition object
        """
        if duration is None:
            duration = self.default_duration
        if direction is None:
            direction = TransitionDirection.LEFT_TO_RIGHT
        if easing is None:
            easing = self.default_easing
        if parameters is None:
            parameters = {}
        
        return Transition(
            transition_type=transition_type,
            duration=duration,
            direction=direction,
            easing=easing,
            parameters=parameters
        )
    
    def apply_fade_transition(self, start_opacity: float = 0.0, 
                             end_opacity: float = 1.0,
                             duration: float = 1.0) -> Dict:
        """
        Create fade transition parameters.
        
        Args:
            start_opacity: Starting opacity
            end_opacity: Ending opacity
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.FADE,
            'start_opacity': start_opacity,
            'end_opacity': end_opacity,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_slide_transition(self, direction: TransitionDirection,
                              distance: float = 10.0,
                              duration: float = 1.0) -> Dict:
        """
        Create slide transition parameters.
        
        Args:
            direction: Direction of slide
            distance: Distance to slide
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.SLIDE,
            'direction': direction,
            'distance': distance,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_zoom_transition(self, start_scale: float = 0.5,
                             end_scale: float = 1.0,
                             duration: float = 1.0) -> Dict:
        """
        Create zoom transition parameters.
        
        Args:
            start_scale: Starting scale
            end_scale: Ending scale
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.ZOOM,
            'start_scale': start_scale,
            'end_scale': end_scale,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_rotate_transition(self, start_angle: float = 0.0,
                               end_angle: float = 360.0,
                               duration: float = 1.0) -> Dict:
        """
        Create rotate transition parameters.
        
        Args:
            start_angle: Starting angle in degrees
            end_angle: Ending angle in degrees
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.ROTATE,
            'start_angle': start_angle,
            'end_angle': end_angle,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_scale_transition(self, start_scale: float = 1.0,
                              end_scale: float = 1.5,
                              duration: float = 1.0) -> Dict:
        """
        Create scale transition parameters.
        
        Args:
            start_scale: Starting scale factor
            end_scale: Ending scale factor
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.SCALE,
            'start_scale': start_scale,
            'end_scale': end_scale,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_wipe_transition(self, direction: TransitionDirection,
                             duration: float = 1.0) -> Dict:
        """
        Create wipe transition parameters.
        
        Args:
            direction: Direction of wipe
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.WIPE,
            'direction': direction,
            'duration': duration,
            'easing': 'linear'
        }
    
    def apply_morph_transition(self, morph_points: List[np.ndarray],
                              duration: float = 1.0) -> Dict:
        """
        Create morph transition parameters.
        
        Args:
            morph_points: List of target points for morphing
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.MORPH,
            'morph_points': morph_points,
            'duration': duration,
            'easing': 'ease_in_out'
        }
    
    def apply_elastic_transition(self, intensity: float = 0.5,
                                duration: float = 1.0) -> Dict:
        """
        Create elastic transition parameters.
        
        Args:
            intensity: Intensity of elastic effect
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.ELASTIC,
            'intensity': intensity,
            'duration': duration,
            'easing': 'elastic'
        }
    
    def apply_bounce_transition(self, bounce_count: int = 3,
                               intensity: float = 0.5,
                               duration: float = 1.0) -> Dict:
        """
        Create bounce transition parameters.
        
        Args:
            bounce_count: Number of bounces
            intensity: Intensity of bounce effect
            duration: Duration in seconds
            
        Returns:
            Transition parameters dictionary
        """
        return {
            'type': TransitionType.BOUNCE,
            'bounce_count': bounce_count,
            'intensity': intensity,
            'duration': duration,
            'easing': 'bounce'
        }
    
    def get_easing_function(self, easing: str) -> Callable[[float], float]:
        """
        Get easing function by name.
        
        Args:
            easing: Name of easing function
            
        Returns:
            Easing function
        """
        easing_functions = {
            'linear': lambda t: t,
            'ease_in': lambda t: t * t,
            'ease_out': lambda t: t * (2 - t),
            'ease_in_out': lambda t: t * t * (3 - 2 * t),
            'elastic': lambda t: t * t * ((t * 2 - 1) * (t * 2 - 3)),
            'bounce': lambda t: 1 - abs(np.cos(t * np.pi * 2) * np.exp(-t * 3)),
            'exponential_in': lambda t: t ** 3,
            'exponential_out': lambda t: 1 - (1 - t) ** 3,
            'sine_in': lambda t: 1 - np.cos(t * np.pi / 2),
            'sine_out': lambda t: np.sin(t * np.pi / 2),
            'sine_in_out': lambda t: (1 - np.cos(t * np.pi)) / 2
        }
        
        return easing_functions.get(easing, lambda t: t)
    
    def interpolate_value(self, start: float, end: float, 
                        progress: float, easing: str = 'linear') -> float:
        """
        Interpolate between two values with easing.
        
        Args:
            start: Starting value
            end: Ending value
            progress: Progress (0.0 to 1.0)
            easing: Easing function name
            
        Returns:
            Interpolated value
        """
        easing_func = self.get_easing_function(easing)
        eased_progress = easing_func(max(0.0, min(1.0, progress)))
        return start + (end - start) * eased_progress
    
    def interpolate_position(self, start_pos: np.ndarray, end_pos: np.ndarray,
                           progress: float, easing: str = 'linear') -> np.ndarray:
        """
        Interpolate between two positions.
        
        Args:
            start_pos: Starting position
            end_pos: Ending position
            progress: Progress (0.0 to 1.0)
            easing: Easing function name
            
        Returns:
            Interpolated position
        """
        easing_func = self.get_easing_function(easing)
        eased_progress = easing_func(max(0.0, min(1.0, progress)))
        return start_pos + (end_pos - start_pos) * eased_progress
    
    def interpolate_color(self, start_color: str, end_color: str,
                         progress: float, easing: str = 'linear') -> str:
        """
        Interpolate between two colors.
        
        Args:
            start_color: Starting color (hex or name)
            end_color: Ending color (hex or name)
            progress: Progress (0.0 to 1.0)
            easing: Easing function name
            
        Returns:
            Interpolated color as hex string
        """
        # Simple implementation - convert to RGB, interpolate, convert back
        from manim import parse_color
        
        start_rgb = parse_color(start_color).get_rgb()
        end_rgb = parse_color(end_color).get_rgb()
        
        easing_func = self.get_easing_function(easing)
        eased_progress = easing_func(max(0.0, min(1.0, progress)))
        
        interpolated_rgb = [
            start_rgb[i] + (end_rgb[i] - start_rgb[i]) * eased_progress
            for i in range(3)
        ]
        
        # Convert back to hex
        r = int(interpolated_rgb[0] * 255)
        g = int(interpolated_rgb[1] * 255)
        b = int(interpolated_rgb[2] * 255)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def register_transition_callback(self, transition_type: str, callback: Callable):
        """
        Register a callback for a specific transition type.
        
        Args:
            transition_type: Type of transition
            callback: Function to call when transition occurs
        """
        self.transition_callbacks[transition_type] = callback
    
    def execute_transition(self, transition: Transition, progress: float):
        """
        Execute a transition at a specific progress.
        
        Args:
            transition: Transition to execute
            progress: Progress (0.0 to 1.0)
        """
        # Call registered callback if exists
        if transition.transition_type.value in self.transition_callbacks:
            callback = self.transition_callbacks[transition.transition_type.value]
            callback(transition, progress)
    
    def create_preset_transition(self, preset_name: str) -> Optional[Transition]:
        """
        Create a preset transition by name.
        
        Args:
            preset_name: Name of preset transition
            
        Returns:
            Transition object or None if preset not found
        """
        presets = {
            'fade_in': self.create_transition(TransitionType.FADE, duration=1.0),
            'fade_out': self.create_transition(TransitionType.FADE, duration=1.0),
            'slide_left': self.create_transition(TransitionType.SLIDE, 
                                                direction=TransitionDirection.LEFT_TO_RIGHT),
            'slide_right': self.create_transition(TransitionType.SLIDE,
                                                 direction=TransitionDirection.RIGHT_TO_LEFT),
            'zoom_in': self.create_transition(TransitionType.ZOOM),
            'zoom_out': self.create_transition(TransitionType.ZOOM),
            'rotate_clockwise': self.create_transition(TransitionType.ROTATE),
            'scale_up': self.create_transition(TransitionType.SCALE),
            'wipe_left': self.create_transition(TransitionType.WIPE,
                                               direction=TransitionDirection.LEFT_TO_RIGHT),
            'bounce_in': self.create_transition(TransitionType.BOUNCE),
            'elastic_pop': self.create_transition(TransitionType.ELASTIC)
        }
        
        return presets.get(preset_name)
    
    def clear(self):
        """Clear all active transitions and callbacks."""
        self.active_transitions.clear()
        self.transition_callbacks.clear()
