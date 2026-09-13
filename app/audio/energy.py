"""
Energy Analyzer
Analyzes energy and spectral features of audio for animation synchronization.
"""

import librosa
import numpy as np
from typing import Tuple, List, Dict
from dataclasses import dataclass


@dataclass
class EnergyInfo:
    """Information about audio energy analysis."""
    rms_energy: np.ndarray
    spectral_centroid: np.ndarray
    spectral_bandwidth: np.ndarray
    spectral_rolloff: np.ndarray
    zero_crossing_rate: np.ndarray
    mfcc: np.ndarray
    chroma: np.ndarray
    time_frames: np.ndarray


class EnergyAnalyzer:
    """Analyzes energy and spectral features for animation control."""
    
    def __init__(self):
        self.current_energy_info = None
        self.hop_length = 512
        self.n_mfcc = 13
        self.n_fft = 2048
    
    def analyze_energy(self, audio: np.ndarray, sr: int) -> EnergyInfo:
        """
        Perform comprehensive energy analysis of audio.
        
        Args:
            audio: Audio data array
            sr: Sample rate
            
        Returns:
            EnergyInfo object with analysis results
        """
        # RMS energy
        rms_energy = librosa.feature.rms(y=audio, hop_length=self.hop_length)[0]
        
        # Spectral features
        spectral_centroid = librosa.feature.spectral_centroid(y=audio, sr=sr, 
                                                            hop_length=self.hop_length)[0]
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=audio, sr=sr,
                                                              hop_length=self.hop_length)[0]
        spectral_rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr,
                                                          hop_length=self.hop_length)[0]
        
        # Zero crossing rate
        zero_crossing_rate = librosa.feature.zero_crossing_rate(audio, hop_length=self.hop_length)[0]
        
        # MFCCs
        mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=self.n_mfcc,
                                    hop_length=self.hop_length)
        
        # Chroma features
        chroma = librosa.feature.chroma_stft(y=audio, sr=sr, hop_length=self.hop_length)
        
        # Time frames
        time_frames = librosa.frames_to_time(np.arange(len(rms_energy)), 
                                            sr=sr, hop_length=self.hop_length)
        
        energy_info = EnergyInfo(
            rms_energy=rms_energy,
            spectral_centroid=spectral_centroid,
            spectral_bandwidth=spectral_bandwidth,
            spectral_rolloff=spectral_rolloff,
            zero_crossing_rate=zero_crossing_rate,
            mfcc=mfcc,
            chroma=chroma,
            time_frames=time_frames
        )
        
        self.current_energy_info = energy_info
        return energy_info
    
    def get_energy_at_time(self, time: float, sr: int) -> float:
        """
        Get energy value at a specific time.
        
        Args:
            time: Time in seconds
            sr: Sample rate
            
        Returns:
            Energy value at given time
        """
        if self.current_energy_info is None:
            return 0.0
        
        frame = int(time * sr / self.hop_length)
        
        if frame < len(self.current_energy_info.rms_energy):
            return float(self.current_energy_info.rms_energy[frame])
        
        return 0.0
    
    def get_normalized_energy(self, energy_info: EnergyInfo) -> np.ndarray:
        """
        Get normalized energy values (0.0 to 1.0).
        
        Args:
            energy_info: EnergyInfo object
            
        Returns:
            Normalized energy array
        """
        energy = energy_info.rms_energy
        if np.max(energy) > 0:
            return energy / np.max(energy)
        return energy
    
    def get_energy_envelope(self, energy_info: EnergyInfo, 
                          attack_time: float = 0.1, 
                          release_time: float = 0.3) -> np.ndarray:
        """
        Get smoothed energy envelope with attack and release.
        
        Args:
            energy_info: EnergyInfo object
            attack_time: Attack time in seconds
            release_time: Release time in seconds
            
        Returns:
            Smoothed energy envelope
        """
        energy = energy_info.rms_energy
        
        # Simple smoothing using exponential moving average
        alpha = 0.1
        smoothed = np.zeros_like(energy)
        smoothed[0] = energy[0]
        
        for i in range(1, len(energy)):
            smoothed[i] = alpha * energy[i] + (1 - alpha) * smoothed[i-1]
        
        return smoothed
    
    def get_frequency_bands(self, audio: np.ndarray, sr: int,
                          bands: List[Tuple[str, Tuple[int, int]]]) -> Dict[str, np.ndarray]:
        """
        Get energy in different frequency bands.
        
        Args:
            audio: Audio data
            sr: Sample rate
            bands: List of (name, (low_freq, high_freq)) tuples
            
        Returns:
            Dictionary mapping band names to energy arrays
        """
        stft = librosa.stft(audio, hop_length=self.hop_length, n_fft=self.n_fft)
        magnitude = np.abs(stft)
        
        freqs = librosa.fft_frequencies(sr=sr, n_fft=self.n_fft)
        band_energies = {}
        
        for band_name, (low_freq, high_freq) in bands:
            # Find frequency indices
            low_idx = np.searchsorted(freqs, low_freq)
            high_idx = np.searchsorted(freqs, high_freq)
            
            # Sum energy in band
            band_energy = np.sum(magnitude[low_idx:high_idx, :], axis=0)
            band_energies[band_name] = band_energy
        
        return band_energies
    
    def get_spectral_contrast(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Get spectral contrast features.
        
        Args:
            audio: Audio data
            sr: Sample rate
            
        Returns:
            Spectral contrast array
        """
        contrast = librosa.feature.spectral_contrast(y=audio, sr=sr,
                                                     hop_length=self.hop_length)
        return contrast
    
    def get_tonnetz(self, audio: np.ndarray, sr: int) -> np.ndarray:
        """
        Get tonal centroid features (tonnetz).
        
        Args:
            audio: Audio data
            sr: Sample rate
            
        Returns:
            Tonnetz features array
        """
        tonnetz = librosa.feature.tonnetz(y=audio, sr=sr, hop_length=self.hop_length)
        return tonnetz
    
    def detect_energy_peaks(self, energy_info: EnergyInfo, 
                           threshold: float = 0.5,
                           min_distance: int = 10) -> np.ndarray:
        """
        Detect peaks in energy envelope.
        
        Args:
            energy_info: EnergyInfo object
            threshold: Threshold for peak detection (normalized)
            min_distance: Minimum distance between peaks in frames
            
        Returns:
            Array of peak frame indices
        """
        from scipy.signal import find_peaks
        
        energy = self.get_normalized_energy(energy_info)
        peaks, _ = find_peaks(energy, height=threshold, distance=min_distance)
        
        return peaks
    
    def get_energy_statistics(self, energy_info: EnergyInfo) -> Dict[str, float]:
        """
        Get statistical measures of energy.
        
        Args:
            energy_info: EnergyInfo object
            
        Returns:
            Dictionary with energy statistics
        """
        energy = energy_info.rms_energy
        
        return {
            'mean': float(np.mean(energy)),
            'std': float(np.std(energy)),
            'max': float(np.max(energy)),
            'min': float(np.min(energy)),
            'median': float(np.median(energy)),
            'percentile_25': float(np.percentile(energy, 25)),
            'percentile_75': float(np.percentile(energy, 75))
        }
    
    def get_dynamics_profile(self, energy_info: EnergyInfo, 
                           window_size: int = 50) -> Dict[str, np.ndarray]:
        """
        Get dynamic profile (attack, decay, sustain, release) analysis.
        
        Args:
            energy_info: EnergyInfo object
            window_size: Size of analysis window
            
        Returns:
            Dictionary with dynamic profile arrays
        """
        energy = energy_info.rms_energy
        
        # Calculate derivatives
        first_derivative = np.gradient(energy)
        second_derivative = np.gradient(first_derivative)
        
        return {
            'energy': energy,
            'attack': np.maximum(first_derivative, 0),
            'decay': np.maximum(-first_derivative, 0),
            'curvature': second_derivative
        }
    
    def clear(self):
        """Clear current energy information."""
        self.current_energy_info = None
