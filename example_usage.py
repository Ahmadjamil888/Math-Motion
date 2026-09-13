"""
Example Usage Script
Demonstrates how to use Math Motion components programmatically.
"""

import numpy as np
from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator
from app.math.geometry import GeometryGenerator
from app.animation.timeline import AnimationTimeline, AnimationKeyframe, AnimationType


def example_formula_processing():
    """Example: Process a mathematical formula."""
    print("Example: Formula Processing")
    print("-" * 40)
    
    # Initialize components
    parser = FormulaParser()
    evaluator = FormulaEvaluator()
    geometry = GeometryGenerator()
    
    # Define a formula
    formula = "sin(x^2) + 0.5*cos(3*x)"
    print(f"Formula: {formula}")
    
    # Parse the formula
    parsed_data = parser.parse_with_domain(formula, domain=(-10, 10))
    if parsed_data:
        print(f"Parsed successfully: {parsed_data['expression']}")
        
        # Evaluate the formula
        x_values, y_values = evaluator.evaluate_range(
            parsed_data['expression'],
            parsed_data['domain'],
            num_points=1000
        )
        
        print(f"Generated {len(x_values)} points")
        print(f"X range: [{x_values.min():.2f}, {x_values.max():.2f}]")
        print(f"Y range: [{y_values.min():.2f}, {y_values.max():.2f}]")
        
        # Generate geometry
        graph_data = geometry.generate_graph(x_values, y_values)
        arc_length = geometry.calculate_arc_length(graph_data)
        print(f"Arc length: {arc_length:.2f}")
        
        return graph_data
    else:
        print("Failed to parse formula")
        return None


def example_animation_timeline():
    """Example: Create an animation timeline."""
    print("\nExample: Animation Timeline")
    print("-" * 40)
    
    # Create timeline
    timeline = AnimationTimeline(duration=10.0, fps=60)
    
    # Add layers
    main_layer = timeline.add_layer("main_graph")
    effects_layer = timeline.add_layer("effects")
    
    # Add keyframes to main layer
    keyframes = [
        AnimationKeyframe(0.0, AnimationType.DRAW_GRAPH, {'duration': 2.0}),
        AnimationKeyframe(2.0, AnimationType.ZOOM, {'zoom_level': 1.5}),
        AnimationKeyframe(4.0, AnimationType.ROTATE, {'angle': 45}),
        AnimationKeyframe(6.0, AnimationType.TRANSFORM, {'target': 'new_graph'}),
        AnimationKeyframe(8.0, AnimationType.FADE_OUT, {'duration': 1.0}),
    ]
    
    for kf in keyframes:
        timeline.add_keyframe("main_graph", kf)
    
    # Add keyframes to effects layer
    effect_keyframes = [
        AnimationKeyframe(1.0, AnimationType.GLOW, {'intensity': 0.5}),
        AnimationKeyframe(3.0, AnimationType.PARTICLE_EFFECT, {'count': 50}),
        AnimationKeyframe(5.0, AnimationType.PULSE, {'speed': 2.0}),
    ]
    
    for kf in effect_keyframes:
        timeline.add_keyframe("effects", kf)
    
    # Get timeline summary
    summary = timeline.get_timeline_summary()
    print(f"Timeline duration: {summary['duration']}s")
    print(f"Total frames: {summary['total_frames']}")
    print(f"Layers: {list(summary['layers'].keys())}")
    
    for layer_name, layer_info in summary['layers'].items():
        print(f"  {layer_name}: {layer_info['keyframe_count']} keyframes")
    
    # Get keyframes at specific time
    events_at_2s = timeline.get_keyframes_at_time(2.0)
    print(f"\nEvents at 2.0s: {len(events_at_2s)}")
    for event in events_at_2s:
        print(f"  - {event.animation_type.value}: {event.parameters}")
    
    return timeline


def example_geometry_transformations():
    """Example: Apply geometric transformations."""
    print("\nExample: Geometry Transformations")
    print("-" * 40)
    
    # Create sample graph data
    x_values = np.linspace(-5, 5, 100)
    y_values = x_values**2
    
    from app.math.geometry import GraphData
    graph_data = GraphData(x=x_values, y=y_values, domain=(-5, 5))
    
    print(f"Original graph: {len(x_values)} points")
    print(f"Original bounds: {graph_data.get_bounds()}")
    
    geometry = GeometryGenerator()
    
    # Scale transformation
    scaled_graph = geometry.scale_graph(graph_data, scale_x=2.0, scale_y=0.5)
    print(f"\nScaled (2x, 0.5y): {scaled_graph.get_bounds()}")
    
    # Translation
    translated_graph = geometry.translate_graph(graph_data, dx=1.0, dy=-2.0)
    print(f"Translated (1, -2): {translated_graph.get_bounds()}")
    
    # Rotation
    rotated_graph = geometry.rotate_graph(graph_data, angle=np.pi/4)  # 45 degrees
    print(f"Rotated (45°): {rotated_graph.get_bounds()}")
    
    return graph_data


def example_formula_evaluation():
    """Example: Advanced formula evaluation."""
    print("\nExample: Advanced Formula Evaluation")
    print("-" * 40)
    
    parser = FormulaParser()
    evaluator = FormulaEvaluator()
    
    formula = "x**3 - 3*x"
    print(f"Formula: {formula}")
    
    parsed_data = parser.parse_with_domain(formula, domain=(-5, 5))
    if parsed_data:
        expr = parsed_data['expression']
        
        # Calculate derivative
        derivative = evaluator.derivative(expr)
        print(f"First derivative: {derivative}")
        
        # Calculate second derivative
        second_derivative = evaluator.derivative(expr, order=2)
        print(f"Second derivative: {second_derivative}")
        
        # Find roots
        roots = evaluator.find_roots(expr, domain=(-5, 5))
        print(f"Roots in domain: {roots}")
        
        # Simplify expression
        simplified = evaluator.simplify_expression(expr)
        print(f"Simplified: {simplified}")


def example_parameterized_functions():
    """Example: Work with parameterized mathematical functions."""
    print("\nExample: Parameterized Functions")
    print("-" * 40)
    
    from app.math.functions import MathFunctions
    
    math_funcs = MathFunctions()
    
    # Get common functions
    functions = math_funcs.get_common_functions()
    print(f"Available functions: {list(functions.keys())}")
    
    # Get example formulas
    examples = math_funcs.get_function_examples()
    print(f"\nExample formulas:")
    for i, example in enumerate(examples[:5], 1):
        print(f"  {i}. {example}")
    
    # Test safe evaluation
    sin_func = functions['sin']
    result = math_funcs.safe_evaluate(sin_func, np.pi/2)
    print(f"\nsin(π/2) = {result:.4f}")
    
    # Test data normalization
    data = np.array([1, 2, 3, 4, 5])
    normalized = math_funcs.normalize_array(data, target_min=0.0, target_max=1.0)
    print(f"Original: {data}")
    print(f"Normalized: {normalized}")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Math Motion Example Usage")
    print("=" * 60)
    
    # Run examples
    example_formula_processing()
    example_animation_timeline()
    example_geometry_transformations()
    example_formula_evaluation()
    example_parameterized_functions()
    
    print("\n" + "=" * 60)
    print("Examples completed!")
    print("=" * 60)
    print("\nTo run the full application:")
    print("  python app/main.py")
    print("\nTo test the pipeline:")
    print("  python test_pipeline.py")


if __name__ == "__main__":
    main()
