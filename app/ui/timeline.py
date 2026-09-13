"""
Timeline Widget
Visual timeline for animation events and audio synchronization.
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSlider, 
                               QLabel, QPushButton, QFrame, QScrollArea)
from PySide6.QtCore import Signal, Qt, QTimer, QRectF
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QFont
from typing import List, Dict


class TimelineWidget(QWidget):
    """Visual timeline for animation events and audio synchronization."""
    
    time_changed = Signal(float)
    event_selected = Signal(dict)
    
    def __init__(self):
        super().__init__()
        
        self.duration = 10.0  # Default duration in seconds
        self.current_time = 0.0
        self.events: List[Dict] = []
        self.audio_waveform: List[float] = []
        self.is_playing = False
        self.playback_speed = 1.0
        
        self.init_ui()
        self.init_timer()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Timeline controls
        controls_layout = QHBoxLayout()
        
        # Play/Pause button
        self.play_button = QPushButton("▶")
        self.play_button.setFixedSize(40, 40)
        self.play_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.play_button.clicked.connect(self.toggle_playback)
        controls_layout.addWidget(self.play_button)
        
        # Stop button
        stop_button = QPushButton("■")
        stop_button.setFixedSize(40, 40)
        stop_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 20px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        stop_button.clicked.connect(self.stop_playback)
        controls_layout.addWidget(stop_button)
        
        # Time display
        self.time_display = QLabel("00:00.00")
        self.time_display.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 16px;
                font-family: monospace;
                padding: 0 10px;
            }
        """)
        controls_layout.addWidget(self.time_display)
        
        # Duration display
        self.duration_display = QLabel("/ 00:10.00")
        self.duration_display.setStyleSheet("""
            QLabel {
                color: #95a5a6;
                font-size: 16px;
                font-family: monospace;
                padding: 0 10px;
            }
        """)
        controls_layout.addWidget(self.duration_display)
        
        controls_layout.addStretch()
        
        # Zoom controls
        zoom_in_button = QPushButton("+")
        zoom_in_button.setFixedSize(30, 30)
        zoom_in_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: none;
                border-radius: 15px;
                font-size: 16px;
            }
        """)
        zoom_in_button.clicked.connect(self.zoom_in)
        controls_layout.addWidget(zoom_in_button)
        
        zoom_out_button = QPushButton("-")
        zoom_out_button.setFixedSize(30, 30)
        zoom_out_button.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: #ecf0f1;
                border: none;
                border-radius: 15px;
                font-size: 16px;
            }
        """)
        zoom_out_button.clicked.connect(self.zoom_out)
        controls_layout.addWidget(zoom_out_button)
        
        layout.addLayout(controls_layout)
        
        # Timeline slider
        self.time_slider = QSlider(Qt.Horizontal)
        self.time_slider.setRange(0, int(self.duration * 100))  # Centiseconds
        self.time_slider.setValue(0)
        self.time_slider.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 8px;
                background: #2c3e50;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #3498db;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
            QSlider::sub-page:horizontal {
                background: #3498db;
                border-radius: 4px;
            }
        """)
        self.time_slider.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.time_slider)
        
        # Event markers container
        self.event_markers_frame = QFrame()
        self.event_markers_frame.setFixedHeight(40)
        self.event_markers_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.event_markers_frame)
        
        # Beat markers
        self.beat_markers_frame = QFrame()
        self.beat_markers_frame.setFixedHeight(20)
        self.beat_markers_frame.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.beat_markers_frame)
    
    def init_timer(self):
        """Initialize playback timer."""
        self.playback_timer = QTimer()
        self.playback_timer.setInterval(16)  # ~60 FPS
        self.playback_timer.timeout.connect(self.update_playback)
    
    def toggle_playback(self):
        """Toggle play/pause state."""
        self.is_playing = not self.is_playing
        
        if self.is_playing:
            self.play_button.setText("⏸")
            self.playback_timer.start()
        else:
            self.play_button.setText("▶")
            self.playback_timer.stop()
    
    def stop_playback(self):
        """Stop playback and reset to beginning."""
        self.is_playing = False
        self.play_button.setText("▶")
        self.playback_timer.stop()
        self.current_time = 0.0
        self.update_time_display()
        self.time_slider.setValue(0)
    
    def update_playback(self):
        """Update playback time."""
        if self.is_playing:
            dt = 0.016 * self.playback_speed  # Time step
            self.current_time += dt
            
            if self.current_time >= self.duration:
                self.current_time = self.duration
                self.stop_playback()
            
            self.update_time_display()
            self.time_slider.setValue(int(self.current_time * 100))
            self.time_changed.emit(self.current_time)
    
    def on_slider_changed(self, value: int):
        """Handle slider value change."""
        self.current_time = value / 100.0
        self.update_time_display()
        self.time_changed.emit(self.current_time)
    
    def update_time_display(self):
        """Update time display label."""
        time_str = self.format_time(self.current_time)
        duration_str = self.format_time(self.duration)
        self.time_display.setText(time_str)
        self.duration_display.setText(f"/ {duration_str}")
    
    def format_time(self, seconds: float) -> str:
        """Format time as MM:SS.ms."""
        minutes = int(seconds // 60)
        seconds_remainder = seconds % 60
        centiseconds = int((seconds_remainder % 1) * 100)
        seconds_int = int(seconds_remainder)
        return f"{minutes:02d}:{seconds_int:02d}.{centiseconds:02d}"
    
    def set_duration(self, duration: float):
        """Set timeline duration."""
        self.duration = duration
        self.time_slider.setRange(0, int(duration * 100))
        self.update_time_display()
    
    def set_current_time(self, time: float):
        """Set current playback time."""
        self.current_time = max(0.0, min(time, self.duration))
        self.time_slider.setValue(int(self.current_time * 100))
        self.update_time_display()
    
    def add_event(self, time: float, event_type: str, metadata: Dict = None):
        """
        Add an event to the timeline.
        
        Args:
            time: Event time in seconds
            event_type: Type of event
            metadata: Additional event metadata
        """
        if metadata is None:
            metadata = {}
        
        self.events.append({
            'time': time,
            'type': event_type,
            'metadata': metadata
        })
        
        # Sort events by time
        self.events.sort(key=lambda e: e['time'])
        
        self.update()
    
    def clear_events(self):
        """Clear all events from timeline."""
        self.events.clear()
        self.update()
    
    def set_audio_waveform(self, waveform: List[float]):
        """
        Set audio waveform for visualization.
        
        Args:
            waveform: List of amplitude values
        """
        self.audio_waveform = waveform
        self.update()
    
    def zoom_in(self):
        """Zoom in on timeline."""
        self.playback_speed = min(self.playback_speed * 1.5, 4.0)
    
    def zoom_out(self):
        """Zoom out on timeline."""
        self.playback_speed = max(self.playback_speed / 1.5, 0.25)
    
    def paintEvent(self, event):
        """Paint event for custom drawing."""
        super().paintEvent(event)
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw event markers
        self.draw_event_markers(painter)
        
        # Draw beat markers
        self.draw_beat_markers(painter)
        
        # Draw waveform if available
        if self.audio_waveform:
            self.draw_waveform(painter)
    
    def draw_event_markers(self, painter: QPainter):
        """Draw event markers on timeline."""
        marker_height = 20
        marker_width = 8
        
        for event in self.events:
            x = int((event['time'] / self.duration) * self.time_slider.width())
            
            # Color based on event type
            if event['type'] == 'beat':
                color = QColor('#e74c3c')
            elif event['type'] == 'energy':
                color = QColor('#f39c12')
            else:
                color = QColor('#3498db')
            
            painter.setBrush(QBrush(color))
            painter.setPen(QPen(Qt.NoPen))
            
            # Draw marker
            painter.drawRect(x - marker_width // 2, 
                           self.event_markers_frame.y() + 10,
                           marker_width, marker_height)
    
    def draw_beat_markers(self, painter: QPainter):
        """Draw beat markers on timeline."""
        marker_height = 10
        marker_width = 4
        
        for event in self.events:
            if event['type'] == 'beat':
                x = int((event['time'] / self.duration) * self.time_slider.width())
                
                painter.setBrush(QBrush(QColor('#e74c3c')))
                painter.setPen(QPen(Qt.NoPen))
                
                painter.drawRect(x - marker_width // 2,
                               self.beat_markers_frame.y() + 5,
                               marker_width, marker_height)
    
    def draw_waveform(self, painter: QPainter):
        """Draw audio waveform."""
        if not self.audio_waveform:
            return
        
        waveform_height = 30
        waveform_y = self.beat_markers_frame.y() + 40
        
        painter.setPen(QPen(QColor('#3498db'), 1))
        
        step = len(self.audio_waveform) / self.time_slider.width()
        
        for i in range(self.time_slider.width()):
            sample_index = int(i * step)
            if sample_index < len(self.audio_waveform):
                amplitude = self.audio_waveform[sample_index]
                y = waveform_y + (1 - amplitude) * waveform_height / 2
                
                if i == 0:
                    painter.moveTo(i, y)
                else:
                    painter.lineTo(i, y)
    
    def get_events_at_time(self, time: float, window: float = 0.1) -> List[Dict]:
        """Get events within a time window."""
        return [e for e in self.events if abs(e['time'] - time) < window]
