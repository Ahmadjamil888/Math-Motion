"""
Beat Detection
Detects beats and tempo in audio using librosa.
"""

import librosa
import numpy as np
from typing import List, Tuple, Dict
from dataclasses import dataclass


@dataclass
class BeatInfo:
    """Information about detected beats."""
    tempo: float
    beats: np.ndarray
    beat_frames: np.ndarray
    onset_envelope: np.ndarray
    onset_times: np.ndarray


class BeatDetector:
    """Detects beats and rhythmic features in audio."""
    
    def __init__(self):
        self.current_beat_info = None
    
    def detect_beats(self, audio: np.ndarray, sr: int, 
                    hop_length: int = 512, 
                    start_bpm: float = 120.0) -> BeatInfo:
        """
        Detect beats in audio using librosa.
        
        Args:
            audio: Audio data array
            sr: Sample rate
            hop_length: Hop length for onset detection
            start_bpm: Starting BPM for tempo estimation
            
        Returns:
            BeatInfo object with beat information
        """
        # Compute onset envelope
        onset_envelope = librosa.onset.onset_strength(y=audio, sr=sr, hop_length=hop_length)
        
        # Detect tempo and beats
        tempo, beat_frames = librosa.beat.beat_track(onset_envelope=onset_envelope, 
                                                     sr=sr, hop_length=hop_length,
                                                     start_bpm=start_bpm)
        
        # Convert beat frames to times
        beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)
        
        # Get onset times
        onset_frames = librosa.onset.onset_detect(onset_envelope=onset_envelope,
                                                sr=sr, hop_length=hop_length)
        onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)
        
        beat_info = BeatInfo(
            tempo=float(tempo),
            beats=beat_times,
            beat_frames=beat_frames,
            onset_envelope=onset_envelope,
            onset_times=onset_times
        )
        
        self.current_beat_info = beat_info
        return beat_info
    
    def get_beat_intervals(self, beat_info: BeatInfo) -> List[float]:
        """
        Get time intervals between consecutive beats.
        
        Args:
            beat_info: BeatInfo object
            
        Returns:
            List of time intervals between beats
        """
        if len(beat_info.beats) < 2:
            return []
        
        intervals = np.diff(beat_info.beats)
        return intervals.tolist()
    
    def get_beat_strength(self, beat_info: BeatInfo, window_size: int = 5) -> np.ndarray:
        """
        Calculate beat strength based on onset envelope.
        
        Args:
            beat_info: BeatInfo object
            window_size: Window size for smoothing
            
        Returns:
            Array of beat strengths
        """
        if len(beat_info.beat_frames) == 0:
            return np.array([])
        
        # Sample onset envelope at beat frames
        beat_strengths = beat_info.onset_envelope[beat_info.beat_frames]
        
        # Normalize
        if len(beat_strengths) > 0 and np.max(beat_strengths) > 0:
            beat_strengths = beat_strengths / np.max(beat_strengths)
        
        return beat_strengths
    
    def detect_downbeats(self, beat_info: BeatInfo, meter: int = 4) -> np.ndarray:
        """
        Detect downbeats (first beat of each measure).
        
        Args:
            beat_info: BeatInfo object
            meter: Time signature (4 for 4/4, 3 for 3/4, etc.)
            
        Returns:
            Array of downbeat times
        """
        if len(beat_info.beats) < meter:
            return np.array([])
        
        # Every meter-th beat is a downbeat
        downbeats = beat_info.beats[::meter]
        return downbeats
    
    def segment_by_beats(self, audio: np.ndarray, sr: int, 
                       beat_info: BeatInfo) -> List[np.ndarray]:
        """
        Segment audio by beats.
        
        Args:
            audio: Audio data
            sr: Sample rate
            beat_info: BeatInfo object
            
        Returns:
            List of audio segments for each beat
        """
        segments = []
        
        for i in range(len(beat_info.beats) - 1):
            start_sample = int(beat_info.beats[i] * sr)
            end_sample = int(beat_info.beats[i + 1] * sr)
            segment = audio[start_sample:end_sample]
            segments.append(segment)
        
        # Add final segment
        if len(beat_info.beats) > 0:
            start_sample = int(beat_info.beats[-1] * sr)
            segments.append(audio[start_sample:])
        
        return segments
    
    def get_beat_phase(self, time: float, beat_info: BeatInfo) -> float:
        """
        Get phase within beat cycle for a given time.
        
        Args:
            time: Time in seconds
            beat_info: BeatInfo object
            
        Returns:
            Phase value (0.0 to 1.0) within beat cycle
        """
        if len(beat_info.beats) < 2:
            return 0.0
        
        # Find the beat interval containing this time
        beat_interval = 60.0 / beat_info.tempo
        phase = (time % beat_interval) / beat_interval
        
        return phase
    
    def visualize_beats(self, beat_info: BeatInfo, audio: np.ndarray, sr: int):
        """
        Create a simple visualization of beats (for debugging).
        
        Args:
            beat_info: BeatInfo object
            audio: Audio data
            sr: Sample rate
        """
        import matplotlib.pyplot as plt
        
        plt.figure(figsize=(12, 4))
        
        # Plot waveform
        librosa.display.waveshow(audio, sr=sr, alpha=0.5)
        
        # Plot beats
        for beat in beat_info.beats:
            plt.axvline(x=beat, color='r', linestyle='--', alpha=0.7)
        
        plt.title(f"Waveform with Beats (Tempo: {beat_info.tempo:.1f} BPM)")
        plt.xlabel("Time (s)")
        plt.tight_layout()
        plt.show()
    
    def get_rhythm_pattern(self, beat_info: BeatInfo, pattern_length: int = 16) -> List[int]:
        """
        Extract a rhythmic pattern from beats.
        
        Args:
            beat_info: BeatInfo object
            pattern_length: Length of pattern in beats
            
        Returns:
            List representing rhythm pattern (1 for beat, 0 for no beat)
        """
        if len(beat_info.beats) == 0:
            return [0] * pattern_length
        
        # Create a binary pattern based on onset strength
        pattern = []
        for i in range(pattern_length):
            if i < len(beat_info.beat_frames):
                strength = beat_info.onset_envelope[beat_info.beat_frames[i]]
                pattern.append(1 if strength > 0.5 else 0)
            else:
                pattern.append(0)
        
        return pattern
    
    def clear(self):
        """Clear current beat information."""
        self.current_beat_info = None
