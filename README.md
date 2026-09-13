# Math Motion - Mathematical Animation Studio

A comprehensive desktop application for creating music-reactive mathematical animations using Manim, SymPy, librosa, and FFmpeg.

## Features

- **Formula Input**: Parse and visualize mathematical formulas using SymPy
- **Music Synchronization**: Analyze audio beats and energy for reactive animations
- **Real-time Preview**: Live preview of mathematical graphs and animations
- **Multiple Styles**: Choose from Minimal, Cinematic, Neon, or Scientific visual styles
- **Flexible Rendering**: Support for various resolutions (720p to 4K) and frame rates
- **Audio Integration**: Combine animations with music using FFmpeg

## Architecture

```
Math Motion Application
├── GUI Layer (PySide6)
│   ├── Main Window
│   ├── Formula Editor
│   ├── Timeline Widget
│   └── Preview Widget
├── Math Engine (SymPy, NumPy)
│   ├── Formula Parser
│   ├── Formula Evaluator
│   ├── Math Functions
│   └── Geometry Generator
├── Audio Engine (librosa)
│   ├── Audio Loader
│   ├── Beat Detection
│   ├── Energy Analysis
│   └── Audio Synchronization
├── Animation Engine (Manim)
│   ├── Math Scene
│   ├── Animation Timeline
│   ├── Transition Manager
│   └── Effect Manager
└── Render Engine (FFmpeg)
    ├── Manim Renderer
    └── FFmpeg Processor
```

## Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (must be installed and available in system PATH)
- Manim Community Edition

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Ahmadjamil888/Math-Motion.git
cd Math-Motion
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install FFmpeg:
- **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH
- **macOS**: `brew install ffmpeg`
- **Linux**: `sudo apt install ffmpeg`

4. Install Manim:
```bash
pip install manim
```

## Usage

### Running the Application

```bash
python app/main.py
```

### Basic Workflow

1. **Enter a Formula**: Type a mathematical formula in the Formula tab
   - Examples: `sin(x^2)`, `x^3 - 3*x`, `exp(-x^2)`

2. **Set Domain**: Adjust the x-axis range for the graph

3. **Load Music** (Optional): Add an audio file for synchronization
   - Supported formats: MP3, WAV, OGG, FLAC, M4A

4. **Choose Style**: Select a visual style from the Style tab
   - Minimal, Cinematic, Neon, Scientific

5. **Configure Output**: Set resolution, frame rate, and output path

6. **Render**: Click the RENDER button to generate the animation

### Supported Formulas

The application supports standard mathematical notation:
- Basic operations: `+`, `-`, `*`, `/`, `^`
- Functions: `sin`, `cos`, `tan`, `exp`, `log`, `sqrt`, `abs`
- Complex expressions: `sin(x^2) + 0.5*cos(3*x)`

## Project Structure

```
animatics/
├── app/
│   ├── ui/              # GUI components
│   ├── math/            # Mathematical processing
│   ├── audio/           # Audio analysis
│   ├── animation/       # Animation logic
│   ├── render/          # Rendering engines
│   └── main.py          # Application entry point
├── assets/
│   ├── music/           # Sample audio files
│   ├── fonts/           # Custom fonts
│   └── textures/        # Textures and images
├── projects/            # Saved project files
├── output/              # Rendered videos
└── requirements.txt     # Python dependencies
```

## API Reference

### Math Engine

```python
from app.math.parser import FormulaParser
from app.math.evaluator import FormulaEvaluator

parser = FormulaParser()
evaluator = FormulaEvaluator()

# Parse formula
expr = parser.parse("sin(x^2)")

# Evaluate formula
x_values, y_values = evaluator.evaluate_range(expr, (-10, 10), 1000)
```

### Audio Engine

```python
from app.audio.loader import AudioLoader
from app.audio.beat_detection import BeatDetector

loader = AudioLoader()
detector = BeatDetector()

# Load audio
audio, sr = loader.load_audio("music.mp3")

# Detect beats
beat_info = detector.detect_beats(audio, sr)
```

### Animation Engine

```python
from app.animation.scene import MathScene, AnimationConfig

config = AnimationConfig(resolution=(1920, 1080), fps=60)
scene = MathScene(config)
```

## Development

### Running Tests

```bash
python tests/test_formula_parser.py
python tests/test_audio_analysis.py
```

### Building for Distribution

```bash
# Using PyInstaller
pyinstaller --onefile --windowed app/main.py
```

## Troubleshooting

### FFmpeg Not Found
Ensure FFmpeg is installed and added to your system PATH:
```bash
ffmpeg -version  # Should show version info
```

### Manim Rendering Issues
Check that Manim is properly installed:
```bash
manim --version
```

### Audio Loading Problems
Ensure audio files are in supported formats and not corrupted.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Credits

Built with:
- [Manim](https://www.manim.community/) - Mathematical animation engine
- [SymPy](https://www.sympy.org/) - Symbolic mathematics
- [librosa](https://librosa.org/) - Audio analysis
- [PySide6](https://www.qt.io/) - GUI framework
- [FFmpeg](https://ffmpeg.org/) - Video processing

## Contact

For questions or support, please open an issue on GitHub.
