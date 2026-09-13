"""
Math Scene
Core Manim scene for mathematical animations.
"""

from manim import *
import numpy as np
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass


@dataclass
class AnimationConfig:
    """Configuration for animation parameters."""
    resolution: tuple = (1920, 1080)
    fps: int = 60
    background_color: str = '#1a1a2e'
    line_color: str = '#00d4ff'
    axes_color: str = '#ffffff'
    font_size: float = 48.0


class MathScene(Scene):
    """Main scene for mathematical animations with audio synchronization."""
    
    def __init__(self, config: AnimationConfig = None, **kwargs):
        if config is None:
            config = AnimationConfig()
        
        self.config = config
        self.graph_data = None
        self.sync_events = []
        self.sync_callback = None
        
        # Configure Manim scene
        kwargs['camera_config'] = {
            'frame_size': config.resolution,
            'frame_rate': config.fps
        }
        
        super().__init__(**kwargs)
    
    def setup(self):
        """Setup the scene with default elements."""
        # Set background color
        self.camera.background_color = parse_color(self.config.background_color)
    
    def construct_axes(self, x_range: tuple = (-10, 10), y_range: tuple = (-5, 5)):
        """
        Create and display coordinate axes.
        
        Args:
            x_range: X-axis range (min, max)
            y_range: Y-axis range (min, max)
            
        Returns:
            Axes object
        """
        axes = Axes(
            x_range=x_range,
            y_range=y_range,
            axis_config={
                "color": self.config.axes_color,
                "stroke_width": 2,
                "include_tip": True,
            }
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label(Tex("x").scale(0.7))
        y_label = axes.get_y_axis_label(Tex("y").scale(0.7))
        
        axes.add(x_label, y_label)
        self.play(Create(axes), run_time=1)
        
        return axes
    
    def plot_function(self, axes: Axes, x_values: np.ndarray, y_values: np.ndarray,
                     color: str = None, line_width: float = 2.0,
                     animate: bool = True) -> Graph:
        """
        Plot a mathematical function on the axes.
        
        Args:
            axes: Axes object
            x_values: Array of x coordinates
            y_values: Array of y coordinates
            color: Line color (default from config)
            line_width: Width of the line
            animate: Whether to animate the drawing
            
        Returns:
            Graph object
        """
        if color is None:
            color = self.config.line_color
        
        # Create the graph
        graph = axes.plot_line_graph(
            x_values=x_values,
            y_values=y_values,
            line_color=color,
            stroke_width=line_width,
            add_vertex_dots=False
        )
        
        if animate:
            self.play(Create(graph), run_time=2)
        else:
            self.add(graph)
        
        return graph
    
    def animate_function_drawing(self, axes: Axes, x_values: np.ndarray, y_values: np.ndarray,
                                duration: float = 3.0, color: str = None) -> Graph:
        """
        Animate the drawing of a function over time.
        
        Args:
            axes: Axes object
            x_values: Array of x coordinates
            y_values: Array of y coordinates
            duration: Duration of animation in seconds
            color: Line color
            
        Returns:
            Graph object
        """
        if color is None:
            color = self.config.line_color
        
        # Create partial graphs for animation
        total_points = len(x_values)
        points_per_frame = max(1, int(total_points / (duration * self.camera.frame_rate)))
        
        graphs = []
        for i in range(points_per_frame, total_points + 1, points_per_frame):
            partial_graph = axes.plot_line_graph(
                x_values=x_values[:i],
                y_values=y_values[:i],
                line_color=color,
                stroke_width=2,
                add_vertex_dots=False
            )
            graphs.append(partial_graph)
        
        # Animate the drawing
        self.play(*[Create(g) for g in graphs], run_time=duration, rate_func=linear)
        
        return graphs[-1] if graphs else None
    
    def add_formula_text(self, formula: str, position: UP + RIGHT, 
                        scale: float = 0.8) -> MathTex:
        """
        Add mathematical formula as text.
        
        Args:
            formula: LaTeX formula string
            position: Position on screen
            scale: Scale factor
            
        Returns:
            MathTex object
        """
        formula_text = MathTex(formula).scale(scale)
        formula_text.move_to(position)
        self.play(Write(formula_text), run_time=1)
        return formula_text
    
    def apply_beat_effect(self, mobject: Mobject, intensity: float = 0.5):
        """
        Apply a beat-based effect to a mobject.
        
        Args:
            mobject: Mobject to apply effect to
            intensity: Intensity of the effect (0.0 to 1.0)
        """
        # Scale effect based on intensity
        scale_factor = 1.0 + intensity * 0.1
        self.play(
            mobject.animate.scale(scale_factor),
            run_time=0.1,
            rate_func=there_and_back
        )
    
    def apply_energy_effect(self, mobject: Mobject, energy: float = 0.5):
        """
        Apply an energy-based effect to a mobject.
        
        Args:
            mobject: Mobject to apply effect to
            energy: Energy level (0.0 to 1.0)
        """
        # Color shift based on energy
        if energy > 0.7:
            color = RED
        elif energy > 0.4:
            color = YELLOW
        else:
            color = self.config.line_color
        
        self.play(
            mobject.animate.set_color(color),
            run_time=0.2
        )
    
    def zoom_to_point(self, axes: Axes, x_center: float, y_center: float,
                     zoom_level: float = 1.5, duration: float = 1.0):
        """
        Zoom the camera to a specific point.
        
        Args:
            axes: Axes object
            x_center: X coordinate to center on
            y_center: Y coordinate to center on
            zoom_level: Zoom factor
            duration: Duration of zoom
        """
        # Manim doesn't have direct zoom, so we simulate it by scaling
        zoom_animation = axes.animate.scale(zoom_level)
        self.play(zoom_animation, run_time=duration)
    
    def create_particles(self, count: int = 50, center: np.ndarray = ORIGIN) -> List[Dot]:
        """
        Create particle effects.
        
        Args:
            count: Number of particles
            center: Center point for particles
            
        Returns:
            List of particle objects
        """
        particles = []
        for _ in range(count):
            # Random position around center
            offset = np.random.uniform(-2, 2, 3)
            particle = Dot(point=center + offset, radius=0.05, color=YELLOW)
            particles.append(particle)
        
        return particles
    
    def animate_particles(self, particles: List[Dot], duration: float = 1.0):
        """
        Animate particles exploding outward.
        
        Args:
            particles: List of particle objects
            duration: Duration of animation
        """
        animations = []
        for particle in particles:
            # Random direction
            direction = np.random.uniform(-1, 1, 3)
            direction = direction / np.linalg.norm(direction) * 2
            
            animations.append(particle.animate.shift(direction))
        
        self.play(*animations, run_time=duration)
    
    def create_glow_effect(self, mobject: Mobject, glow_color: str = '#00d4ff') -> Mobject:
        """
        Create a glow effect around a mobject.
        
        Args:
            mobject: Mobject to add glow to
            glow_color: Color of the glow
            
        Returns:
            Glow mobject
        """
        glow = mobject.copy()
        glow.set_stroke(width=10, color=glow_color, opacity=0.3)
        glow.z_index = mobject.z_index - 1
        self.add(glow)
        return glow
    
    def animate_transform(self, from_mobject: Mobject, to_mobject: Mobject,
                        duration: float = 1.0):
        """
        Transform one mobject into another.
        
        Args:
            from_mobject: Source mobject
            to_mobject: Target mobject
            duration: Duration of transformation
        """
        self.play(Transform(from_mobject, to_mobject), run_time=duration)
    
    def create_fade_in(self, mobject: Mobject, duration: float = 1.0):
        """
        Fade in a mobject.
        
        Args:
            mobject: Mobject to fade in
            duration: Duration of fade
        """
        mobject.set_opacity(0)
        self.play(mobject.animate.set_opacity(1), run_time=duration)
    
    def create_fade_out(self, mobject: Mobject, duration: float = 1.0):
        """
        Fade out a mobject.
        
        Args:
            mobject: Mobject to fade out
            duration: Duration of fade
        """
        self.play(mobject.animate.set_opacity(0), run_time=duration)
    
    def set_sync_callback(self, callback: Callable):
        """
        Set callback for audio synchronization.
        
        Args:
            callback: Function to call on sync events
        """
        self.sync_callback = callback
    
    def process_sync_events(self, current_time: float):
        """
        Process synchronization events for current time.
        
        Args:
            current_time: Current animation time in seconds
        """
        if self.sync_callback:
            self.sync_callback(current_time)
    
    def render_with_audio_sync(self, sync_events: List[Dict], 
                              total_duration: float):
        """
        Render scene with audio synchronization.
        
        Args:
            sync_events: List of sync event dictionaries
            total_duration: Total duration of animation
        """
        self.sync_events = sync_events
        
        # Calculate frames
        total_frames = int(total_duration * self.camera.frame_rate)
        
        for frame in range(total_frames):
            current_time = frame / self.camera.frame_rate
            
            # Process sync events for this time
            self.process_sync_events(current_time)
            
            # Render frame
            self.render_frame()
    
    def render_frame(self):
        """Render a single frame (placeholder for actual rendering)."""
        # This would be called by Manim's render loop
        pass


class FormulaAnimationScene(MathScene):
    """Specialized scene for formula animations."""
    
    def __init__(self, formula: str, x_values: np.ndarray, y_values: np.ndarray,
                 config: AnimationConfig = None, **kwargs):
        self.formula = formula
        self.x_values = x_values
        self.y_values = y_values
        super().__init__(config, **kwargs)
    
    def construct(self):
        """Construct the formula animation."""
        # Setup axes
        axes = self.construct_axes()
        
        # Add formula text
        self.add_formula_text(self.formula, UP + RIGHT)
        
        # Animate function drawing
        graph = self.animate_function_drawing(axes, self.x_values, self.y_values)
        
        # Wait for sync events
        self.wait()
