# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## About

**Pitch Range Detector 🎶**

Descoperă cu precizie gama ta vocală sau instrumentală!
Încarcă un fișier audio, apasă „Analizează” și vizualizează notele extreme, frecvențele și intervalul muzical.

Aplicația funcționează complet offline și este creată special pentru cântăreți, profesori de muzică și ingineri de sunet care doresc o analiză rapidă și intuitivă.

Dezvoltată cu pasiune în Python ❤️

Versiune: 1.0
Funcționalitate: Tool offline pentru analiza de pitch și determinarea gamei vocale/instrumentale.

Tehnologii utilizate:
• Framework: PyQt5
• Analiză audio: Librosa
• Formate compatibile: WAV, MP3, FLAC, OGG

Open-source | Creat de Finimus
🌐 github.com/Finimus

© 2025 – Finimus

## Project Overview

**Pitch Range Detector** is a Windows desktop application for offline pitch range detection and audio frequency analysis. Built with PyQt5 for the GUI and librosa for audio processing, it analyzes vocal and instrumental recordings to determine frequency ranges and convert them to musical notes.

**Tech Stack**: Python 3.8+, PyQt5 (GUI), librosa (audio processing), numpy (numerical computation)

## Development Commands

### Setup
```powershell
# Install all dependencies
pip install -r requirements.txt
```

### Running the Application
```powershell
# Run the GUI application
python main.py
```

### Building Executables
```powershell
# Build standalone .exe (recommended - uses spec file)
pyinstaller PitchRangeDetector.spec

# Alternative: Build with command line options
pyinstaller --name="PitchRangeDetector" --windowed --onefile --icon=icon.ico main.py

# Build with separate files (faster startup)
pyinstaller --name="PitchRangeDetector" --windowed --icon=icon.ico main.py
```

**Output locations**:
- One-file build: `dist\PitchRangeDetector.exe`
- Directory build: `dist\PitchRangeDetector\PitchRangeDetector.exe`

## Architecture

### Core Components

**main.py**: PyQt5 GUI application
- `PitchRangeDetectorApp`: Main window with dark theme UI
- `AnalysisThread`: Background worker thread (QThread) for non-blocking audio analysis
- UI manages file selection, analysis triggering, and results display
- Uses signals/slots pattern for thread-safe communication

**audio_analyzer.py**: Audio processing module
- `AudioAnalyzer`: Core pitch detection engine
- `load_audio()`: Loads audio files using librosa (preserves original sample rate)
- `detect_pitch()`: Uses librosa's pYIN algorithm for robust pitch detection
  - Range: C2 (~65 Hz) to C7 (~2093 Hz) - covers human voice and most instruments
  - Returns frequencies and confidence scores, filters out non-voiced frames
- `hz_to_note()`: Converts Hz to musical notation (e.g., 440 Hz → A4)
- `analyze_audio()`: Full pipeline returning min/max/median frequencies with note conversions

### Threading Model

The application uses PyQt5's QThread to prevent UI freezing during audio analysis:
1. User clicks "Analizează" button
2. `AnalysisThread` spawns and runs `AudioAnalyzer.analyze_audio()` in background
3. Thread emits `finished` signal with results or `error` signal on failure
4. Main thread updates UI labels with results

### Audio Processing Pipeline

1. **Load**: `librosa.load()` converts audio to mono, preserves sample rate
2. **Pitch Detection**: `librosa.pyin()` detects fundamental frequency per frame
3. **Filtering**: Remove NaN values (non-voiced frames)
4. **Statistics**: Calculate min/max/median frequencies and mean confidence
5. **Conversion**: Transform Hz values to musical note notation using MIDI note numbers

### PyInstaller Configuration

`PitchRangeDetector.spec` includes:
- Hidden imports for librosa, scipy, numba, soundfile dependencies
- Excludes unnecessary packages (matplotlib, tkinter, pandas) to reduce size
- Windowed mode (`console=False`) for clean GUI launch
- Expected output: 200-400 MB executable (large due to scientific libraries)

## Important Constraints

- **Windows-only**: UI is optimized for Windows 10/11 (Segoe UI fonts, Fusion style)
- **No testing framework**: There are no unit tests in this project
- **Monophonic sources**: pYIN algorithm works best with single-pitch sources (voice, melodic instruments); struggles with polyphonic content (piano chords)
- **Audio quality dependent**: Requires clear recordings without excessive noise for accurate detection
- **Romanian UI**: All user-facing text is in Romanian

## Supported Audio Formats

WAV, MP3, OGG, FLAC (handled by librosa + soundfile/audioread)
