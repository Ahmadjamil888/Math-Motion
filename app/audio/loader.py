"""
Audio Loader
Handles loading and basic processing of audio files.
"""

import librosa
import numpy as np
import soundfile as sf
from typing import Tuple, Optional, Dict
from pathlib import Path


class AudioLoader:
    """Loads and processes audio files for analysis."""
    
    def __init__(self):
        self.current_audio = None
        self.current_sr = None
        self.current_duration = None
        self.audio_path = None
    
    def load_audio(self, file_path: str, sr: Optional[int] = None) -> Tuple[np.ndarray, int]:
        """
        Load audio file using librosa.
        
        Args:
            file_path: Path to audio file
            sr: Sample rate (None for original rate)
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            audio_data, sample_rate = librosa.load(file_path, sr=sr)
            
            self.current_audio = audio_data
            self.current_sr = sample_rate
            self.current_duration = len(audio_data) / sample_rate
            self.audio_path = file_path
            
            return audio_data, sample_rate
        except Exception as e:
            print(f"Error loading audio file {file_path}: {e}")
            return np.array([]), 44100
    
    def load_with_soundfile(self, file_path: str) -> Tuple[np.ndarray, int]:
        """
        Load audio file using soundfile (preserves original format).
        
        Args:
            file_path: Path to audio file
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        try:
            audio_data, sample_rate = sf.read(file_path)
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            self.current_audio = audio_data
            self.current_sr = sample_rate
            self.current_duration = len(audio_data) / sample_rate
            self.audio_path = file_path
            
            return audio_data, sample_rate
        except Exception as e:
            print(f"Error loading audio file with soundfile {file_path}: {e}")
            return np.array([]), 44100
    
    def get_audio_info(self) -> Dict[str, any]:
        """
        Get information about currently loaded audio.
        
        Returns:
            Dictionary with audio information
        """
        if self.current_audio is None:
            return {}
        
        return {
            'duration': self.current_duration,
            'sample_rate': self.current_sr,
            'num_samples': len(self.current_audio),
            'channels': 1,  # We always convert to mono
            'file_path': self.audio_path
        }
    
    def get_segment(self, start_time: float, end_time: float) -> np.ndarray:
        """
        Extract a segment of audio by time.
        
        Args:
            start_time: Start time in seconds
            end_time: End time in seconds
            
        Returns:
            Audio segment as numpy array
        """
        if self.current_audio is None:
            return np.array([])
        
        start_sample = int(start_time * self.current_sr)
        end_sample = int(end_time * self.current_sr)
        
        return self.current_audio[start_sample:end_sample]
    
    def resample(self, target_sr: int) -> np.ndarray:
        """
        Resample current audio to target sample rate.
        
        Args:
            target_sr: Target sample rate
            
        Returns:
            Resampled audio data
        """
        if self.current_audio is None:
            return np.array([])
        
        if self.current_sr == target_sr:
            return self.current_audio
        
        resampled = librosa.resample(self.current_audio, orig_sr=self.current_sr, 
                                    target_sr=target_sr)
        self.current_audio = resampled
        self.current_sr = target_sr
        
        return resampled
    
    def trim_silence(self, threshold: float = 0.01) -> np.ndarray:
        """
        Remove silence from beginning and end of audio.
        
        Args:
            threshold: Amplitude threshold for silence detection
            
        Returns:
            Trimmed audio data
        """
        if self.current_audio is None:
            return np.array([])
        
        trimmed, _ = librosa.effects.trim(self.current_audio, 
                                         top_db=20 - 20 * np.log10(threshold))
        self.current_audio = trimmed
        self.current_duration = len(trimmed) / self.current_sr
        
        return trimmed
    
    def normalize(self, target_peak: float = 0.8) -> np.ndarray:
        """
        Normalize audio to target peak amplitude.
        
        Args:
            target_peak: Target peak amplitude (0.0 to 1.0)
            
        Returns:
            Normalized audio data
        """
        if self.current_audio is None:
            return np.array([])
        
        current_peak = np.max(np.abs(self.current_audio))
        if current_peak > 0:
            normalized = self.current_audio * (target_peak / current_peak)
            self.current_audio = normalized
            return normalized
        
        return self.current_audio
    
    def save_audio(self, output_path: str, format: str = 'wav'):
        """
        Save current audio to file.
        
        Args:
            output_path: Output file path
            format: Audio format (wav, mp3, etc.)
        """
        if self.current_audio is None:
            print("No audio loaded to save")
            return
        
        try:
            sf.write(output_path, self.current_audio, self.current_sr, format=format)
            print(f"Audio saved to {output_path}")
        except Exception as e:
            print(f"Error saving audio: {e}")
    
    def clear(self):
        """Clear current audio data."""
        self.current_audio = None
        self.current_sr = None
        self.current_duration = None
        self.audio_path = None
    
    def is_loaded(self) -> bool:
        """Check if audio is currently loaded."""
        return self.current_audio is not None
