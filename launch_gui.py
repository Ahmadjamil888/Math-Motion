"""
Simple GUI Launcher
Launches the Math Motion GUI with available components.
"""

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from PySide6.QtWidgets import QApplication
from app.ui.main_window import MainWindow
from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator
from app.math.geometry import GeometryGenerator


class SimpleMathMotionApp:
    """Simplified version of Math Motion with available components."""
    
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle('Fusion')
        
        # Initialize mathematical components
        self.parser = FormulaParser()
        self.evaluator = FormulaEvaluator()
        self.geometry = GeometryGenerator()
        
        # Initialize main window
        self.main_window = MainWindow()
        self.main_window.setWindowTitle("Math Motion (Basic - No Animation)")
        
        # Connect basic signals
        self.main_window.formula_changed.connect(self.on_formula_changed)
        
        # Disable render button since animation isn't available
        self.main_window.render_button.setEnabled(False)
        self.main_window.render_button.setText("RENDER (N/A)")
        self.main_window.render_button.setStyleSheet("""
            QPushButton {
                background-color: #7f8c8d;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
        """)
        
        # Note: Music loading disabled in basic version
    
    def on_formula_changed(self, formula: str):
        """Handle formula change."""
        if not formula:
            return
        
        try:
            # Convert ^ to ** for Python compatibility
            formula_python = formula.replace('^', '**')
            
            # Parse formula
            parsed = self.parser.parse_with_domain(formula_python, domain=(-10, 10))
            
            if parsed:
                # Evaluate formula
                x_values, y_values = self.evaluator.evaluate_range(
                    parsed['expression'],
                    parsed['domain'],
                    num_points=1000
                )
                
                # Update preview
                self.main_window.preview_widget.set_graph_data(x_values, y_values)
                self.main_window.status_bar.showMessage(f"Formula processed: {formula}")
            else:
                self.main_window.status_bar.showMessage("Failed to process formula")
        
        except Exception as e:
            self.main_window.status_bar.showMessage(f"Error: {str(e)}")
    
    def run(self):
        """Run the application."""
        self.main_window.show()
        return self.app.exec()


def main():
    """Main entry point."""
    print("=" * 60)
    print("Math Motion - Basic GUI Version")
    print("=" * 60)
    print("Features available:")
    print("- Formula parsing and evaluation")
    print("- Real-time graph preview")
    print("- Mathematical transformations")
    print("\nFeatures disabled (require additional setup):")
    print("- Audio analysis (requires audio file)")
    print("- Animation rendering (requires Manim + C++ Build Tools)")
    print("- Video export (requires FFmpeg)")
    print("=" * 60)
    
    app = SimpleMathMotionApp()
    sys.exit(app.run())


if __name__ == "__main__":
    main()
