"""
Manim Renderer
Handles rendering of Manim scenes to video files.
"""

import subprocess
import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass
import numpy as np


@dataclass
class RenderConfig:
    """Configuration for Manim rendering."""
    resolution: tuple = (1920, 1080)
    fps: int = 60
    quality: str = "high"  # low, medium, high, ultra
    background_color: str = "#1a1a2e"
    output_format: str = "mp4"
    transparent: bool = False
    frame_rate: int = 60


@dataclass
class RenderResult:
    """Result of rendering operation."""
    success: bool
    output_path: Optional[str]
    duration: float
    frame_count: int
    error_message: Optional[str] = None


class ManimRenderer:
    """Handles Manim scene rendering."""
    
    def __init__(self, config: RenderConfig = None):
        if config is None:
            config = RenderConfig()
        
        self.config = config
        self.temp_dir = None
        self.current_scene = None
    
    def create_temp_directory(self) -> str:
        """Create a temporary directory for rendering."""
        self.temp_dir = tempfile.mkdtemp(prefix="manim_render_")
        return self.temp_dir
    
    def cleanup_temp_directory(self):
        """Clean up temporary directory."""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.temp_dir = None
    
    def generate_scene_file(self, scene_class: str, scene_code: str, 
                          output_dir: str) -> str:
        """
        Generate a Python file with the Manim scene.
        
        Args:
            scene_class: Name of the scene class
            scene_code: Python code for the scene
            output_dir: Directory to save the file
            
        Returns:
            Path to the generated scene file
        """
        scene_file = os.path.join(output_dir, f"{scene_class.lower()}.py")
        
        with open(scene_file, 'w') as f:
            f.write(scene_code)
        
        return scene_file
    
    def render_scene(self, scene_file: str, scene_name: str,
                    output_dir: str = None) -> RenderResult:
        """
        Render a Manim scene to video.
        
        Args:
            scene_file: Path to the scene Python file
            scene_name: Name of the scene class
            output_dir: Output directory for video
            
        Returns:
            RenderResult with rendering information
        """
        if output_dir is None:
            output_dir = os.getcwd()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Build manim command
        cmd = [
            "manim",
            scene_file,
            scene_name,
            "-ql",  # Quality level (l=low, m=medium, h=high, k=ultra)
            "--format", self.config.output_format,
            "--resolution", f"{self.config.resolution[0]},{self.config.resolution[1]}",
            "--frame_rate", str(self.config.fps),
            "-o", output_dir
        ]
        
        if self.config.transparent:
            cmd.append("--transparent")
        
        try:
            # Run manim command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Find the output file
                output_files = list(Path(output_dir).glob(f"{scene_name}.*.{self.config.output_format}"))
                if output_files:
                    output_path = str(output_files[0])
                    
                    # Get video info
                    duration, frame_count = self._get_video_info(output_path)
                    
                    return RenderResult(
                        success=True,
                        output_path=output_path,
                        duration=duration,
                        frame_count=frame_count
                    )
                else:
                    return RenderResult(
                        success=False,
                        output_path=None,
                        duration=0.0,
                        frame_count=0,
                        error_message="Output file not found"
                    )
            else:
                return RenderResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    frame_count=0,
                    error_message=result.stderr
                )
        
        except subprocess.TimeoutExpired:
            return RenderResult(
                success=False,
                output_path=None,
                duration=0.0,
                frame_count=0,
                error_message="Rendering timed out"
            )
        except Exception as e:
            return RenderResult(
                success=False,
                output_path=None,
                duration=0.0,
                frame_count=0,
                error_message=str(e)
            )
    
    def _get_video_info(self, video_path: str) -> tuple[float, int]:
        """
        Get video duration and frame count using ffprobe.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Tuple of (duration, frame_count)
        """
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-show_entries", "stream=nb_read_frames",
                "-of", "default=noprint_wrappers=1:nokey=1",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                duration = float(lines[0]) if len(lines) > 0 else 0.0
                frame_count = int(lines[1]) if len(lines) > 1 else 0
                return duration, frame_count
        
        except Exception:
            pass
        
        return 0.0, 0
    
    def render_formula_animation(self, formula: str, x_values: np.ndarray, 
                                y_values: np.ndarray, config: RenderConfig = None) -> RenderResult:
        """
        Render a formula animation.
        
        Args:
            formula: Mathematical formula string
            x_values: X coordinate array
            y_values: Y coordinate array
            config: Optional render configuration
            
        Returns:
            RenderResult with rendering information
        """
        if config:
            self.config = config
        
        # Create temporary directory
        temp_dir = self.create_temp_directory()
        
        try:
            # Generate scene code
            scene_code = self._generate_formula_scene_code(formula, x_values, y_values)
            
            # Write scene file
            scene_file = self.generate_scene_file("FormulaAnimationScene", scene_code, temp_dir)
            
            # Render the scene
            result = self.render_scene(scene_file, "FormulaAnimationScene", "output")
            
            return result
        
        finally:
            self.cleanup_temp_directory()
    
    def _generate_formula_scene_code(self, formula: str, x_values: np.ndarray, 
                                     y_values: np.ndarray) -> str:
        """Generate Python code for a formula animation scene."""
        
        # Convert arrays to string representation
        x_str = str(x_values.tolist())
        y_str = str(y_values.tolist())
        
        code = f'''
from manim import *
import numpy as np

class FormulaAnimationScene(Scene):
    def construct(self):
        # Setup
        self.camera.background_color = "{self.config.background_color}"
        
        # Create axes
        axes = Axes(
            x_range={self._get_range(x_values)},
            y_range={self._get_range(y_values)},
            axis_config={{
                "color": "{self.config.axes_color}",
                "stroke_width": 2,
                "include_tip": True,
            }}
        )
        
        # Add axis labels
        x_label = axes.get_x_axis_label(Tex("x").scale(0.7))
        y_label = axes.get_y_axis_label(Tex("y").scale(0.7))
        axes.add(x_label, y_label)
        
        self.play(Create(axes), run_time=1)
        
        # Add formula text
        formula_text = MathTex("{formula}").scale(0.8)
        formula_text.move_to(UP + RIGHT)
        self.play(Write(formula_text), run_time=1)
        
        # Plot the function
        x_vals = np.array({x_str})
        y_vals = np.array({y_str})
        
        graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=y_vals,
            line_color="{self.config.line_color}",
            stroke_width=2,
            add_vertex_dots=False
        )
        
        self.play(Create(graph), run_time=2)
        
        self.wait()
'''
        return code
    
    def _get_range(self, values: np.ndarray) -> tuple:
        """Get min/max range for array."""
        return (float(np.min(values)), float(np.max(values)))
    
    def render_synced_animation(self, formula: str, x_values: np.ndarray,
                               y_values: np.ndarray, sync_events: List[Dict],
                               config: RenderConfig = None) -> RenderResult:
        """
        Render animation with audio synchronization.
        
        Args:
            formula: Mathematical formula string
            x_values: X coordinate array
            y_values: Y coordinate array
            sync_events: List of synchronization events
            config: Optional render configuration
            
        Returns:
            RenderResult with rendering information
        """
        if config:
            self.config = config
        
        # Create temporary directory
        temp_dir = self.create_temp_directory()
        
        try:
            # Generate scene code with sync
            scene_code = self._generate_synced_scene_code(formula, x_values, y_values, sync_events)
            
            # Write scene file
            scene_file = self.generate_scene_file("SyncedAnimationScene", scene_code, temp_dir)
            
            # Render the scene
            result = self.render_scene(scene_file, "SyncedAnimationScene", "output")
            
            return result
        
        finally:
            self.cleanup_temp_directory()
    
    def _generate_synced_scene_code(self, formula: str, x_values: np.ndarray,
                                   y_values: np.ndarray, sync_events: List[Dict]) -> str:
        """Generate Python code for synced animation scene."""
        
        x_str = str(x_values.tolist())
        y_str = str(y_values.tolist())
        sync_str = str(sync_events)
        
        code = f'''
from manim import *
import numpy as np

class SyncedAnimationScene(Scene):
    def construct(self):
        # Setup
        self.camera.background_color = "{self.config.background_color}"
        
        # Create axes
        axes = Axes(
            x_range={self._get_range(x_values)},
            y_range={self._get_range(y_values)},
            axis_config={{
                "color": "{self.config.axes_color}",
                "stroke_width": 2,
                "include_tip": True,
            }}
        )
        
        self.play(Create(axes), run_time=1)
        
        # Add formula text
        formula_text = MathTex("{formula}").scale(0.8)
        formula_text.move_to(UP + RIGHT)
        self.play(Write(formula_text), run_time=1)
        
        # Plot the function
        x_vals = np.array({x_str})
        y_vals = np.array({y_str})
        
        graph = axes.plot_line_graph(
            x_values=x_vals,
            y_values=y_vals,
            line_color="{self.config.line_color}",
            stroke_width=2,
            add_vertex_dots=False
        )
        
        self.play(Create(graph), run_time=2)
        
        # Process sync events
        sync_events = {sync_str}
        
        for event in sync_events:
            self.wait_until(lambda: self.renderer.time >= event["time"])
            
            if event["type"] == "beat":
                self.play(graph.animate.scale(1.1), run_time=0.1)
                self.play(graph.animate.scale(0.909), run_time=0.1)
            elif event["type"] == "energy":
                intensity = event.get("intensity", 0.5)
                if intensity > 0.7:
                    self.play(graph.animate.set_color(RED), run_time=0.2)
                else:
                    self.play(graph.animate.set_color("{self.config.line_color}"), run_time=0.2)
        
        self.wait()
'''
        return code
    
    def set_quality(self, quality: str):
        """
        Set render quality.
        
        Args:
            quality: Quality level ('low', 'medium', 'high', 'ultra')
        """
        quality_map = {
            'low': 'l',
            'medium': 'm',
            'high': 'h',
            'ultra': 'k'
        }
        self.config.quality = quality
    
    def get_quality_flag(self) -> str:
        """Get manim quality flag."""
        quality_map = {
            'low': '-ql',
            'medium': '-qm',
            'high': '-qh',
            'ultra': '-qk'
        }
        return quality_map.get(self.config.quality, '-qh')
    
    def clear(self):
        """Clear renderer state."""
        self.cleanup_temp_directory()
        self.current_scene = None
