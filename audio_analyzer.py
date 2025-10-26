"""
Audio Analysis Module
Pitch detection and frequency analysis using librosa
"""

import numpy as np
import librosa
import librosa.display


class AudioAnalyzer:
    """Analyzes audio files to detect pitch range and frequency information"""
    
    # Standard note names
    NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    
    def __init__(self):
        self.sample_rate = None
        self.audio_data = None
        
    def hz_to_note(self, frequency):
        """
        Convert frequency in Hz to musical note name with octave
        
        Args:
            frequency: Frequency in Hz
            
        Returns:
            String representation of note (e.g., 'A4', 'C#3')
        """
        if frequency <= 0:
            return "N/A"
            
        # A4 = 440 Hz is our reference
        # Calculate semitones from A4
        semitones_from_a4 = 12 * np.log2(frequency / 440.0)
        
        # A4 is the 9th note (index 9) in octave 4
        # Calculate the MIDI note number
        midi_note = 69 + round(semitones_from_a4)
        
        # Get octave and note name
        octave = (midi_note // 12) - 1
        note_index = midi_note % 12
        note_name = self.NOTE_NAMES[note_index]
        
        return f"{note_name}{octave}"
        
    def load_audio(self, file_path):
        """
        Load audio file
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            # Load audio file with librosa
            # sr=None preserves the original sample rate
            audio_data, sample_rate = librosa.load(file_path, sr=None, mono=True)
            
            self.audio_data = audio_data
            self.sample_rate = sample_rate
            
            return audio_data, sample_rate
        except Exception as e:
            raise Exception(f"Eroare la încărcarea fișierului audio: {str(e)}")
            
    def detect_pitch(self, audio_data, sample_rate):
        """
        Detect pitch using the pYIN algorithm (robust pitch detection)
        
        Args:
            audio_data: Audio time series
            sample_rate: Sample rate of audio
            
        Returns:
            Tuple of (frequencies, confidences) - both as numpy arrays
        """
        try:
            # Use pYIN for robust pitch detection
            # fmin and fmax define the expected pitch range (human voice + instruments)
            f0, voiced_flag, voiced_probs = librosa.pyin(
                audio_data,
                fmin=librosa.note_to_hz('C2'),  # ~65 Hz (low male voice)
                fmax=librosa.note_to_hz('C7'),  # ~2093 Hz (high soprano)
                sr=sample_rate,
                frame_length=2048
            )
            
            # Filter out non-voiced frames (NaN values)
            valid_indices = ~np.isnan(f0)
            frequencies = f0[valid_indices]
            confidences = voiced_probs[valid_indices]
            
            if len(frequencies) == 0:
                raise Exception("Nu s-au detectat frecvențe vocale/instrumentale în fișier")
                
            return frequencies, confidences
            
        except Exception as e:
            raise Exception(f"Eroare la detectarea pitch-ului: {str(e)}")
            
    def analyze_audio(self, file_path):
        """
        Complete audio analysis pipeline
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Dictionary with analysis results
        """
        # Load audio
        audio_data, sample_rate = self.load_audio(file_path)
        
        # Detect pitch
        frequencies, confidences = self.detect_pitch(audio_data, sample_rate)
        
        # Calculate statistics
        min_freq = np.min(frequencies)
        max_freq = np.max(frequencies)
        median_freq = np.median(frequencies)
        mean_confidence = np.mean(confidences) * 100  # Convert to percentage
        
        # Convert to notes
        min_note = self.hz_to_note(min_freq)
        max_note = self.hz_to_note(max_freq)
        median_note = self.hz_to_note(median_freq)
        
        # Prepare results
        results = {
            'min_freq': min_freq,
            'max_freq': max_freq,
            'median_freq': median_freq,
            'min_note': min_note,
            'max_note': max_note,
            'median_note': median_note,
            'confidence': mean_confidence,
            'num_samples': len(frequencies),
            'sample_rate': sample_rate,
            'duration': len(audio_data) / sample_rate
        }
        
        return results
        
    def get_frequency_range_info(self, min_note, max_note):
        """
        Get additional information about the frequency range
        
        Args:
            min_note: Minimum note (e.g., 'C3')
            max_note: Maximum note (e.g., 'G5')
            
        Returns:
            Dictionary with range classification info
        """
        # This could be extended to classify voice types or instrument ranges
        classifications = {
            'bass': (82.41, 329.63),      # E2 - E4
            'baritone': (98.00, 392.00),  # G2 - G4
            'tenor': (130.81, 523.25),    # C3 - C5
            'alto': (174.61, 698.46),     # F3 - F5
            'soprano': (261.63, 1046.50)  # C4 - C5
        }
        
        return classifications
