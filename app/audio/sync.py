"""
Audio Sync
Synchronizes animation events with audio features (beats, energy, etc.).
"""

import numpy as np
from typing import List, Dict, Callable, Optional, Tuple
from dataclasses import dataclass
from .beat_detection import BeatInfo
from .energy import EnergyInfo


@dataclass
class SyncEvent:
    """Represents a synchronized animation event."""
    time: float
    event_type: str
    intensity: float
    metadata: Dict


@dataclass
class Timeline:
    """Timeline for synchronized animation events."""
    events: List[SyncEvent]
    duration: float
    
    def add_event(self, event: SyncEvent):
        """Add an event to the timeline."""
        self.events.append(event)
        self.events.sort(key=lambda e: e.time)
    
    def get_events_at_time(self, time: float, window: float = 0.1) -> List[SyncEvent]:
        """Get events within a time window."""
        return [e for e in self.events if abs(e.time - time) < window]
    
    def get_events_in_range(self, start: float, end: float) -> List[SyncEvent]:
        """Get events within a time range."""
        return [e for e in self.events if start <= e.time <= end]


class AudioSync:
    """Synchronizes animation with audio features."""
    
    def __init__(self):
        self.timeline = Timeline(events=[], duration=0.0)
        self.beat_info = None
        self.energy_info = None
        self.sync_callbacks = {}
    
    def load_audio_features(self, beat_info: BeatInfo, energy_info: EnergyInfo):
        """
        Load audio features for synchronization.
        
        Args:
            beat_info: BeatInfo object from beat detection
            energy_info: EnergyInfo object from energy analysis
        """
        self.beat_info = beat_info
        self.energy_info = energy_info
        
        # Set timeline duration
        if beat_info and len(beat_info.beats) > 0:
            self.timeline.duration = float(beat_info.beats[-1]) + 1.0
        elif energy_info and len(energy_info.time_frames) > 0:
            self.timeline.duration = float(energy_info.time_frames[-1]) + 1.0
    
    def create_beat_timeline(self, beat_info: BeatInfo, 
                           event_types: List[str] = None) -> Timeline:
        """
        Create timeline based on beats.
        
        Args:
            beat_info: BeatInfo object
            event_types: List of event types to use (default: ['beat'])
            
        Returns:
            Timeline with beat events
        """
        if event_types is None:
            event_types = ['beat']
        
        timeline = Timeline(events=[], duration=0.0)
        
        for i, beat_time in enumerate(beat_info.beats):
            # Calculate intensity based on onset strength
            if i < len(beat_info.onset_envelope):
                intensity = float(beat_info.onset_envelope[i])
            else:
                intensity = 0.5
            
            # Cycle through event types
            event_type = event_types[i % len(event_types)]
            
            event = SyncEvent(
                time=float(beat_time),
                event_type=event_type,
                intensity=intensity,
                metadata={'beat_index': i}
            )
            
            timeline.add_event(event)
        
        # Set duration
        if len(beat_info.beats) > 0:
            timeline.duration = float(beat_info.beats[-1]) + 1.0
        
        return timeline
    
    def create_energy_timeline(self, energy_info: EnergyInfo,
                              threshold: float = 0.5,
                              event_type: str = 'energy_peak') -> Timeline:
        """
        Create timeline based on energy peaks.
        
        Args:
            energy_info: EnergyInfo object
            threshold: Energy threshold for event creation
            event_type: Type of event to create
            
        Returns:
            Timeline with energy events
        """
        from .energy import EnergyAnalyzer
        
        analyzer = EnergyAnalyzer()
        peaks = analyzer.detect_energy_peaks(energy_info, threshold=threshold)
        
        timeline = Timeline(events=[], duration=0.0)
        
        for peak_idx in peaks:
            if peak_idx < len(energy_info.time_frames):
                time = float(energy_info.time_frames[peak_idx])
                intensity = float(energy_info.rms_energy[peak_idx])
                
                # Normalize intensity
                if np.max(energy_info.rms_energy) > 0:
                    intensity = intensity / np.max(energy_info.rms_energy)
                
                event = SyncEvent(
                    time=time,
                    event_type=event_type,
                    intensity=intensity,
                    metadata={'peak_index': peak_idx}
                )
                
                timeline.add_event(event)
        
        # Set duration
        if len(energy_info.time_frames) > 0:
            timeline.duration = float(energy_info.time_frames[-1]) + 1.0
        
        return timeline
    
    def create_combined_timeline(self, beat_info: BeatInfo, 
                                energy_info: EnergyInfo,
                                beat_weight: float = 0.7,
                                energy_weight: float = 0.3) -> Timeline:
        """
        Create combined timeline from beats and energy.
        
        Args:
            beat_info: BeatInfo object
            energy_info: EnergyInfo object
            beat_weight: Weight for beat events
            energy_weight: Weight for energy events
            
        Returns:
            Combined timeline
        """
        beat_timeline = self.create_beat_timeline(beat_info)
        energy_timeline = self.create_energy_timeline(energy_info, threshold=0.3)
        
        # Combine events
        combined_events = []
        
        # Add beat events with adjusted intensity
        for event in beat_timeline.events:
            event.intensity *= beat_weight
            combined_events.append(event)
        
        # Add energy events with adjusted intensity
        for event in energy_timeline.events:
            event.intensity *= energy_weight
            event.event_type = 'energy'
            combined_events.append(event)
        
        # Sort by time
        combined_events.sort(key=lambda e: e.time)
        
        # Merge events that are very close in time
        merged_events = self._merge_nearby_events(combined_events, time_threshold=0.05)
        
        timeline = Timeline(events=merged_events, duration=max(beat_timeline.duration, energy_timeline.duration))
        return timeline
    
    def _merge_nearby_events(self, events: List[SyncEvent], 
                           time_threshold: float = 0.05) -> List[SyncEvent]:
        """Merge events that are very close in time."""
        if not events:
            return []
        
        merged = [events[0]]
        
        for event in events[1:]:
            last_event = merged[-1]
            
            if event.time - last_event.time < time_threshold:
                # Merge: combine intensities
                last_event.intensity = max(last_event.intensity, event.intensity)
                last_event.metadata.update(event.metadata)
            else:
                merged.append(event)
        
        return merged
    
    def register_sync_callback(self, event_type: str, callback: Callable[[SyncEvent], None]):
        """
        Register a callback for a specific event type.
        
        Args:
            event_type: Type of event (e.g., 'beat', 'energy_peak')
            callback: Function to call when event occurs
        """
        self.sync_callbacks[event_type] = callback
    
    def process_timeline(self, timeline: Timeline, 
                        current_time: float,
                        callback: Callable[[SyncEvent], None] = None):
        """
        Process timeline events for a given time.
        
        Args:
            timeline: Timeline to process
            current_time: Current time in seconds
            callback: Optional callback function for events
        """
        events = timeline.get_events_at_time(current_time, window=0.1)
        
        for event in events:
            # Call registered callback if exists
            if event.event_type in self.sync_callbacks:
                self.sync_callbacks[event.event_type](event)
            
            # Call provided callback if exists
            if callback:
                callback(event)
    
    def get_sync_value(self, time: float, value_type: str = 'energy') -> float:
        """
        Get synchronized value at a specific time.
        
        Args:
            time: Time in seconds
            value_type: Type of value ('energy', 'beat_phase', 'intensity')
            
        Returns:
            Synchronized value (0.0 to 1.0)
        """
        if value_type == 'energy' and self.energy_info:
            from .energy import EnergyAnalyzer
            analyzer = EnergyAnalyzer()
            return analyzer.get_energy_at_time(time, self.energy_info.time_frames)
        
        elif value_type == 'beat_phase' and self.beat_info:
            from .beat_detection import BeatDetector
            detector = BeatDetector()
            return detector.get_beat_phase(time, self.beat_info)
        
        elif value_type == 'intensity':
            # Get intensity from nearest event
            events = self.timeline.get_events_at_time(time, window=0.2)
            if events:
                return max(e.intensity for e in events)
            return 0.0
        
        return 0.0
    
    def create_animation_keyframes(self, timeline: Timeline, 
                                  property_name: str,
                                  value_range: Tuple[float, float] = (0.0, 1.0)) -> Dict[float, float]:
        """
        Create animation keyframes from timeline.
        
        Args:
            timeline: Timeline with events
            property_name: Name of property to animate
            value_range: Range of values (min, max)
            
        Returns:
            Dictionary mapping time to property value
        """
        keyframes = {}
        
        for event in timeline.events:
            # Map intensity to value range
            value = value_range[0] + event.intensity * (value_range[1] - value_range[0])
            keyframes[event.time] = value
        
        return keyframes
    
    def smooth_keyframes(self, keyframes: Dict[float, float],
                        smoothing_window: float = 0.1) -> Dict[float, float]:
        """
        Smooth keyframe values over time.
        
        Args:
            keyframes: Dictionary of time->value mappings
            smoothing_window: Time window for smoothing
            
        Returns:
            Smoothed keyframes dictionary
        """
        if not keyframes:
            return keyframes
        
        times = sorted(keyframes.keys())
        values = [keyframes[t] for t in times]
        
        # Convert to arrays for processing
        times_array = np.array(times)
        values_array = np.array(values)
        
        # Simple moving average
        smoothed_values = np.zeros_like(values_array)
        for i, time in enumerate(times):
            # Find nearby keyframes
            nearby_times = times_array[(times_array >= time - smoothing_window) & 
                                      (times_array <= time + smoothing_window)]
            if len(nearby_times) > 0:
                nearby_values = [keyframes[t] for t in nearby_times]
                smoothed_values[i] = np.mean(nearby_values)
            else:
                smoothed_values[i] = values_array[i]
        
        return {float(times_array[i]): float(smoothed_values[i]) 
                for i in range(len(times_array))}
    
    def export_timeline(self, timeline: Timeline, format: str = 'json') -> str:
        """
        Export timeline to a format.
        
        Args:
            timeline: Timeline to export
            format: Export format ('json', 'csv')
            
        Returns:
            String representation of timeline
        """
        if format == 'json':
            import json
            events_data = [
                {
                    'time': event.time,
                    'type': event.event_type,
                    'intensity': event.intensity,
                    'metadata': event.metadata
                }
                for event in timeline.events
            ]
            return json.dumps({
                'duration': timeline.duration,
                'events': events_data
            }, indent=2)
        
        elif format == 'csv':
            import io
            import csv
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['time', 'event_type', 'intensity', 'metadata'])
            for event in timeline.events:
                writer.writerow([event.time, event.event_type, event.intensity, str(event.metadata)])
            return output.getvalue()
        
        return str(timeline)
    
    def clear(self):
        """Clear synchronization data."""
        self.timeline = Timeline(events=[], duration=0.0)
        self.beat_info = None
        self.energy_info = None
        self.sync_callbacks.clear()
