# Quick Start Guide

Get started with Math Motion in 5 minutes!

## Installation

1. **Clone or download the project**
   ```bash
   cd animatics
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```
   This will:
   - Check Python version (requires 3.8+)
   - Verify FFmpeg installation
   - Install Python dependencies
   - Create necessary directories
   - Run basic tests

3. **Launch the application**
   ```bash
   python app/main.py
   ```

## Your First Animation

### Step 1: Enter a Formula
- Click on the "Formula" tab in the left panel
- Type a mathematical formula like: `sin(x^2)`
- Or select an example from the dropdown

### Step 2: Adjust Domain
- Set the X-axis range (default: -10 to 10)
- The preview will update automatically

### Step 3: Add Music (Optional)
- Click the "Music" tab
- Click "Browse" to select an audio file
- The app will automatically detect beats and energy

### Step 4: Choose Style
- Click the "Style" tab
- Select a visual style:
  - **Minimal**: Clean, academic look
  - **Cinematic**: Dark theme with blue accents
  - **Neon**: Vibrant colors on dark background
  - **Scientific**: Professional research style

### Step 5: Configure Output
- Click the "Render" tab
- Choose resolution (720p, 1080p, 1440p, 4K)
- Set frame rate (24, 30, 60, 120 FPS)
- Select output location

### Step 6: Render
- Click the "RENDER" button
- Wait for rendering to complete
- Find your video in the output folder

## Formula Examples

Try these formulas to get started:

```
sin(x^2)
cos(x) + sin(x)
x^3 - 3*x
exp(-x^2)
1/(1 + x^2)
sin(x)/x
```

## Tips

- **Complex formulas**: Use parentheses for grouping: `sin(x^2) + 0.5*cos(3*x)`
- **Domain matters**: Adjust the domain to see different parts of the function
- **Music sync**: The best results come from music with clear beats
- **Preview first**: Use the preview to check your formula before rendering
- **Start simple**: Begin with basic formulas before trying complex ones

## Troubleshooting

### "FFmpeg not found"
- Install FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add it to your system PATH
- Run setup.py again

### "Formula parsing failed"
- Check for balanced parentheses
- Use standard mathematical notation
- Try a simpler formula first

### "Audio loading failed"
- Ensure the file is a supported format (MP3, WAV, OGG, FLAC, M4A)
- Check that the file isn't corrupted
- Try a different audio file

### Rendering takes too long
- Lower the resolution
- Reduce the frame rate
- Shorten the domain range
- Use a shorter audio clip

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [example_usage.py](example_usage.py) for programmatic usage
- Run [test_pipeline.py](test_pipeline.py) to test individual components
- Experiment with different formulas and styles

## Keyboard Shortcuts

- **Ctrl+N**: New project
- **Ctrl+O**: Open project
- **Ctrl+S**: Save project
- **F11**: Fullscreen mode
- **Space**: Play/pause preview

## Support

For issues or questions:
1. Check the README.md documentation
2. Run test_pipeline.py to diagnose problems
3. Open an issue on GitHub

Enjoy creating mathematical animations! 🎵📊
