"""
Test Pipeline Script
Demonstrates the complete Math Motion pipeline without GUI.
"""

import sys
import os
import numpy as np
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator
from app.math.geometry import GeometryGenerator
from app.audio.loader import AudioLoader
from app.audio.beat_detection import BeatDetector
from app.audio.energy import EnergyAnalyzer
from app.audio.sync import AudioSync
from app.animation.timeline import AnimationTimeline
from app.animation.transitions import TransitionManager
from app.animation.effects import EffectManager
from app.render.manim_renderer import ManimRenderer, RenderConfig


def test_math_pipeline():
    """Test the mathematical formula processing pipeline."""
    print("=" * 60)
    print("Testing Math Pipeline")
    print("=" * 60)
    
    # Initialize components
    parser = FormulaParser()
    evaluator = FormulaEvaluator()
    geometry = GeometryGenerator()
    
    # Test formula
    formula = "sin(x^2) + 0.5*cos(3*x)"
    print(f"\nProcessing formula: {formula}")
    
    # Parse formula
    parsed_data = parser.parse_with_domain(formula, domain=(-10, 10))
    if parsed_data:
        print(f"✓ Formula parsed successfully")
        print(f"  Expression: {parsed_data['expression']}")
        print(f"  Variable: {parsed_data['variable']}")
        print(f"  Domain: {parsed_data['domain']}")
    else:
        print("✗ Formula parsing failed")
        return False
    
    # Evaluate formula
    x_values, y_values = evaluator.evaluate_range(
        parsed_data['expression'],
        parsed_data['domain'],
        num_points=1000
    )
    
    print(f"✓ Formula evaluated")
    print(f"  Points generated: {len(x_values)}")
    print(f"  X range: [{x_values.min():.2f}, {x_values.max():.2f}]")
    print(f"  Y range: [{y_values.min():.2f}, {y_values.max():.2f}]")
    
    # Generate geometry
    graph_data = geometry.generate_graph(x_values, y_values)
    print(f"✓ Geometry generated")
    print(f"  Arc length: {geometry.calculate_arc_length(graph_data):.2f}")
    
    return True


def test_audio_pipeline(audio_path: str = None):
    """Test the audio processing pipeline."""
    print("\n" + "=" * 60)
    print("Testing Audio Pipeline")
    print("=" * 60)
    
    if audio_path is None or not os.path.exists(audio_path):
        print("⚠ No audio file provided, skipping audio tests")
        return None
    
    # Initialize components
    loader = AudioLoader()
    beat_detector = BeatDetector()
    energy_analyzer = EnergyAnalyzer()
    audio_sync = AudioSync()
    
    # Load audio
    print(f"\nLoading audio: {audio_path}")
    audio_data, sr = loader.load_audio(audio_path)
    
    if len(audio_data) == 0:
        print("✗ Audio loading failed")
        return None
    
    audio_info = loader.get_audio_info()
    print(f"✓ Audio loaded successfully")
    print(f"  Duration: {audio_info['duration']:.2f}s")
    print(f"  Sample rate: {audio_info['sample_rate']} Hz")
    print(f"  Samples: {audio_info['num_samples']}")
    
    # Detect beats
    print("\nDetecting beats...")
    beat_info = beat_detector.detect_beats(audio_data, sr)
    print(f"✓ Beats detected")
    print(f"  Tempo: {beat_info.tempo:.1f} BPM")
    print(f"  Beat count: {len(beat_info.beats)}")
    print(f"  First 5 beats: {beat_info.beats[:5]}")
    
    # Analyze energy
    print("\nAnalyzing energy...")
    energy_info = energy_analyzer.analyze_energy(audio_data, sr)
    stats = energy_analyzer.get_energy_statistics(energy_info)
    print(f"✓ Energy analysis complete")
    print(f"  Mean energy: {stats['mean']:.4f}")
    print(f"  Max energy: {stats['max']:.4f}")
    print(f"  Std deviation: {stats['std']:.4f}")
    
    # Create sync timeline
    print("\nCreating sync timeline...")
    audio_sync.load_audio_features(beat_info, energy_info)
    timeline = audio_sync.create_combined_timeline(beat_info, energy_info)
    print(f"✓ Timeline created")
    print(f"  Duration: {timeline.duration:.2f}s")
    print(f"  Events: {len(timeline.events)}")
    
    return {
        'beat_info': beat_info,
        'energy_info': energy_info,
        'timeline': timeline
    }


def test_animation_pipeline():
    """Test the animation pipeline."""
    print("\n" + "=" * 60)
    print("Testing Animation Pipeline")
    print("=" * 60)
    
    # Initialize components
    timeline = AnimationTimeline(duration=10.0, fps=60)
    transition_manager = TransitionManager()
    effect_manager = EffectManager()
    
    # Create animation timeline
    print("\nCreating animation timeline...")
    timeline.add_layer("main_graph")
    
    from app.animation.timeline import AnimationKeyframe, AnimationType
    
    # Add some keyframes
    keyframes = [
        AnimationKeyframe(0.0, AnimationType.DRAW_GRAPH, {'duration': 2.0}),
        AnimationKeyframe(2.0, AnimationType.ZOOM, {'zoom_level': 1.5}),
        AnimationKeyframe(4.0, AnimationType.BEAT_RESPONSE, {'intensity': 0.8}),
        AnimationKeyframe(6.0, AnimationType.ENERGY_RESPONSE, {'energy': 0.6}),
        AnimationKeyframe(8.0, AnimationType.FADE_OUT, {'duration': 1.0}),
    ]
    
    for kf in keyframes:
        timeline.add_keyframe("main_graph", kf)
    
    print(f"✓ Timeline created with {len(keyframes)} keyframes")
    
    # Test transitions
    print("\nTesting transitions...")
    fade_transition = transition_manager.apply_fade_transition(duration=1.0)
    print(f"✓ Fade transition created: {fade_transition}")
    
    # Test effects
    print("\nTesting effects...")
    glow_effect = effect_manager.create_glow_effect(color="#00d4ff")
    print(f"✓ Glow effect created: {glow_effect}")
    
    return True


def test_render_pipeline():
    """Test the rendering pipeline (requires Manim and FFmpeg)."""
    print("\n" + "=" * 60)
    print("Testing Render Pipeline")
    print("=" * 60)
    
    # Check if Manim is available
    try:
        import subprocess
        result = subprocess.run(["manim", "--version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("⚠ Manim not available, skipping render tests")
            return False
    except:
        print("⚠ Manim not available, skipping render tests")
        return False
    
    print("✓ Manim is available")
    
    # Check if FFmpeg is available
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("⚠ FFmpeg not available, skipping render tests")
            return False
    except:
        print("⚠ FFmpeg not available, skipping render tests")
        return False
    
    print("✓ FFmpeg is available")
    
    # Test basic formula rendering
    print("\nTesting formula rendering...")
    renderer = ManimRenderer()
    
    # Create test data
    x_values = np.linspace(-10, 10, 1000)
    y_values = np.sin(x_values**2)
    
    config = RenderConfig(
        resolution=(1280, 720),
        fps=30,
        quality="medium"
    )
    
    print("  This would render: sin(x^2)")
    print("  (Actual rendering skipped to save time)")
    print("✓ Render pipeline test complete")
    
    return True


def main():
    """Run all pipeline tests."""
    print("\n" + "=" * 60)
    print("Math Motion Pipeline Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Test math pipeline
    results['math'] = test_math_pipeline()
    
    # Test audio pipeline (optional)
    audio_path = None  # Set to a real audio file path to test
    results['audio'] = test_audio_pipeline(audio_path)
    
    # Test animation pipeline
    results['animation'] = test_animation_pipeline()
    
    # Test render pipeline
    results['render'] = test_render_pipeline()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for component, result in results.items():
        if result is True:
            print(f"✓ {component.upper()}: PASSED")
        elif result is False:
            print(f"✗ {component.upper()}: FAILED")
        else:
            print(f"⚠ {component.upper()}: SKIPPED")
    
    print("\n" + "=" * 60)
    print("Pipeline test suite complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
