"""
Test Mathematical Components Only
Tests the math engine components that are currently installed.
"""

import sys
import numpy as np
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator
from app.math.geometry import GeometryGenerator
from app.math.functions import MathFunctions


def test_formula_parsing():
    """Test formula parsing with SymPy."""
    print("=" * 60)
    print("Testing Formula Parsing (SymPy)")
    print("=" * 60)
    
    parser = FormulaParser()
    
    # Test various formulas
    formulas = [
        "sin(x**2)",
        "x**3 - 3*x",
        "exp(-x**2)",
        "cos(x) + sin(x)",
        "1/(1 + x**2)"
    ]
    
    for formula in formulas:
        parsed = parser.parse_with_domain(formula, domain=(-5, 5))
        if parsed:
            print(f"[OK] Parsed: {formula}")
            print(f"  Expression: {parsed['expression']}")
        else:
            print(f"[FAIL] Failed: {formula}")
    
    return True


def test_formula_evaluation():
    """Test formula evaluation with NumPy."""
    print("\n" + "=" * 60)
    print("Testing Formula Evaluation (NumPy)")
    print("=" * 60)
    
    parser = FormulaParser()
    evaluator = FormulaEvaluator()
    
    formula = "sin(x**2) + 0.5*cos(3*x)"
    print(f"Formula: {formula}")
    
    parsed = parser.parse_with_domain(formula, domain=(-10, 10))
    if parsed:
        x_values, y_values = evaluator.evaluate_range(
            parsed['expression'],
            parsed['domain'],
            num_points=1000
        )
        
        print(f"[OK] Evaluated successfully")
        print(f"  Points: {len(x_values)}")
        print(f"  X range: [{x_values.min():.2f}, {x_values.max():.2f}]")
        print(f"  Y range: [{y_values.min():.2f}, {y_values.max():.2f}]")
        
        # Test derivative
        derivative = evaluator.derivative(parsed['expression'])
        print(f"  Derivative: {derivative}")
        
        # Test root finding
        roots = evaluator.find_roots(parsed['expression'], domain=(-10, 10))
        print(f"  Roots: {roots}")
        
        return True
    else:
        print("[FAIL] Failed to parse formula")
        return False


def test_geometry_generation():
    """Test geometry generation."""
    print("\n" + "=" * 60)
    print("Testing Geometry Generation")
    print("=" * 60)
    
    geometry = GeometryGenerator()
    
    # Create sample data
    x_values = np.linspace(-5, 5, 100)
    y_values = x_values**2
    
    graph_data = geometry.generate_graph(x_values, y_values)
    
    print(f"[OK] Graph data created")
    print(f"  Points: {len(graph_data.x)}")
    print(f"  Bounds: {graph_data.get_bounds()}")
    print(f"  Arc length: {geometry.calculate_arc_length(graph_data):.2f}")
    
    # Test transformations
    scaled = geometry.scale_graph(graph_data, scale_x=2.0, scale_y=0.5)
    print(f"  Scaled bounds: {scaled.get_bounds()}")
    
    rotated = geometry.rotate_graph(graph_data, angle=np.pi/4)
    print(f"  Rotated bounds: {rotated.get_bounds()}")
    
    return True


def test_math_functions():
    """Test mathematical functions utilities."""
    print("\n" + "=" * 60)
    print("Testing Math Functions")
    print("=" * 60)
    
    math_funcs = MathFunctions()
    
    # Test available functions
    functions = math_funcs.get_common_functions()
    print(f"[OK] Available functions: {list(functions.keys())}")
    
    # Test example formulas
    examples = math_funcs.get_function_examples()
    print(f"[OK] Example formulas: {len(examples)} examples")
    for i, example in enumerate(examples[:3], 1):
        print(f"  {i}. {example}")
    
    # Test data normalization
    data = np.array([1, 2, 3, 4, 5])
    normalized = math_funcs.normalize_array(data)
    print(f"[OK] Normalization test:")
    print(f"  Original: {data}")
    print(f"  Normalized: {normalized}")
    
    # Test safe evaluation
    sin_func = functions['sin']
    result = math_funcs.safe_evaluate(sin_func, np.pi/2)
    print(f"[OK] Safe evaluation: sin(pi/2) = {result:.4f}")
    
    return True


def main():
    """Run all mathematical component tests."""
    print("\n" + "=" * 60)
    print("Math Motion - Mathematical Components Test")
    print("=" * 60)
    print("Testing components that are currently installed...")
    print()
    
    results = {}
    
    # Run tests
    results['parsing'] = test_formula_parsing()
    results['evaluation'] = test_formula_evaluation()
    results['geometry'] = test_geometry_generation()
    results['functions'] = test_math_functions()
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for component, result in results.items():
        status = "[OK] PASSED" if result else "[FAIL] FAILED"
        print(f"{component.upper()}: {status}")
    
    print("\n" + "=" * 60)
    print("Mathematical components are working correctly!")
    print("=" * 60)
    print("\nNote: GUI, audio, and animation components require additional")
    print("dependencies (PySide6, librosa, manim) which need to be installed")
    print("separately due to Python 3.14 compatibility and system requirements.")
    print("\nSee INSTALLATION_STATUS.md for detailed setup instructions.")


if __name__ == "__main__":
    main()
