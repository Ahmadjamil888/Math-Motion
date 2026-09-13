"""
Formula Evaluator
Evaluates symbolic expressions at specific points using NumPy.
"""

import numpy as np
from sympy import lambdify, diff, integrate, simplify
from sympy.core.expr import Expr
from typing import Callable, Optional, Tuple, List


class FormulaEvaluator:
    """Evaluates mathematical expressions at specific points."""
    
    def __init__(self):
        self.compiled_functions = {}
    
    def compile_function(self, expr: Expr, variable: str = 'x') -> Callable:
        """
        Compile a SymPy expression into a NumPy-compatible function.
        
        Args:
            expr: SymPy expression
            variable: Variable name
            
        Returns:
            Function that can be called with NumPy arrays
        """
        # Create a cache key
        cache_key = str(expr) + variable
        
        if cache_key in self.compiled_functions:
            return self.compiled_functions[cache_key]
        
        # Compile the function
        func = lambdify(variable, expr, modules=['numpy'])
        self.compiled_functions[cache_key] = func
        return func
    
    def evaluate(self, expr: Expr, x_values: np.ndarray, 
                 variable: str = 'x') -> np.ndarray:
        """
        Evaluate expression at given x values.
        
        Args:
            expr: SymPy expression
            x_values: Array of x values to evaluate
            variable: Variable name
            
        Returns:
            Array of y values
        """
        func = self.compile_function(expr, variable)
        try:
            return func(x_values)
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            return np.zeros_like(x_values)
    
    def evaluate_range(self, expr: Expr, domain: Tuple[float, float], 
                      num_points: int = 1000, variable: str = 'x') -> Tuple[np.ndarray, np.ndarray]:
        """
        Evaluate expression over a range of values.
        
        Args:
            expr: SymPy expression
            domain: Tuple of (min, max) values
            num_points: Number of points to evaluate
            variable: Variable name
            
        Returns:
            Tuple of (x_values, y_values) arrays
        """
        x_values = np.linspace(domain[0], domain[1], num_points)
        y_values = self.evaluate(expr, x_values, variable)
        return x_values, y_values
    
    def derivative(self, expr: Expr, variable: str = 'x', order: int = 1) -> Expr:
        """
        Compute the derivative of an expression.
        
        Args:
            expr: SymPy expression
            variable: Variable to differentiate with respect to
            order: Order of derivative (1 for first, 2 for second, etc.)
            
        Returns:
            Derivative expression
        """
        return diff(expr, variable, order)
    
    def integral(self, expr: Expr, variable: str = 'x') -> Expr:
        """
        Compute the indefinite integral of an expression.
        
        Args:
            expr: SymPy expression
            variable: Variable to integrate with respect to
            
        Returns:
            Integral expression
        """
        return integrate(expr, variable)
    
    def simplify_expression(self, expr: Expr) -> Expr:
        """
        Simplify a mathematical expression.
        
        Args:
            expr: SymPy expression
            
        Returns:
            Simplified expression
        """
        return simplify(expr)
    
    def find_roots(self, expr: Expr, variable: str = 'x', 
                   domain: Optional[Tuple[float, float]] = None) -> List[float]:
        """
        Find approximate roots of an expression within a domain.
        
        Args:
            expr: SymPy expression
            variable: Variable name
            domain: Optional domain to search within
            
        Returns:
            List of root values
        """
        from sympy import solve
        
        try:
            solutions = solve(expr, variable)
            roots = []
            
            for sol in solutions:
                if sol.is_real:
                    root = float(sol)
                    if domain is None or (domain[0] <= root <= domain[1]):
                        roots.append(root)
            
            return roots
        except Exception as e:
            print(f"Error finding roots: {e}")
            return []
    
    def clear_cache(self):
        """Clear the compiled function cache."""
        self.compiled_functions.clear()
