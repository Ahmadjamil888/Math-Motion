"""
Animation Timeline
Manages animation sequences and timing for mathematical animations.
"""

import numpy as np
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class AnimationType(Enum):
    """Types of animations."""
    DRAW_GRAPH = "draw_graph"
    TRANSFORM = "transform"
    ZOOM = "zoom"
    ROTATE = "rotate"
    SCALE = "scale"
    FADE_IN = "fade_in"
    FADE_OUT = "fade_out"
    PARTICLE_EFFECT = "particle_effect"
    GLOW_EFFECT = "glow_effect"
    BEAT_RESPONSE = "beat_response"
    ENERGY_RESPONSE = "energy_response"
    CUSTOM = "custom"


@dataclass
class AnimationKeyframe:
    """Keyframe for animation timeline."""
    time: float
    animation_type: AnimationType
    parameters: Dict
    duration: float = 1.0
    easing: str = "linear"


@dataclass
class AnimationLayer:
    """Layer for organizing animations."""
    name: str
    keyframes: List[AnimationKeyframe]
    enabled: bool = True
    opacity: float = 1.0


class AnimationTimeline:
    """Manages animation sequences and timing."""
    
    def __init__(self, duration: float = 10.0, fps: int = 60):
        self.duration = duration
        self.fps = fps
        self.layers: Dict[str, AnimationLayer] = {}
        self.current_time = 0.0
        self.total_frames = int(duration * fps)
        self.time_scale = 1.0
    
    def add_layer(self, name: str) -> AnimationLayer:
        """
        Add a new animation layer.
        
        Args:
            name: Name of the layer
            
        Returns:
            AnimationLayer object
        """
        layer = AnimationLayer(name=name, keyframes=[])
        self.layers[name] = layer
        return layer
    
    def add_keyframe(self, layer_name: str, keyframe: AnimationKeyframe):
        """
        Add a keyframe to a layer.
        
        Args:
            layer_name: Name of the layer
            keyframe: AnimationKeyframe to add
        """
        if layer_name not in self.layers:
            self.add_layer(layer_name)
        
        self.layers[layer_name].keyframes.append(keyframe)
        # Sort keyframes by time
        self.layers[layer_name].keyframes.sort(key=lambda k: k.time)
    
    def get_keyframes_at_time(self, time: float, layer_name: str = None) -> List[AnimationKeyframe]:
        """
        Get keyframes at a specific time.
        
        Args:
            time: Time in seconds
            layer_name: Optional layer name (None for all layers)
            
        Returns:
            List of keyframes at the given time
        """
        keyframes = []
        
        layers_to_search = [layer_name] if layer_name else self.layers.keys()
        
        for layer in layers_to_search:
            if layer in self.layers and self.layers[layer].enabled:
                for keyframe in self.layers[layer].keyframes:
                    if abs(keyframe.time - time) < 0.1:  # 100ms window
                        keyframes.append(keyframe)
        
        return keyframes
    
    def get_keyframes_in_range(self, start: float, end: float, 
                              layer_name: str = None) -> List[AnimationKeyframe]:
        """
        Get keyframes within a time range.
        
        Args:
            start: Start time in seconds
            end: End time in seconds
            layer_name: Optional layer name
            
        Returns:
            List of keyframes in the range
        """
        keyframes = []
        
        layers_to_search = [layer_name] if layer_name else self.layers.keys()
        
        for layer in layers_to_search:
            if layer in self.layers and self.layers[layer].enabled:
                for keyframe in self.layers[layer].keyframes:
                    if start <= keyframe.time <= end:
                        keyframes.append(keyframe)
        
        return keyframes
    
    def remove_keyframe(self, layer_name: str, time: float):
        """
        Remove keyframe at specific time from layer.
        
        Args:
            layer_name: Name of the layer
            time: Time of keyframe to remove
        """
        if layer_name in self.layers:
            self.layers[layer_name].keyframes = [
                k for k in self.layers[layer_name].keyframes 
                if abs(k.time - time) >= 0.1
            ]
    
    def clear_layer(self, layer_name: str):
        """Clear all keyframes from a layer."""
        if layer_name in self.layers:
            self.layers[layer_name].keyframes.clear()
    
    def remove_layer(self, layer_name: str):
        """Remove a layer entirely."""
        if layer_name in self.layers:
            del self.layers[layer_name]
    
    def set_layer_enabled(self, layer_name: str, enabled: bool):
        """Enable or disable a layer."""
        if layer_name in self.layers:
            self.layers[layer_name].enabled = enabled
    
    def set_layer_opacity(self, layer_name: str, opacity: float):
        """Set opacity of a layer."""
        if layer_name in self.layers:
            self.layers[layer_name].opacity = max(0.0, min(1.0, opacity))
    
    def get_timeline_summary(self) -> Dict:
        """
        Get summary of timeline structure.
        
        Returns:
            Dictionary with timeline information
        """
        summary = {
            'duration': self.duration,
            'fps': self.fps,
            'total_frames': self.total_frames,
            'layers': {}
        }
        
        for layer_name, layer in self.layers.items():
            summary['layers'][layer_name] = {
                'enabled': layer.enabled,
                'opacity': layer.opacity,
                'keyframe_count': len(layer.keyframes),
                'animation_types': list(set(kf.animation_type.value for kf in layer.keyframes))
            }
        
        return summary
    
    def optimize_timeline(self):
        """Optimize timeline by removing redundant keyframes."""
        for layer in self.layers.values():
            # Remove consecutive keyframes with same parameters
            optimized_keyframes = []
            
            for i, keyframe in enumerate(layer.keyframes):
                if i == 0:
                    optimized_keyframes.append(keyframe)
                else:
                    prev_keyframe = optimized_keyframes[-1]
                    if (keyframe.animation_type != prev_keyframe.animation_type or
                        keyframe.parameters != prev_keyframe.parameters):
                        optimized_keyframes.append(keyframe)
            
            layer.keyframes = optimized_keyframes
    
    def duplicate_layer(self, source_layer: str, target_layer: str):
        """
        Duplicate a layer.
        
        Args:
            source_layer: Name of layer to duplicate
            target_layer: Name of new layer
        """
        if source_layer in self.layers:
            source = self.layers[source_layer]
            new_layer = AnimationLayer(
                name=target_layer,
                keyframes=[AnimationKeyframe(kf.time, kf.animation_type, 
                                           kf.parameters.copy(), kf.duration, kf.easing)
                          for kf in source.keyframes],
                enabled=source.enabled,
                opacity=source.opacity
            )
            self.layers[target_layer] = new_layer
    
    def merge_layers(self, target_layer: str, source_layers: List[str]):
        """
        Merge multiple layers into one.
        
        Args:
            target_layer: Name of target layer
            source_layers: List of source layer names to merge
        """
        if target_layer not in self.layers:
            self.add_layer(target_layer)
        
        for source_layer in source_layers:
            if source_layer in self.layers:
                self.layers[target_layer].keyframes.extend(
                    self.layers[source_layer].keyframes
                )
        
        # Sort merged keyframes by time
        self.layers[target_layer].keyframes.sort(key=lambda k: k.time)
    
    def scale_timeline(self, scale_factor: float):
        """
        Scale the timeline duration and keyframe times.
        
        Args:
            scale_factor: Factor to scale timeline by
        """
        self.duration *= scale_factor
        self.total_frames = int(self.duration * self.fps)
        
        for layer in self.layers.values():
            for keyframe in layer.keyframes:
                keyframe.time *= scale_factor
                keyframe.duration *= scale_factor
    
    def offset_timeline(self, time_offset: float):
        """
        Offset all keyframe times.
        
        Args:
            time_offset: Time offset in seconds
        """
        for layer in self.layers.values():
            for keyframe in layer.keyframes:
                keyframe.time += time_offset
    
    def get_easing_function(self, easing: str) -> Callable:
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
            'bounce': lambda t: 1 - abs(np.cos(t * np.pi * 2) * np.exp(-t * 3)),
            'elastic': lambda t: t * t * ((t * 2 - 1) * (t * 2 - 3))
        }
        
        return easing_functions.get(easing, lambda t: t)
    
    def export_timeline(self, format: str = 'json') -> str:
        """
        Export timeline to format.
        
        Args:
            format: Export format ('json', 'dict')
            
        Returns:
            Timeline data as string or dict
        """
        data = {
            'duration': self.duration,
            'fps': self.fps,
            'layers': {}
        }
        
        for layer_name, layer in self.layers.items():
            data['layers'][layer_name] = {
                'enabled': layer.enabled,
                'opacity': layer.opacity,
                'keyframes': [
                    {
                        'time': kf.time,
                        'animation_type': kf.animation_type.value,
                        'parameters': kf.parameters,
                        'duration': kf.duration,
                        'easing': kf.easing
                    }
                    for kf in layer.keyframes
                ]
            }
        
        if format == 'json':
            import json
            return json.dumps(data, indent=2)
        elif format == 'dict':
            return data
        
        return str(data)
    
    def import_timeline(self, data: str, format: str = 'json'):
        """
        Import timeline from format.
        
        Args:
            data: Timeline data
            format: Import format ('json', 'dict')
        """
        if format == 'json':
            import json
            data = json.loads(data)
        
        self.duration = data.get('duration', 10.0)
        self.fps = data.get('fps', 60)
        self.total_frames = int(self.duration * self.fps)
        
        self.layers.clear()
        
        for layer_name, layer_data in data.get('layers', {}).items():
            layer = AnimationLayer(
                name=layer_name,
                keyframes=[
                    AnimationKeyframe(
                        time=kf['time'],
                        animation_type=AnimationType(kf['animation_type']),
                        parameters=kf['parameters'],
                        duration=kf.get('duration', 1.0),
                        easing=kf.get('easing', 'linear')
                    )
                    for kf in layer_data.get('keyframes', [])
                ],
                enabled=layer_data.get('enabled', True),
                opacity=layer_data.get('opacity', 1.0)
            )
            self.layers[layer_name] = layer
    
    def clear(self):
        """Clear all timeline data."""
        self.layers.clear()
        self.current_time = 0.0
