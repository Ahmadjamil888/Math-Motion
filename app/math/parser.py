"""
Formula Parser using SymPy
Converts mathematical string expressions into symbolic expressions.
"""

from sympy import symbols, parse_expr, sympify, SympifyError
from sympy.core.expr import Expr
from typing import Optional, Dict, Any


class FormulaParser:
    """Parses mathematical formulas using SymPy."""
    
    def __init__(self):
        self.variables = {}
        self._init_common_symbols()
    
    def _init_common_symbols(self):
        """Initialize common mathematical symbols."""
        self.variables['x'] = symbols('x', real=True)
        self.variables['y'] = symbols('y', real=True)
        self.variables['t'] = symbols('t', real=True)
        self.variables['theta'] = symbols('theta', real=True)
    
    def parse(self, formula: str, variable: str = 'x') -> Optional[Expr]:
        """
        Parse a mathematical formula string into a SymPy expression.
        
        Args:
            formula: Mathematical formula as string (e.g., "sin(x^2) + 0.5*cos(3*x)")
            variable: Main variable for the formula (default: 'x')
            
        Returns:
            SymPy expression or None if parsing fails
        """
        try:
            # Ensure the variable is defined
            if variable not in self.variables:
                self.variables[variable] = symbols(variable, real=True)
            
            # Parse the expression
            expr = parse_expr(formula, local_dict=self.variables)
            return expr
        except (SympifyError, SyntaxError) as e:
            print(f"Error parsing formula '{formula}': {e}")
            return None
    
    def parse_with_domain(self, formula: str, variable: str = 'x', 
                         domain: tuple = (-10, 10)) -> Optional[Dict[str, Any]]:
        """
        Parse formula with domain information.
        
        Args:
            formula: Mathematical formula as string
            variable: Main variable for the formula
            domain: Tuple of (min, max) values for the variable
            
        Returns:
            Dictionary with expression and domain info or None if parsing fails
        """
        expr = self.parse(formula, variable)
        if expr is None:
            return None
        
        return {
            'expression': expr,
            'variable': variable,
            'domain': domain,
            'formula_string': formula
        }
    
    def add_variable(self, name: str, real: bool = True):
        """Add a custom variable symbol."""
        self.variables[name] = symbols(name, real=real)
    
    def get_variables(self) -> Dict[str, Any]:
        """Get all defined variables."""
        return self.variables.copy()
    
    def is_valid_formula(self, formula: str) -> bool:
        """Check if a formula string is valid."""
        return self.parse(formula) is not None
