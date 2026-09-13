"""
Main Window
Main application window for Math Motion.
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QSplitter, QFrame, QLabel, QPushButton, QStatusBar,
                               QMenuBar, QMenu, QFileDialog, QTabWidget)
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtGui import QAction, QIcon, QKeySequence
from typing import Optional
import sys


class MainWindow(QMainWindow):
    """Main application window for Math Motion."""
    
    # Signals
    formula_changed = Signal(str)
    music_loaded = Signal(str)
    render_requested = Signal()
    
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Math Motion - Mathematical Animation Studio")
        self.setGeometry(100, 100, 1400, 900)
        
        # Initialize UI components
        self.init_ui()
        self.init_menu()
        self.init_status_bar()
        
        # Application state
        self.current_formula = ""
        self.current_music_path = ""
        self.is_rendering = False
    
    def init_ui(self):
        """Initialize the user interface."""
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Create main content area with splitter
        content_splitter = QSplitter(Qt.Horizontal)
        
        # Left panel (controls)
        left_panel = self.create_left_panel()
        content_splitter.addWidget(left_panel)
        
        # Right panel (preview)
        right_panel = self.create_right_panel()
        content_splitter.addWidget(right_panel)
        
        # Set splitter proportions
        content_splitter.setStretchFactor(0, 1)
        content_splitter.setStretchFactor(1, 2)
        
        main_layout.addWidget(content_splitter)
        
        # Create footer (timeline)
        footer = self.create_footer()
        main_layout.addWidget(footer)
    
    def create_header(self) -> QFrame:
        """Create the header section."""
        header = QFrame()
        header.setFrameStyle(QFrame.StyledPanel)
        header.setFixedHeight(60)
        header.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-bottom: 2px solid #34495e;
            }
        """)
        
        layout = QHBoxLayout(header)
        
        # Logo/Title
        title_label = QLabel("MATH MOTION")
        title_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 24px;
                font-weight: bold;
                padding: 0 20px;
            }
        """)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        # Status indicator
        self.status_indicator = QLabel("● Ready")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #2ecc71;
                font-size: 14px;
                padding: 0 20px;
            }
        """)
        layout.addWidget(self.status_indicator)
        
        return header
    
    def create_left_panel(self) -> QFrame:
        """Create the left control panel."""
        left_panel = QFrame()
        left_panel.setFrameStyle(QFrame.StyledPanel)
        left_panel.setMinimumWidth(350)
        left_panel.setMaximumWidth(450)
        left_panel.setStyleSheet("""
            QFrame {
                background-color: #34495e;
                border-right: 2px solid #2c3e50;
            }
        """)
        
        layout = QVBoxLayout(left_panel)
        
        # Create tab widget for different control sections
        tab_widget = QTabWidget()
        tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #34495e;
            }
            QTabBar::tab {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
            }
        """)
        
        # Formula tab
        formula_tab = self.create_formula_tab()
        tab_widget.addTab(formula_tab, "Formula")
        
        # Music tab
        music_tab = self.create_music_tab()
        tab_widget.addTab(music_tab, "Music")
        
        # Style tab
        style_tab = self.create_style_tab()
        tab_widget.addTab(style_tab, "Style")
        
        # Render tab
        render_tab = self.create_render_tab()
        tab_widget.addTab(render_tab, "Render")
        
        layout.addWidget(tab_widget)
        
        return left_panel
    
    def create_formula_tab(self) -> QWidget:
        """Create the formula control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Formula input label
        formula_label = QLabel("Mathematical Formula:")
        formula_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(formula_label)
        
        # Formula input field (placeholder - will be replaced with FormulaEditor)
        from .formula_editor import FormulaEditor
        self.formula_editor = FormulaEditor()
        self.formula_editor.formula_changed.connect(self.on_formula_changed)
        layout.addWidget(self.formula_editor)
        
        # Domain controls
        domain_label = QLabel("Domain:")
        domain_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(domain_label)
        
        domain_layout = QHBoxLayout()
        self.domain_min_input = self.create_number_input(-10)
        self.domain_max_input = self.create_number_input(10)
        
        domain_layout.addWidget(QLabel("Min:"))
        domain_layout.addWidget(self.domain_min_input)
        domain_layout.addWidget(QLabel("Max:"))
        domain_layout.addWidget(self.domain_max_input)
        layout.addLayout(domain_layout)
        
        layout.addStretch()
        
        return widget
    
    def create_music_tab(self) -> QWidget:
        """Create the music control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Music file selection
        music_label = QLabel("Music File:")
        music_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(music_label)
        
        music_file_layout = QHBoxLayout()
        self.music_path_display = QLabel("No file selected")
        self.music_path_display.setStyleSheet("color: #95a5a6; font-size: 12px;")
        self.music_path_display.setWordWrap(True)
        
        browse_button = QPushButton("Browse")
        browse_button.setStyleSheet("""
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
        browse_button.clicked.connect(self.browse_music_file)
        
        music_file_layout.addWidget(self.music_path_display, 1)
        music_file_layout.addWidget(browse_button)
        layout.addLayout(music_file_layout)
        
        # Audio analysis placeholder
        audio_info_label = QLabel("Audio Analysis:")
        audio_info_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(audio_info_label)
        
        self.audio_info_display = QLabel("Load music file to see analysis")
        self.audio_info_display.setStyleSheet("color: #95a5a6; font-size: 12px;")
        self.audio_info_display.setWordWrap(True)
        layout.addWidget(self.audio_info_display)
        
        layout.addStretch()
        
        return widget
    
    def create_style_tab(self) -> QWidget:
        """Create the style control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Style presets
        style_label = QLabel("Animation Style:")
        style_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(style_label)
        
        from PySide6.QtWidgets import QRadioButton, QButtonGroup
        
        self.style_group = QButtonGroup()
        
        styles = ["Minimal", "Cinematic", "Neon", "Scientific"]
        for i, style in enumerate(styles):
            radio = QRadioButton(style)
            radio.setStyleSheet("color: #ecf0f1;")
            if i == 0:
                radio.setChecked(True)
            self.style_group.addButton(radio, i)
            layout.addWidget(radio)
        
        # Resolution
        resolution_label = QLabel("Resolution:")
        resolution_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(resolution_label)
        
        from PySide6.QtWidgets import QComboBox
        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems(["720p", "1080p", "1440p", "4K"])
        self.resolution_combo.setCurrentIndex(1)
        self.resolution_combo.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.resolution_combo)
        
        # Frame rate
        fps_label = QLabel("Frame Rate:")
        fps_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(fps_label)
        
        self.fps_combo = QComboBox()
        self.fps_combo.addItems(["24 FPS", "30 FPS", "60 FPS", "120 FPS"])
        self.fps_combo.setCurrentIndex(2)
        self.fps_combo.setStyleSheet("""
            QComboBox {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 5px;
                border-radius: 4px;
            """)
        layout.addWidget(self.fps_combo)
        
        layout.addStretch()
        
        return widget
    
    def create_render_tab(self) -> QWidget:
        """Create the render control tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Render settings
        render_label = QLabel("Render Settings:")
        render_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(render_label)
        
        # Output path
        output_label = QLabel("Output Path:")
        output_label.setStyleSheet("color: #ecf0f1; font-size: 14px;")
        layout.addWidget(output_label)
        
        output_layout = QHBoxLayout()
        self.output_path_display = QLabel("output/final_video.mp4")
        self.output_path_display.setStyleSheet("color: #95a5a6; font-size: 12px;")
        
        output_browse_button = QPushButton("Change")
        output_browse_button.setStyleSheet("""
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
        output_browse_button.clicked.connect(self.browse_output_path)
        
        output_layout.addWidget(self.output_path_display, 1)
        output_layout.addWidget(output_browse_button)
        layout.addLayout(output_layout)
        
        layout.addStretch()
        
        # Render button
        self.render_button = QPushButton("RENDER")
        self.render_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #7f8c8d;
            }
        """)
        self.render_button.clicked.connect(self.on_render_clicked)
        layout.addWidget(self.render_button)
        
        return widget
    
    def create_right_panel(self) -> QFrame:
        """Create the right preview panel."""
        right_panel = QFrame()
        right_panel.setFrameStyle(QFrame.StyledPanel)
        right_panel.setStyleSheet("""
            QFrame {
                background-color: #1a1a2e;
            }
        """)
        
        layout = QVBoxLayout(right_panel)
        
        # Preview label
        preview_label = QLabel("LIVE PREVIEW")
        preview_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #2c3e50;
            }
        """)
        layout.addWidget(preview_label)
        
        # Preview area (placeholder - will be replaced with Preview widget)
        from .preview import Preview
        self.preview_widget = Preview()
        layout.addWidget(self.preview_widget)
        
        return right_panel
    
    def create_footer(self) -> QFrame:
        """Create the footer timeline section."""
        footer = QFrame()
        footer.setFrameStyle(QFrame.StyledPanel)
        footer.setFixedHeight(120)
        footer.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-top: 2px solid #34495e;
            }
        """)
        
        layout = QVBoxLayout(footer)
        
        # Timeline label
        timeline_label = QLabel("TIMELINE")
        timeline_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 12px;
                font-weight: bold;
                padding: 5px 10px;
            }
        """)
        layout.addWidget(timeline_label)
        
        # Timeline widget (placeholder - will be replaced with Timeline widget)
        from .timeline import TimelineWidget
        self.timeline_widget = TimelineWidget()
        layout.addWidget(self.timeline_widget)
        
        return footer
    
    def create_number_input(self, default_value: float):
        """Create a number input field."""
        from PySide6.QtWidgets import QDoubleSpinBox
        spinbox = QDoubleSpinBox()
        spinbox.setRange(-1000, 1000)
        spinbox.setValue(default_value)
        spinbox.setStyleSheet("""
            QDoubleSpinBox {
                background-color: #2c3e50;
                color: #ecf0f1;
                padding: 5px;
                border-radius: 4px;
            }
        """)
        return spinbox
    
    def init_menu(self):
        """Initialize the menu bar."""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
            QMenuBar::item:selected {
                background-color: #3498db;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New Project", self)
        new_action.setShortcut(QKeySequence.New)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Project", self)
        open_action.setShortcut(QKeySequence.Open)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut(QKeySequence.Save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.Undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.Redo)
        edit_menu.addAction(redo_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        fullscreen_action = QAction("Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence.FullScreen)
        view_menu.addAction(fullscreen_action)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        documentation_action = QAction("Documentation", self)
        help_menu.addAction(documentation_action)
        
        about_action = QAction("About", self)
        help_menu.addAction(about_action)
    
    def init_status_bar(self):
        """Initialize the status bar."""
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2c3e50;
                color: #ecf0f1;
            }
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def browse_music_file(self):
        """Browse for music file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Music File",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a)"
        )
        
        if file_path:
            self.current_music_path = file_path
            self.music_path_display.setText(file_path.split("/")[-1])
            self.music_loaded.emit(file_path)
            self.status_bar.showMessage(f"Loaded: {file_path.split('/')[-1]}")
    
    def browse_output_path(self):
        """Browse for output file path."""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Select Output File",
            "output/final_video.mp4",
            "Video Files (*.mp4 *.avi *.mov)"
        )
        
        if file_path:
            self.output_path_display.setText(file_path)
    
    def on_formula_changed(self, formula: str):
        """Handle formula change."""
        self.current_formula = formula
        self.formula_changed.emit(formula)
        self.status_bar.showMessage(f"Formula: {formula}")
    
    def on_render_clicked(self):
        """Handle render button click."""
        if not self.current_formula:
            self.status_bar.showMessage("Please enter a formula first")
            return
        
        self.is_rendering = True
        self.render_button.setEnabled(False)
        self.render_button.setText("RENDERING...")
        self.status_indicator.setText("● Rendering")
        self.status_indicator.setStyleSheet("""
            QLabel {
                color: #f39c12;
                font-size: 14px;
                padding: 0 20px;
            }
        """)
        
        self.render_requested.emit()
        self.status_bar.showMessage("Rendering started...")
    
    def set_rendering_complete(self, success: bool):
        """Set rendering completion state."""
        self.is_rendering = False
        self.render_button.setEnabled(True)
        self.render_button.setText("RENDER")
        
        if success:
            self.status_indicator.setText("● Complete")
            self.status_indicator.setStyleSheet("""
                QLabel {
                    color: #2ecc71;
                    font-size: 14px;
                    padding: 0 20px;
                }
            """)
            self.status_bar.showMessage("Rendering completed successfully")
        else:
            self.status_indicator.setText("● Error")
            self.status_indicator.setStyleSheet("""
                QLabel {
                    color: #e74c3c;
                    font-size: 14px;
                    padding: 0 20px;
                }
            """)
            self.status_bar.showMessage("Rendering failed")
    
    def get_current_settings(self) -> dict:
        """Get current application settings."""
        return {
            'formula': self.current_formula,
            'music_path': self.current_music_path,
            'domain_min': self.domain_min_input.value(),
            'domain_max': self.domain_max_input.value(),
            'style': self.style_group.checkedId(),
            'resolution': self.resolution_combo.currentText(),
            'fps': self.fps_combo.currentText(),
            'output_path': self.output_path_display.text()
        }
