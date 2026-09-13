"""
Geometry Generator
Converts mathematical expressions into geometric coordinates for rendering.
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass


@dataclass
class GraphData:
    """Data structure for graph coordinates."""
    x: np.ndarray
    y: np.ndarray
    domain: Tuple[float, float]
    variable: str = 'x'
    
    def to_point_pairs(self) -> List[Tuple[float, float]]:
        """Convert to list of (x, y) tuples."""
        return list(zip(self.x, self.y))
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """Get (x_min, x_max, y_min, y_max) bounds."""
        return (self.x.min(), self.x.max(), self.y.min(), self.y.max())


class GeometryGenerator:
    """Generates geometric data from mathematical expressions."""
    
    def __init__(self):
        self.default_resolution = 1000
    
    def generate_graph(self, x_values: np.ndarray, y_values: np.ndarray,
                      variable: str = 'x', domain: Optional[Tuple[float, float]] = None) -> GraphData:
        """
        Generate graph data from coordinate arrays.
        
        Args:
            x_values: Array of x coordinates
            y_values: Array of y coordinates
            variable: Variable name
            domain: Optional domain tuple
            
        Returns:
            GraphData object
        """
        if domain is None:
            domain = (float(x_values.min()), float(x_values.max()))
        
        return GraphData(
            x=x_values,
            y=y_values,
            domain=domain,
            variable=variable
        )
    
    def generate_parametric(self, x_func: callable, y_func: callable,
                           t_range: Tuple[float, float],
                           num_points: int = 1000) -> GraphData:
        """
        Generate parametric curve data.
        
        Args:
            x_func: Function for x coordinate as function of t
            y_func: Function for y coordinate as function of t
            t_range: Tuple of (t_min, t_max)
            num_points: Number of points to generate
            
        Returns:
            GraphData object with parametric coordinates
        """
        t_values = np.linspace(t_range[0], t_range[1], num_points)
        x_values = x_func(t_values)
        y_values = y_func(t_values)
        
        return GraphData(
            x=x_values,
            y=y_values,
            domain=t_range,
            variable='t'
        )
    
    def generate_polar(self, r_func: callable, theta_range: Tuple[float, float] = (0, 2*np.pi),
                      num_points: int = 1000) -> GraphData:
        """
        Generate polar curve data.
        
        Args:
            r_func: Function for radius as function of theta
            theta_range: Tuple of (theta_min, theta_max)
            num_points: Number of points to generate
            
        Returns:
            GraphData object with Cartesian coordinates from polar
        """
        theta_values = np.linspace(theta_range[0], theta_range[1], num_points)
        r_values = r_func(theta_values)
        
        # Convert to Cartesian coordinates
        x_values = r_values * np.cos(theta_values)
        y_values = r_values * np.sin(theta_values)
        
        return GraphData(
            x=x_values,
            y=y_values,
            domain=theta_range,
            variable='theta'
        )
    
    def generate_implicit_contour(self, func: callable, x_range: Tuple[float, float],
                                y_range: Tuple[float, float],
                                resolution: int = 100) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate data for implicit function contour plot.
        
        Args:
            func: Function f(x, y) = 0
            x_range: Tuple of (x_min, x_max)
            y_range: Tuple of (y_min, y_max)
            resolution: Grid resolution
            
        Returns:
            Tuple of (X, Y, Z) meshgrid arrays
        """
        x = np.linspace(x_range[0], x_range[1], resolution)
        y = np.linspace(y_range[0], y_range[1], resolution)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        
        return X, Y, Z
    
    def generate_vector_field(self, x_func: callable, y_func: callable,
                            x_range: Tuple[float, float],
                            y_range: Tuple[float, float],
                            grid_size: int = 20) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Generate vector field data.
        
        Args:
            x_func: Function for x component of vector
            y_func: Function for y component of vector
            x_range: Tuple of (x_min, x_max)
            y_range: Tuple of (y_min, y_max)
            grid_size: Number of grid points in each direction
            
        Returns:
            Tuple of (X, Y, U, V) arrays for vector field
        """
        x = np.linspace(x_range[0], x_range[1], grid_size)
        y = np.linspace(y_range[0], y_range[1], grid_size)
        X, Y = np.meshgrid(x, y)
        U = x_func(X, Y)
        V = y_func(X, Y)
        
        return X, Y, U, V
    
    def apply_transform(self, graph: GraphData, transform_matrix: np.ndarray) -> GraphData:
        """
        Apply affine transformation to graph data.
        
        Args:
            graph: Original GraphData
            transform_matrix: 3x3 transformation matrix
            
        Returns:
            Transformed GraphData
        """
        # Convert to homogeneous coordinates
        ones = np.ones_like(graph.x)
        points = np.vstack([graph.x, graph.y, ones])
        
        # Apply transformation
        transformed = transform_matrix @ points
        
        return GraphData(
            x=transformed[0, :],
            y=transformed[1, :],
            domain=graph.domain,
            variable=graph.variable
        )
    
    def scale_graph(self, graph: GraphData, scale_x: float = 1.0, 
                   scale_y: float = 1.0) -> GraphData:
        """Scale graph coordinates."""
        return GraphData(
            x=graph.x * scale_x,
            y=graph.y * scale_y,
            domain=(graph.domain[0] * scale_x, graph.domain[1] * scale_x),
            variable=graph.variable
        )
    
    def translate_graph(self, graph: GraphData, dx: float = 0.0, 
                       dy: float = 0.0) -> GraphData:
        """Translate graph coordinates."""
        return GraphData(
            x=graph.x + dx,
            y=graph.y + dy,
            domain=(graph.domain[0] + dx, graph.domain[1] + dx),
            variable=graph.variable
        )
    
    def rotate_graph(self, graph: GraphData, angle: float) -> GraphData:
        """
        Rotate graph coordinates around origin.
        
        Args:
            graph: Original GraphData
            angle: Rotation angle in radians
            
        Returns:
            Rotated GraphData
        """
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        
        x_rotated = graph.x * cos_a - graph.y * sin_a
        y_rotated = graph.x * sin_a + graph.y * cos_a
        
        return GraphData(
            x=x_rotated,
            y=y_rotated,
            domain=graph.domain,
            variable=graph.variable
        )
    
    def calculate_arc_length(self, graph: GraphData) -> float:
        """Calculate total arc length of the graph."""
        dx = np.diff(graph.x)
        dy = np.diff(graph.y)
        ds = np.sqrt(dx**2 + dy**2)
        return np.sum(ds)
    
    def calculate_curvature(self, graph: GraphData) -> np.ndarray:
        """
        Calculate curvature at each point.
        
        Args:
            graph: GraphData object
            
        Returns:
            Array of curvature values
        """
        dx = np.gradient(graph.x)
        dy = np.gradient(graph.y)
        ddx = np.gradient(dx)
        ddy = np.gradient(dy)
        
        numerator = dx * ddy - dy * ddx
        denominator = (dx**2 + dy**2)**(3/2)
        
        # Avoid division by zero
        denominator = np.where(denominator == 0, 1e-10, denominator)
        
        return numerator / denominator
