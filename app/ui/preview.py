"""
Preview Widget
Widget for previewing mathematical animations.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QFrame, QSizePolicy)
from PySide6.QtCore import Signal, Qt, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QPolygonF
from PySide6.QtCore import QPointF
import numpy as np
from typing import Optional


class Preview(QWidget):
    """Widget for previewing mathematical animations."""
    
    frame_requested = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.x_values = None
        self.y_values = None
        self.current_frame = 0
        self.total_frames = 0
        self.is_playing = False
        self.show_axes = True
        self.show_grid = True
        self.line_color = QColor('#00d4ff')
        self.background_color = QColor('#1a1a2e')
        self.axes_color = QColor('#ffffff')
        
        self.init_ui()
        self.init_timer()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Preview controls
        controls_frame = QFrame()
        controls_frame.setStyleSheet("background-color: #2c3e50; padding: 5px;")
        controls_layout = QHBoxLayout(controls_frame)
        
        # Play/Pause button
        self.play_button = QPushButton("▶ Play")
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.play_button.clicked.connect(self.toggle_playback)
        controls_layout.addWidget(self.play_button)
        
        # Reset button
        reset_button = QPushButton("↺ Reset")
        reset_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #34495e;
            }
        """)
        reset_button.clicked.connect(self.reset_preview)
        controls_layout.addWidget(reset_button)
        
        controls_layout.addStretch()
        
        # Frame counter
        self.frame_label = QLabel("Frame: 0/0")
        self.frame_label.setStyleSheet("color: #ecf0f1; font-size: 12px;")
        controls_layout.addWidget(self.frame_label)
        
        layout.addWidget(controls_frame)
        
        # Preview area (this widget itself)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumHeight(300)
        
        # Info overlay
        self.info_label = QLabel("No formula loaded")
        self.info_label.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 14px;
                background-color: rgba(44, 62, 80, 0.8);
                padding: 10px;
                border-radius: 8px;
            }
        """)
        self.info_label.setAlignment(Qt.AlignCenter)
    
    def init_timer(self):
        """Initialize animation timer."""
        self.animation_timer = QTimer()
        self.animation_timer.setInterval(33)  # ~30 FPS
        self.animation_timer.timeout.connect(self.update_animation)
    
    def toggle_playback(self):
        """Toggle play/pause state."""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_button.setText("⏸ Pause")
            self.animation_timer.start()
        else:
            self.play_button.setText("▶ Play")
            self.animation_timer.stop()
    
    def reset_preview(self):
        """Reset preview to first frame."""
        self.current_frame = 0
        self.is_playing = False
        self.play_button.setText("▶ Play")
        self.animation_timer.stop()
        self.update()
        self.update_frame_label()
    
    def update_animation(self):
        """Update animation frame."""
        if self.is_playing and self.total_frames > 0:
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.update()
            self.update_frame_label()
            self.frame_requested.emit()
    
    def update_frame_label(self):
        """Update frame counter label."""
        self.frame_label.setText(f"Frame: {self.current_frame}/{self.total_frames}")
    
    def set_graph_data(self, x_values: np.ndarray, y_values: np.ndarray):
        """
        Set graph data for preview.
        
        Args:
            x_values: X coordinate array
            y_values: Y coordinate array
        """
        self.x_values = x_values
        self.y_values = y_values
        self.total_frames = len(x_values)
        self.current_frame = 0
        self.info_label.setText(f"Formula loaded: {len(x_values)} points")
        self.update()
        self.update_frame_label()
    
    def clear_preview(self):
        """Clear preview data."""
        self.x_values = None
        self.y_values = None
        self.current_frame = 0
        self.total_frames = 0
        self.info_label.setText("No formula loaded")
        self.update()
        self.update_frame_label()
    
    def set_line_color(self, color: QColor):
        """Set line color for graph."""
        self.line_color = color
        self.update()
    
    def set_background_color(self, color: QColor):
        """Set background color."""
        self.background_color = color
        self.update()
    
    def set_axes_color(self, color: QColor):
        """Set axes color."""
        self.axes_color = color
        self.update()
    
    def toggle_axes(self, show: bool):
        """Toggle axes visibility."""
        self.show_axes = show
        self.update()
    
    def toggle_grid(self, show: bool):
        """Toggle grid visibility."""
        self.show_grid = show
        self.update()
    
    def paintEvent(self, event):
        """Paint event for custom drawing."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), self.background_color)
        
        # Draw axes if enabled
        if self.show_axes:
            self.draw_axes(painter)
        
        # Draw grid if enabled
        if self.show_grid:
            self.draw_grid(painter)
        
        # Draw graph if data is available
        if self.x_values is not None and self.y_values is not None:
            self.draw_graph(painter)
        
        # Draw info overlay if no data
        if self.x_values is None:
            self.draw_info_overlay(painter)
    
    def draw_axes(self, painter: QPainter):
        """Draw coordinate axes."""
        width = self.width()
        height = self.height()
        
        # Calculate center
        center_x = width // 2
        center_y = height // 2
        
        painter.setPen(QPen(self.axes_color, 2))
        
        # Draw X axis
        painter.drawLine(0, center_y, width, center_y)
        
        # Draw Y axis
        painter.drawLine(center_x, 0, center_x, height)
        
        # Draw axis labels
        painter.setPen(QPen(self.axes_color))
        painter.setFont(QFont('Arial', 10))
        
        painter.drawText(width - 20, center_y - 10, "x")
        painter.drawText(center_x + 10, 20, "y")
    
    def draw_grid(self, painter: QPainter):
        """Draw background grid."""
        width = self.width()
        height = self.height()
        
        painter.setPen(QPen(QColor('#34495e'), 1, Qt.DotLine))
        
        # Calculate grid spacing
        grid_spacing = 50
        
        # Draw vertical lines
        for x in range(0, width, grid_spacing):
            painter.drawLine(x, 0, x, height)
        
        # Draw horizontal lines
        for y in range(0, height, grid_spacing):
            painter.drawLine(0, y, width, y)
    
    def draw_graph(self, painter: QPainter):
        """Draw mathematical graph."""
        if self.x_values is None or self.y_values is None:
            return
        
        width = self.width()
        height = self.height()
        
        # Calculate scaling
        if len(self.x_values) > 0:
            x_min, x_max = np.min(self.x_values), np.max(self.x_values)
            y_min, y_max = np.min(self.y_values), np.max(self.y_values)
            
            # Add padding
            x_range = x_max - x_min if x_max != x_min else 1.0
            y_range = y_max - y_min if y_max != y_min else 1.0
            
            x_padding = x_range * 0.1
            y_padding = y_range * 0.1
            
            x_min -= x_padding
            x_max += x_padding
            y_min -= y_padding
            y_max += y_padding
            
            # Calculate scale factors
            x_scale = width / (x_max - x_min)
            y_scale = height / (y_max - y_min)
            
            # Draw line for current frame
            if self.current_frame > 0:
                painter.setPen(QPen(self.line_color, 2))
                
                points = []
                for i in range(min(self.current_frame, len(self.x_values))):
                    x = int((self.x_values[i] - x_min) * x_scale)
                    y = int(height - (self.y_values[i] - y_min) * y_scale)
                    points.append(QPointF(x, y))
                
                if len(points) > 1:
                    painter.drawPolyline(QPolygonF(points))
    
    def draw_info_overlay(self, painter: QPainter):
        """Draw info overlay when no data is loaded."""
        text = self.info_label.text()
        
        painter.setPen(QPen(QColor('#95a5a6')))
        painter.setFont(QFont('Arial', 14))
        
        rect = self.rect()
        painter.drawText(rect, Qt.AlignCenter, text)
    
    def get_current_frame(self) -> int:
        """Get current frame number."""
        return self.current_frame
    
    def set_current_frame(self, frame: int):
        """Set current frame number."""
        if 0 <= frame < self.total_frames:
            self.current_frame = frame
            self.update()
            self.update_frame_label()
    
    def get_frame_count(self) -> int:
        """Get total frame count."""
        return self.total_frames
