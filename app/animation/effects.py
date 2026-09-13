"""
Effect Manager
Manages visual effects for mathematical animations.
"""

import numpy as np
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum


class EffectType(Enum):
    """Types of visual effects."""
    GLOW = "glow"
    PARTICLE_EXPLOSION = "particle_explosion"
    TRAIL = "trail"
    PULSE = "pulse"
    SHADOW = "shadow"
    REFLECTION = "reflection"
    BLUR = "blur"
    CHROMATIC_ABERRATION = "chromatic_aberration"
    GLITCH = "glitch"
    WAVE = "wave"
    ROTATE_3D = "rotate_3d"
    PIXELATE = "pixelate"
    NEON = "neon"
    SMOKE = "smoke"


@dataclass
class Effect:
    """Effect configuration."""
    effect_type: EffectType
    intensity: float = 0.5
    duration: float = 1.0
    parameters: Dict = None


@dataclass
class Particle:
    """Single particle for particle effects."""
    position: np.ndarray
    velocity: np.ndarray
    lifetime: float
    size: float
    color: str = "#ffffff"


class EffectManager:
    """Manages visual effects for animations."""
    
    def __init__(self):
        self.active_effects: List[Effect] = []
        self.particles: List[Particle] = []
        self.effect_callbacks: Dict[str, Callable] = {}
        self.default_intensity = 0.5
        self.default_duration = 1.0
    
    def create_effect(self, effect_type: EffectType, 
                     intensity: float = None,
                     duration: float = None,
                     parameters: Dict = None) -> Effect:
        """
        Create an effect configuration.
        
        Args:
            effect_type: Type of effect
            intensity: Intensity of effect (0.0 to 1.0)
            duration: Duration in seconds
            parameters: Additional parameters
            
        Returns:
            Effect object
        """
        if intensity is None:
            intensity = self.default_intensity
        if duration is None:
            duration = self.default_duration
        if parameters is None:
            parameters = {}
        
        return Effect(
            effect_type=effect_type,
            intensity=intensity,
            duration=duration,
            parameters=parameters
        )
    
    def create_glow_effect(self, color: str = "#00d4ff", 
                          blur_radius: float = 10.0,
                          intensity: float = 0.5) -> Effect:
        """
        Create a glow effect.
        
        Args:
            color: Color of the glow
            blur_radius: Radius of blur
            intensity: Intensity of effect
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.GLOW,
            intensity=intensity,
            parameters={
                'color': color,
                'blur_radius': blur_radius
            }
        )
    
    def create_particle_explosion(self, particle_count: int = 50,
                                  spread: float = 2.0,
                                  colors: List[str] = None) -> Effect:
        """
        Create a particle explosion effect.
        
        Args:
            particle_count: Number of particles
            spread: Spread of particles
            colors: List of colors for particles
            
        Returns:
            Effect object
        """
        if colors is None:
            colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]
        
        return self.create_effect(
            EffectType.PARTICLE_EXPLOSION,
            parameters={
                'particle_count': particle_count,
                'spread': spread,
                'colors': colors
            }
        )
    
    def create_trail_effect(self, trail_length: int = 10,
                           fade_speed: float = 0.1,
                           color: str = "#ffffff") -> Effect:
        """
        Create a trail effect.
        
        Args:
            trail_length: Length of trail
            fade_speed: Speed of trail fade
            color: Color of trail
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.TRAIL,
            parameters={
                'trail_length': trail_length,
                'fade_speed': fade_speed,
                'color': color
            }
        )
    
    def create_pulse_effect(self, pulse_speed: float = 2.0,
                           min_scale: float = 0.9,
                           max_scale: float = 1.1) -> Effect:
        """
        Create a pulse effect.
        
        Args:
            pulse_speed: Speed of pulsing
            min_scale: Minimum scale factor
            max_scale: Maximum scale factor
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.PULSE,
            parameters={
                'pulse_speed': pulse_speed,
                'min_scale': min_scale,
                'max_scale': max_scale
            }
        )
    
    def create_shadow_effect(self, offset_x: float = 0.1,
                           offset_y: float = -0.1,
                           blur_radius: float = 5.0,
                           opacity: float = 0.3) -> Effect:
        """
        Create a shadow effect.
        
        Args:
            offset_x: X offset of shadow
            offset_y: Y offset of shadow
            blur_radius: Blur radius
            opacity: Shadow opacity
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.SHADOW,
            intensity=opacity,
            parameters={
                'offset_x': offset_x,
                'offset_y': offset_y,
                'blur_radius': blur_radius
            }
        )
    
    def create_neon_effect(self, color: str = "#00d4ff",
                          glow_intensity: float = 0.8,
                          line_width: float = 2.0) -> Effect:
        """
        Create a neon glow effect.
        
        Args:
            color: Neon color
            glow_intensity: Intensity of glow
            line_width: Width of neon line
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.NEON,
            intensity=glow_intensity,
            parameters={
                'color': color,
                'line_width': line_width
            }
        )
    
    def create_wave_effect(self, amplitude: float = 0.1,
                          frequency: float = 2.0,
                          speed: float = 1.0) -> Effect:
        """
        Create a wave distortion effect.
        
        Args:
            amplitude: Wave amplitude
            frequency: Wave frequency
            speed: Wave speed
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.WAVE,
            parameters={
                'amplitude': amplitude,
                'frequency': frequency,
                'speed': speed
            }
        )
    
    def create_glitch_effect(self, intensity: float = 0.3,
                           frequency: float = 0.5) -> Effect:
        """
        Create a glitch effect.
        
        Args:
            intensity: Intensity of glitch
            frequency: Frequency of glitch occurrence
            
        Returns:
            Effect object
        """
        return self.create_effect(
            EffectType.GLITCH,
            intensity=intensity,
            parameters={
                'frequency': frequency
            }
        )
    
    def spawn_particles(self, center: np.ndarray, count: int = 50,
                       spread: float = 2.0, colors: List[str] = None):
        """
        Spawn particles at a location.
        
        Args:
            center: Center position for particles
            count: Number of particles to spawn
            spread: Spread of particles
            colors: List of colors for particles
        """
        if colors is None:
            colors = ["#ffffff"]
        
        for _ in range(count):
            # Random position within spread
            offset = np.random.uniform(-spread, spread, 3)
            position = center + offset
            
            # Random velocity
            velocity = np.random.uniform(-1, 1, 3) * 2
            
            # Random lifetime
            lifetime = np.random.uniform(0.5, 2.0)
            
            # Random size
            size = np.random.uniform(0.02, 0.1)
            
            # Random color
            color = np.random.choice(colors)
            
            particle = Particle(
                position=position,
                velocity=velocity,
                lifetime=lifetime,
                size=size,
                color=color
            )
            
            self.particles.append(particle)
    
    def update_particles(self, dt: float) -> List[Particle]:
        """
        Update particle positions and remove dead particles.
        
        Args:
            dt: Time delta in seconds
            
        Returns:
            List of active particles
        """
        active_particles = []
        
        for particle in self.particles:
            # Update position
            particle.position += particle.velocity * dt
            
            # Update lifetime
            particle.lifetime -= dt
            
            # Add gravity
            particle.velocity[1] -= 9.8 * dt
            
            # Keep alive particles
            if particle.lifetime > 0:
                active_particles.append(particle)
        
        self.particles = active_particles
        return active_particles
    
    def apply_glow_to_mobject(self, mobject, color: str = "#00d4ff", 
                              blur_radius: float = 10.0):
        """
        Apply glow effect to a mobject.
        
        Args:
            mobject: Mobject to apply glow to
            color: Glow color
            blur_radius: Blur radius
        """
        # This would be implemented with Manim's glow capabilities
        # For now, this is a placeholder
        pass
    
    def apply_pulse_to_mobject(self, mobject, time: float, 
                              pulse_speed: float = 2.0,
                              min_scale: float = 0.9,
                              max_scale: float = 1.1):
        """
        Apply pulse effect to a mobject.
        
        Args:
            mobject: Mobject to apply pulse to
            time: Current time
            pulse_speed: Speed of pulsing
            min_scale: Minimum scale
            max_scale: Maximum scale
        """
        # Calculate scale based on sine wave
        scale = min_scale + (max_scale - min_scale) * (0.5 + 0.5 * np.sin(time * pulse_speed))
        mobject.scale(scale)
    
    def apply_wave_to_mobject(self, mobject, time: float,
                             amplitude: float = 0.1,
                             frequency: float = 2.0):
        """
        Apply wave distortion to a mobject.
        
        Args:
            mobject: Mobject to apply wave to
            time: Current time
            amplitude: Wave amplitude
            frequency: Wave frequency
        """
        # This would modify mobject points with wave distortion
        # For now, this is a placeholder
        pass
    
    def get_effect_intensity(self, effect: Effect, time: float) -> float:
        """
        Get intensity of an effect at a specific time.
        
        Args:
            effect: Effect to evaluate
            time: Current time
            
        Returns:
            Intensity value (0.0 to 1.0)
        """
        # Simple fade in/out based on duration
        if time < 0:
            return 0.0
        elif time > effect.duration:
            return 0.0
        else:
            # Linear fade in and out
            progress = time / effect.duration
            if progress < 0.5:
                return progress * 2 * effect.intensity
            else:
                return (1 - progress) * 2 * effect.intensity
    
    def register_effect_callback(self, effect_type: str, callback: Callable):
        """
        Register a callback for a specific effect type.
        
        Args:
            effect_type: Type of effect
            callback: Function to call when effect is applied
        """
        self.effect_callbacks[effect_type] = callback
    
    def execute_effect(self, effect: Effect, time: float):
        """
        Execute an effect at a specific time.
        
        Args:
            effect: Effect to execute
            time: Current time
        """
        # Call registered callback if exists
        if effect.effect_type.value in self.effect_callbacks:
            callback = self.effect_callbacks[effect.effect_type.value]
            callback(effect, time)
    
    def create_preset_effect(self, preset_name: str) -> Optional[Effect]:
        """
        Create a preset effect by name.
        
        Args:
            preset_name: Name of preset effect
            
        Returns:
            Effect object or None if preset not found
        """
        presets = {
            'neon_blue': self.create_neon_effect("#00d4ff"),
            'neon_red': self.create_neon_effect("#ff0000"),
            'neon_green': self.create_neon_effect("#00ff00"),
            'pulse_glow': self.create_pulse_effect(),
            'particle_burst': self.create_particle_explosion(),
            'trail_effect': self.create_trail_effect(),
            'shadow_soft': self.create_shadow_effect(),
            'wave_distortion': self.create_wave_effect(),
            'glitch_effect': self.create_glitch_effect()
        }
        
        return presets.get(preset_name)
    
    def clear_effects(self):
        """Clear all active effects."""
        self.active_effects.clear()
    
    def clear_particles(self):
        """Clear all particles."""
        self.particles.clear()
    
    def clear(self):
        """Clear all effects and particles."""
        self.clear_effects()
        self.clear_particles()
        self.effect_callbacks.clear()
