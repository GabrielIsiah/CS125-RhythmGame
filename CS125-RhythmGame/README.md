# Rhythm Game

A rhythm-based game where players hit arrows in sync with music. The game features multiple songs, difficulty levels, and a unique gravity mode.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CS125-RhythmGame.git
cd CS125-RhythmGame
```

2. Create and activate a virtual environment (recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Game Structure

The game uses the following directory structure:
```
CS125-RhythmGame/
├── assets/
│   ├── fonts/
│   │   └── Grand9k Pixel.ttf
│   ├── songs/
│   │   ├── Song 1/
│   │   │   ├── audio/
│   │   │   │   └── song1.mp3
│   │   │   └── key_log.csv
│   │   ├── Song 2/
│   │   │   ├── audio/
│   │   │   │   └── song2.mp3
│   │   │   └── key_log.csv
│   │   └── Song 3/
│   │       ├── audio/
│   │       │   └── song3.mp3
│   │       └── key_log.csv
│   ├── sounds/
│   │   ├── perfect.wav
│   │   ├── good.wav
│   │   └── miss.wav
│   └── vids/
│       ├── song1.mp4
│       ├── song2.mp4
│       └── song3.mp4
├── game/
│   ├── arrow_spawner.py
│   ├── constants.py
│   ├── game.py
│   ├── hit_detection.py
│   ├── menu.py
│   ├── outline_manager.py
│   ├── pattern_manager.py
│   └── pyvidplayer.py
├── Sprites/
│   └── tiles.py
├── Utility/
│   ├── audio_manager.py
│   └── font_manager.py
├── requirements.txt
└── Main.py
```

## Running the Game

1. Make sure you're in the project directory and your virtual environment is activated:
```bash
cd CS125-RhythmGame
# Activate virtual environment if not already activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

2. Run the game:
```bash
python Main.py
```

## Game Controls

- **D**: Left arrow
- **F**: Down arrow
- **J**: Up arrow
- **K**: Right arrow
- **ESC**: Pause/Resume game

## Game Features

- Multiple songs with different difficulties
- Gravity mode (arrows fall from top or bottom)
- Combo system
- Score tracking
- Hit feedback (Perfect, Good, Late, Miss)
- Background video with adjustable transparency
- Song-specific music videos

## Troubleshooting

If you encounter any issues:

1. **Missing Dependencies**: Make sure all required packages are installed:
```bash
pip install -r requirements.txt
```

2. **Audio Issues**: 
   - Check if your system's audio is working
   - Make sure the audio files are in the correct locations
   - Verify that the audio file paths in `menu.py` are correct

3. **Video Issues**:
   - Ensure the video files are in the correct location (`assets/vids/songX.mp4` where X is the song number)
   - Check if your system supports the video codec
   - Each song should have its corresponding video file (e.g., song1.mp4 for Song 1)

4. **Font Issues**:
   - Make sure the font file is in the correct location (`assets/fonts/Grand9k Pixel.ttf`)
   - If the font is missing, the game will fall back to the system font

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.