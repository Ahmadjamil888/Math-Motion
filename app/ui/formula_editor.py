"""
Formula Editor
Widget for editing and previewing mathematical formulas.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                               QLabel, QComboBox, QPushButton, QFrame)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont, QTextCharFormat, QColor
from typing import List


class FormulaEditor(QWidget):
    """Widget for editing mathematical formulas with syntax highlighting."""
    
    formula_changed = Signal(str)
    
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        self.current_formula = ""
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Formula input area
        self.formula_input = QTextEdit()
        self.formula_input.setPlaceholderText("Enter formula (e.g., sin(x^2) + 0.5*cos(3*x))")
        self.formula_input.setMaximumHeight(100)
        self.formula_input.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: 2px solid #34495e;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 14px;
            }
            QTextEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        self.formula_input.textChanged.connect(self.on_formula_changed)
        layout.addWidget(self.formula_input)
        
        # Quick insert buttons
        quick_insert_frame = QFrame()
        quick_insert_frame.setStyleSheet("background-color: #2c3e50; border-radius: 8px; padding: 5px;")
        quick_insert_layout = QHBoxLayout(quick_insert_frame)
        
        quick_insert_label = QLabel("Quick Insert:")
        quick_insert_label.setStyleSheet("color: #ecf0f1; font-size: 12px;")
        quick_insert_layout.addWidget(quick_insert_label)
        
        # Quick insert buttons
        quick_buttons = [
            ("sin", "sin(x)"),
            ("cos", "cos(x)"),
            ("tan", "tan(x)"),
            ("exp", "exp(x)"),
            ("log", "log(x)"),
            ("sqrt", "sqrt(x)"),
            ("^2", "x^2"),
            ("^3", "x^3")
        ]
        
        for label, formula in quick_buttons:
            button = QPushButton(label)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            button.clicked.connect(lambda checked, f=formula: self.insert_formula(f))
            quick_insert_layout.addWidget(button)
        
        layout.addWidget(quick_insert_frame)
        
        # Example formulas dropdown
        example_layout = QHBoxLayout()
        
        example_label = QLabel("Examples:")
        example_label.setStyleSheet("color: #ecf0f1; font-size: 12px;")
        example_layout.addWidget(example_label)
        
        self.example_combo = QComboBox()
        self.example_combo.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        self.example_combo.addItems([
            "Select an example...",
            "x^2",
            "sin(x)",
            "cos(x)",
            "exp(x)",
            "log(x)",
            "sqrt(x)",
            "sin(x^2)",
            "cos(x) + sin(x)",
            "x^3 - 3*x",
            "sin(x) * cos(x)",
            "exp(-x^2)",
            "1/(1 + x^2)",
            "sin(x)/x"
        ])
        self.example_combo.currentIndexChanged.connect(self.on_example_selected)
        example_layout.addWidget(self.example_combo)
        
        layout.addLayout(example_layout)
        
        # Validation status
        self.validation_label = QLabel("Formula validation: Ready")
        self.validation_label.setStyleSheet("color: #95a5a6; font-size: 11px;")
        layout.addWidget(self.validation_label)
    
    def on_formula_changed(self):
        """Handle formula text change."""
        self.current_formula = self.formula_input.toPlainText()
        self.formula_changed.emit(self.current_formula)
        
        # Basic validation
        if self.validate_formula(self.current_formula):
            self.validation_label.setText("Formula validation: Valid")
            self.validation_label.setStyleSheet("color: #2ecc71; font-size: 11px;")
        else:
            self.validation_label.setText("Formula validation: Invalid")
            self.validation_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
    
    def validate_formula(self, formula: str) -> bool:
        """
        Basic formula validation.
        
        Args:
            formula: Formula string to validate
            
        Returns:
            True if formula appears valid, False otherwise
        """
        if not formula or not formula.strip():
            return False
        
        # Check for balanced parentheses
        if formula.count('(') != formula.count(')'):
            return False
        
        # Check for common mathematical functions
        valid_functions = ['sin', 'cos', 'tan', 'exp', 'log', 'sqrt', 'abs', 'power']
        has_function = any(func in formula.lower() for func in valid_functions)
        
        # Check for basic operators
        has_operator = any(op in formula for op in ['+', '-', '*', '/', '^'])
        
        # Check for variable
        has_variable = 'x' in formula.lower()
        
        # Formula should have at least one of these elements
        return has_function or has_operator or has_variable
    
    def insert_formula(self, formula: str):
        """
        Insert formula at cursor position.
        
        Args:
            formula: Formula to insert
        """
        cursor = self.formula_input.textCursor()
        cursor.insertText(formula)
        self.formula_input.setTextCursor(cursor)
    
    def on_example_selected(self, index: int):
        """Handle example formula selection."""
        if index > 0:  # Skip the "Select an example..." option
            formula = self.example_combo.itemText(index)
            self.formula_input.setText(formula)
            self.example_combo.setCurrentIndex(0)  # Reset to default
    
    def get_formula(self) -> str:
        """Get current formula."""
        return self.current_formula
    
    def set_formula(self, formula: str):
        """Set formula text."""
        self.formula_input.setText(formula)
        self.current_formula = formula
    
    def clear(self):
        """Clear the formula editor."""
        self.formula_input.clear()
        self.current_formula = ""
        self.validation_label.setText("Formula validation: Ready")
        self.validation_label.setStyleSheet("color: #95a5a6; font-size: 11px;")
