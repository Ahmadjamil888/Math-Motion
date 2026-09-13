"""
Main Application Entry Point (Basic Version)
Math Motion - Mathematical Animation Studio
Runs without Manim for mathematical functionality only.
"""

import sys
import os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QObject, Signal

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.ui.main_window import MainWindow
from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator
from app.math.geometry import GeometryGenerator
from app.audio.loader import AudioLoader
from app.audio.beat_detection import BeatDetector
from app.audio.energy import EnergyAnalyzer
from app.audio.sync import AudioSync

# Try to import animation components, but handle gracefully
try:
    from app.animation.scene import MathScene, AnimationConfig
    from app.animation.timeline import AnimationTimeline
    from app.animation.transitions import TransitionManager
    from app.animation.effects import EffectManager
    from app.render.manim_renderer import ManimRenderer, RenderConfig
    from app.render.ffmpeg import FFmpegProcessor, FFmpegConfig
    ANIMATION_AVAILABLE = True
except ImportError:
    ANIMATION_AVAILABLE = False
    print("Note: Animation components not available (requires Manim + C++ Build Tools)")
    print("Mathematical and audio components will work without animation features.")


class ApplicationCore(QObject):
    """Core application logic connecting all components."""
    
    # Signals
    rendering_progress = Signal(str)
    rendering_complete = Signal(bool, str)
    preview_updated = Signal(object)
    
    def __init__(self):
        super().__init__()
        
        # Initialize components
        self.init_math_engine()
        self.init_audio_engine()
        
        # Initialize animation components only if available
        if ANIMATION_AVAILABLE:
            self.init_animation_engine()
            self.init_render_engine()
        
        # Application state
        self.current_formula = ""
        self.current_graph_data = None
        self.current_audio_data = None
        self.current_beat_info = None
        self.current_energy_info = None
        self.current_sync_timeline = None
    
    def init_math_engine(self):
        """Initialize mathematical components."""
        self.parser = FormulaParser()
        self.evaluator = FormulaEvaluator()
        self.geometry = GeometryGenerator()
    
    def init_audio_engine(self):
        """Initialize audio components."""
        self.audio_loader = AudioLoader()
        self.beat_detector = BeatDetector()
        self.energy_analyzer = EnergyAnalyzer()
        self.audio_sync = AudioSync()
    
    def init_animation_engine(self):
        """Initialize animation components."""
        self.animation_timeline = AnimationTimeline()
        self.transition_manager = TransitionManager()
        self.effect_manager = EffectManager()
    
    def init_render_engine(self):
        """Initialize rendering components."""
        self.manim_renderer = ManimRenderer()
        self.ffmpeg_processor = FFmpegProcessor()
    
    def process_formula(self, formula: str, domain_min: float = -10.0, 
                       domain_max: float = 10.0, num_points: int = 1000):
        """
        Process a mathematical formula.
        
        Args:
            formula: Mathematical formula string
            domain_min: Minimum domain value
            domain_max: Maximum domain value
            num_points: Number of points to evaluate
            
        Returns:
            Tuple of (x_values, y_values) or None if parsing fails
        """
        # Parse formula
        parsed_data = self.parser.parse_with_domain(formula, domain=(domain_min, domain_max))
        
        if parsed_data is None:
            return None
        
        # Evaluate formula
        x_values, y_values = self.evaluator.evaluate_range(
            parsed_data['expression'],
            parsed_data['domain'],
            num_points
        )
        
        # Generate geometry
        self.current_graph_data = self.geometry.generate_graph(
            x_values, y_values,
            variable=parsed_data['variable'],
            domain=parsed_data['domain']
        )
        
        self.current_formula = formula
        
        return x_values, y_values
    
    def load_audio(self, audio_path: str):
        """
        Load and analyze audio file.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load audio
            audio_data, sr = self.audio_loader.load_audio(audio_path)
            
            if len(audio_data) == 0:
                return False
            
            self.current_audio_data = audio_data
            
            # Detect beats
            self.current_beat_info = self.beat_detector.detect_beats(audio_data, sr)
            
            # Analyze energy
            self.current_energy_info = self.energy_analyzer.analyze_energy(audio_data, sr)
            
            # Create sync timeline
            self.audio_sync.load_audio_features(self.current_beat_info, self.current_energy_info)
            self.current_sync_timeline = self.audio_sync.create_combined_timeline(
                self.current_beat_info,
                self.current_energy_info
            )
            
            return True
        
        except Exception as e:
            print(f"Error loading audio: {e}")
            return False
    
    def render_animation(self, settings: dict) -> bool:
        """
        Render the complete animation.
        
        Args:
            settings: Dictionary of render settings
            
        Returns:
            True if successful, False otherwise
        """
        if not ANIMATION_AVAILABLE:
            self.rendering_progress.emit("Animation rendering not available (requires Manim)")
            self.rendering_complete.emit(False, "Manim not installed - requires C++ Build Tools")
            return False
        
        try:
            self.rendering_progress.emit("Starting render...")
            
            # Create render configuration
            anim_config = self.create_animation_config(settings)
            render_config = RenderConfig(
                resolution=anim_config.resolution,
                fps=anim_config.fps,
                background_color=anim_config.background_color
            )
            
            self.manim_renderer.config = render_config
            
            # Prepare sync events
            sync_events = []
            if self.current_sync_timeline:
                for event in self.current_sync_timeline.events:
                    sync_events.append({
                        'time': event.time,
                        'type': event.event_type,
                        'intensity': event.intensity,
                        'metadata': event.metadata
                    })
            
            self.rendering_progress.emit("Rendering animation...")
            
            # Render animation
            if sync_events:
                result = self.manim_renderer.render_synced_animation(
                    self.current_formula,
                    self.current_graph_data.x,
                    self.current_graph_data.y,
                    sync_events,
                    render_config
                )
            else:
                result = self.manim_renderer.render_formula_animation(
                    self.current_formula,
                    self.current_graph_data.x,
                    self.current_graph_data.y,
                    render_config
                )
            
            if not result.success:
                self.rendering_complete.emit(False, result.error_message or "Rendering failed")
                return False
            
            video_path = result.output_path
            self.rendering_progress.emit(f"Animation rendered: {video_path}")
            
            # Combine with audio if available
            if self.current_audio_data is not None and self.audio_loader.audio_path:
                self.rendering_progress.emit("Combining with audio...")
                
                output_path = settings.get('output_path', 'output/final_video.mp4')
                
                # Ensure output directory exists
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                
                combine_result = self.ffmpeg_processor.combine_video_audio(
                    video_path,
                    self.audio_loader.audio_path,
                    output_path
                )
                
                if combine_result.success:
                    self.rendering_progress.emit(f"Final video: {output_path}")
                    self.rendering_complete.emit(True, output_path)
                    return True
                else:
                    self.rendering_complete.emit(False, combine_result.error_message or "Audio combination failed")
                    return False
            else:
                # No audio, just copy the rendered video
                output_path = settings.get('output_path', 'output/final_video.mp4')
                os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
                
                import shutil
                shutil.copy(video_path, output_path)
                
                self.rendering_progress.emit(f"Final video: {output_path}")
                self.rendering_complete.emit(True, output_path)
                return True
        
        except Exception as e:
            self.rendering_complete.emit(False, str(e))
            return False
    
    def create_animation_config(self, settings: dict):
        """Create animation configuration from UI settings."""
        from app.animation.scene import AnimationConfig
        
        # Map resolution string to tuple
        resolution_map = {
            "720p": (1280, 720),
            "1080p": (1920, 1080),
            "1440p": (2560, 1440),
            "4K": (3840, 2160)
        }
        
        # Map FPS string to int
        fps_map = {
            "24 FPS": 24,
            "30 FPS": 30,
            "60 FPS": 60,
            "120 FPS": 120
        }
        
        resolution = resolution_map.get(settings.get('resolution', '1080p'), (1920, 1080))
        fps = fps_map.get(settings.get('fps', '60 FPS'), 60)
        
        # Map style to colors
        style_map = {
            0: {  # Minimal
                'background': '#ffffff',
                'line': '#000000',
                'axes': '#333333'
            },
            1: {  # Cinematic
                'background': '#1a1a2e',
                'line': '#00d4ff',
                'axes': '#ffffff'
            },
            2: {  # Neon
                'background': '#0a0a0a',
                'line': '#ff00ff',
                'axes': '#00ffff'
            },
            3: {  # Scientific
                'background': '#f8f9fa',
                'line': '#e74c3c',
                'axes': '#2c3e50'
            }
        }
        
        style = style_map.get(settings.get('style', 1), style_map[1])
        
        return AnimationConfig(
            resolution=resolution,
            fps=fps,
            background_color=style['background'],
            line_color=style['line'],
            axes_color=style['axes']
        )
    
    def get_audio_info(self) -> dict:
        """Get information about loaded audio."""
        if self.current_audio_data is None:
            return {}
        
        info = self.audio_loader.get_audio_info()
        
        if self.current_beat_info:
            info['tempo'] = self.current_beat_info.tempo
            info['beat_count'] = len(self.current_beat_info.beats)
        
        if self.current_energy_info:
            stats = self.energy_analyzer.get_energy_statistics(self.current_energy_info)
            info.update(stats)
        
        return info
    
    def get_sync_events(self) -> list:
        """Get synchronization events."""
        if self.current_sync_timeline is None:
            return []
        
        return [
            {
                'time': event.time,
                'type': event.event_type,
                'intensity': event.intensity
            }
            for event in self.current_sync_timeline.events
        ]
    
    def clear(self):
        """Clear all current data."""
        self.current_formula = ""
        self.current_graph_data = None
        self.current_audio_data = None
        self.current_beat_info = None
        self.current_energy_info = None
        self.current_sync_timeline = None
        
        self.audio_loader.clear()
        self.beat_detector.clear()
        self.energy_analyzer.clear()
        self.audio_sync.clear()
        
        if ANIMATION_AVAILABLE:
            self.animation_timeline.clear()


class MathMotionApp:
    """Main application class."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        # Set application properties
        self.app.setApplicationName("Math Motion")
        self.app.setApplicationVersion("0.1.0 (Basic)")
        self.app.setOrganizationName("Math Motion Studio")
        
        # Initialize core
        self.core = ApplicationCore()
        
        # Initialize main window
        self.main_window = MainWindow()
        
        # Update window title to reflect basic version
        if not ANIMATION_AVAILABLE:
            self.main_window.setWindowTitle("Math Motion (Basic - No Animation)")
        
        # Connect signals
        self.connect_signals()
    
    def connect_signals(self):
        """Connect application signals."""
        # Formula changes
        self.main_window.formula_changed.connect(self.on_formula_changed)
        
        # Music loading
        self.main_window.music_loaded.connect(self.on_music_loaded)
        
        # Render requests
        self.main_window.render_requested.connect(self.on_render_requested)
        
        # Core signals
        self.core.rendering_progress.connect(self.on_rendering_progress)
        self.core.rendering_complete.connect(self.on_rendering_complete)
    
    def on_formula_changed(self, formula: str):
        """Handle formula change from UI."""
        if not formula:
            return
        
        settings = self.main_window.get_current_settings()
        domain_min = settings.get('domain_min', -10.0)
        domain_max = settings.get('domain_max', 10.0)
        
        result = self.core.process_formula(formula, domain_min, domain_max)
        
        if result is not None:
            x_values, y_values = result
            self.main_window.preview_widget.set_graph_data(x_values, y_values)
            self.main_window.status_bar.showMessage(f"Formula processed: {formula}")
        else:
            self.main_window.status_bar.showMessage("Failed to process formula")
    
    def on_music_loaded(self, audio_path: str):
        """Handle music file loading."""
        success = self.core.load_audio(audio_path)
        
        if success:
            audio_info = self.core.get_audio_info()
            
            # Update UI with audio info
            info_text = f"Duration: {audio_info.get('duration', 0):.2f}s\n"
            info_text += f"Tempo: {audio_info.get('tempo', 0):.1f} BPM\n"
            info_text += f"Beats: {audio_info.get('beat_count', 0)}"
            
            self.main_window.audio_info_display.setText(info_text)
            
            # Update timeline with beat events
            sync_events = self.core.get_sync_events()
            for event in sync_events:
                self.main_window.timeline_widget.add_event(
                    event['time'],
                    event['type'],
                    {'intensity': event['intensity']}
                )
            
            # Set timeline duration
            duration = audio_info.get('duration', 10.0)
            self.main_window.timeline_widget.set_duration(duration)
            
            self.main_window.status_bar.showMessage("Audio loaded and analyzed")
        else:
            self.main_window.audio_info_display.setText("Failed to load audio")
            self.main_window.status_bar.showMessage("Failed to load audio file")
    
    def on_render_requested(self):
        """Handle render request from UI."""
        if not ANIMATION_AVAILABLE:
            self.main_window.status_bar.showMessage("Animation rendering not available (requires Manim)")
            return
        
        settings = self.main_window.get_current_settings()
        
        # Start rendering in a separate thread to avoid blocking UI
        def render_thread():
            success = self.core.render_animation(settings)
            # UI update happens via signals
        
        import threading
        render_thread_obj = threading.Thread(target=render_thread)
        render_thread_obj.daemon = True
        render_thread_obj.start()
    
    def on_rendering_progress(self, message: str):
        """Handle rendering progress updates."""
        self.main_window.status_bar.showMessage(message)
    
    def on_rendering_complete(self, success: bool, message: str):
        """Handle rendering completion."""
        self.main_window.set_rendering_complete(success)
        
        if success:
            self.main_window.status_bar.showMessage(f"Rendering complete: {message}")
        else:
            self.main_window.status_bar.showMessage(f"Rendering failed: {message}")
    
    def run(self):
        """Run the application."""
        self.main_window.show()
        return self.app.exec()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Math Motion - Mathematical Animation Studio")
    print("=" * 60)
    
    if ANIMATION_AVAILABLE:
        print("Full version with animation support")
    else:
        print("Basic version - Mathematical and audio features only")
        print("Animation rendering requires Manim + Microsoft Visual C++ Build Tools")
        print("See INSTALLATION_STATUS.md for details")
    
    print("=" * 60)
    
    app = MathMotionApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
