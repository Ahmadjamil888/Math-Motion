"""
Mathematical Functions
Provides common mathematical functions and utilities for formula processing.
"""

import numpy as np
from typing import Callable, Dict, List


class MathFunctions:
    """Collection of mathematical functions and utilities."""
    
    @staticmethod
    def get_common_functions() -> Dict[str, Callable]:
        """
        Get dictionary of common mathematical functions.
        
        Returns:
            Dictionary mapping function names to their implementations
        """
        return {
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'asin': np.arcsin,
            'acos': np.arccos,
            'atan': np.arctan,
            'sinh': np.sinh,
            'cosh': np.cosh,
            'tanh': np.tanh,
            'exp': np.exp,
            'log': np.log,
            'log10': np.log10,
            'log2': np.log2,
            'sqrt': np.sqrt,
            'abs': np.abs,
            'power': np.power,
            'floor': np.floor,
            'ceil': np.ceil,
            'round': np.round,
        }
    
    @staticmethod
    def get_function_examples() -> List[str]:
        """
        Get list of example formulas.
        
        Returns:
            List of example formula strings
        """
        return [
            "x**2",
            "sin(x)",
            "cos(x)",
            "exp(x)",
            "log(x)",
            "sqrt(x)",
            "sin(x**2)",
            "cos(x) + sin(x)",
            "x**3 - 3*x",
            "sin(x) * cos(x)",
            "exp(-x**2)",
            "1/(1 + x**2)",
            "sin(x)/x",
            "tan(x)",
            "abs(x)",
        ]
    
    @staticmethod
    def safe_evaluate(func: Callable, x: float, default: float = 0.0) -> float:
        """
        Safely evaluate a function, returning default on error.
        
        Args:
            func: Function to evaluate
            x: Input value
            default: Default value if evaluation fails
            
        Returns:
            Function result or default value
        """
        try:
            result = func(x)
            if np.isfinite(result):
                return float(result)
            return default
        except (ZeroDivisionError, ValueError, OverflowError):
            return default
    
    @staticmethod
    def normalize_array(arr: np.ndarray, target_min: float = 0.0, 
                        target_max: float = 1.0) -> np.ndarray:
        """
        Normalize array to target range.
        
        Args:
            arr: Input array
            target_min: Target minimum value
            target_max: Target maximum value
            
        Returns:
            Normalized array
        """
        arr_min = np.min(arr)
        arr_max = np.max(arr)
        
        if arr_max == arr_min:
            return np.full_like(arr, target_min)
        
        normalized = (arr - arr_min) / (arr_max - arr_min)
        return normalized * (target_max - target_min) + target_min
    
    @staticmethod
    def smooth_data(data: np.ndarray, window_size: int = 5) -> np.ndarray:
        """
        Apply moving average smoothing to data.
        
        Args:
            data: Input data array
            window_size: Size of smoothing window
            
        Returns:
            Smoothed data array
        """
        if len(data) < window_size:
            return data
        
        kernel = np.ones(window_size) / window_size
        return np.convolve(data, kernel, mode='same')
    
    @staticmethod
    def resample_data(x: np.ndarray, y: np.ndarray, 
                     num_points: int) -> tuple[np.ndarray, np.ndarray]:
        """
        Resample data to a specific number of points.
        
        Args:
            x: Original x values
            y: Original y values
            num_points: Target number of points
            
        Returns:
            Tuple of resampled (x, y) arrays
        """
        from scipy import interpolate
        
        if len(x) < 2:
            return x, y
        
        # Create interpolation function
        f = interpolate.interp1d(x, y, kind='cubic', 
                                 fill_value='extrapolate')
        
        # Generate new x values
        x_new = np.linspace(x.min(), x.max(), num_points)
        y_new = f(x_new)
        
        return x_new, y_new
    
    @staticmethod
    def detect_features(x: np.ndarray, y: np.ndarray, 
                       threshold: float = 0.1) -> Dict[str, List[int]]:
        """
        Detect features in the data (peaks, valleys, inflection points).
        
        Args:
            x: X values
            y: Y values
            threshold: Threshold for feature detection
            
        Returns:
            Dictionary with lists of indices for each feature type
        """
        from scipy.signal import find_peaks
        
        # Find peaks
        peaks, _ = find_peaks(y, height=threshold)
        
        # Find valleys (peaks in inverted data)
        valleys, _ = find_peaks(-y, height=threshold)
        
        # Calculate approximate inflection points (where second derivative changes sign)
        dy = np.gradient(y, x)
        d2y = np.gradient(dy, x)
        inflection_points = np.where(np.diff(np.sign(d2y)) != 0)[0]
        
        return {
            'peaks': peaks.tolist(),
            'valleys': valleys.tolist(),
            'inflection_points': inflection_points.tolist()
        }
