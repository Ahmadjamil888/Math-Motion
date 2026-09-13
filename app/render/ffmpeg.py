"""
FFmpeg Processor
Handles video processing, audio merging, and final video output using FFmpeg.
"""

import subprocess
import os
from pathlib import Path
from typing import Dict, Optional, List
from dataclasses import dataclass


@dataclass
class FFmpegConfig:
    """Configuration for FFmpeg processing."""
    video_codec: str = "libx264"
    audio_codec: str = "aac"
    video_bitrate: str = "5M"
    audio_bitrate: str = "192k"
    preset: str = "medium"  # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
    crf: int = 23  # Constant Rate Factor (0-51, lower is better quality)
    sample_rate: int = 44100
    channels: int = 2


@dataclass
class ProcessingResult:
    """Result of FFmpeg processing operation."""
    success: bool
    output_path: Optional[str]
    duration: float
    file_size: int
    error_message: Optional[str] = None


class FFmpegProcessor:
    """Handles FFmpeg video processing operations."""
    
    def __init__(self, config: FFmpegConfig = None):
        if config is None:
            config = FFmpegConfig()
        
        self.config = config
        self.ffmpeg_available = self._check_ffmpeg_available()
    
    def _check_ffmpeg_available(self) -> bool:
        """Check if FFmpeg is available on the system."""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def combine_video_audio(self, video_path: str, audio_path: str, 
                          output_path: str) -> ProcessingResult:
        """
        Combine video and audio files.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path for output file
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        
        # Build FFmpeg command
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", self.config.video_codec,
            "-c:a", self.config.audio_codec,
            "-b:v", self.config.video_bitrate,
            "-b:a", self.config.audio_bitrate,
            "-preset", self.config.preset,
            "-crf", str(self.config.crf),
            "-ar", str(self.config.sample_rate),
            "-ac", str(self.config.channels),
            "-shortest",  # Match duration of shortest input
            "-y",  # Overwrite output file
            output_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0 and os.path.exists(output_path):
                duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except subprocess.TimeoutExpired:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="Processing timed out"
            )
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def extract_audio(self, video_path: str, output_path: str) -> ProcessingResult:
        """
        Extract audio from video file.
        
        Args:
            video_path: Path to video file
            output_path: Path for output audio file
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        cmd = [
            "ffmpeg",
            "-i", video_path,
            "-vn",  # No video
            "-acodec", self.config.audio_codec,
            "-b:a", self.config.audio_bitrate,
            "-ar", str(self.config.sample_rate),
            "-ac", str(self.config.channels),
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_path):
                duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def add_audio_to_video(self, video_path: str, audio_path: str,
                          output_path: str, replace_audio: bool = True) -> ProcessingResult:
        """
        Add audio track to video file.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Path for output file
            replace_audio: Whether to replace existing audio
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        # Build command based on whether we're replacing or adding audio
        if replace_audio:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",  # Copy video stream without re-encoding
                "-c:a", self.config.audio_codec,
                "-map", "0:v:0",  # Use video from first input
                "-map", "1:a:0",  # Use audio from second input
                "-shortest",
                "-y",
                output_path
            ]
        else:
            cmd = [
                "ffmpeg",
                "-i", video_path,
                "-i", audio_path,
                "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first",
                "-c:v", "copy",
                "-y",
                output_path
            ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_path):
                duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def trim_video(self, input_path: str, output_path: str,
                  start_time: float, duration: float) -> ProcessingResult:
        """
        Trim video to specific time range.
        
        Args:
            input_path: Path to input video
            output_path: Path for output video
            start_time: Start time in seconds
            duration: Duration in seconds
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        cmd = [
            "ffmpeg",
            "-ss", str(start_time),
            "-i", input_path,
            "-t", str(duration),
            "-c:v", self.config.video_codec,
            "-c:a", self.config.audio_codec,
            "-preset", self.config.preset,
            "-crf", str(self.config.crf),
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_path):
                video_duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=video_duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def resize_video(self, input_path: str, output_path: str,
                    width: int, height: int) -> ProcessingResult:
        """
        Resize video to specific dimensions.
        
        Args:
            input_path: Path to input video
            output_path: Path for output video
            width: Target width
            height: Target height
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vf", f"scale={width}:{height}",
            "-c:v", self.config.video_codec,
            "-preset", self.config.preset,
            "-crf", str(self.config.crf),
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_path):
                duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def change_frame_rate(self, input_path: str, output_path: str,
                         frame_rate: int) -> ProcessingResult:
        """
        Change video frame rate.
        
        Args:
            input_path: Path to input video
            output_path: Path for output video
            frame_rate: Target frame rate
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-r", str(frame_rate),
            "-c:v", self.config.video_codec,
            "-preset", self.config.preset,
            "-crf", str(self.config.crf),
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0 and os.path.exists(output_path):
                duration, file_size = self._get_media_info(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=duration,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def _get_media_info(self, file_path: str) -> tuple[float, int]:
        """
        Get media file duration and size.
        
        Args:
            file_path: Path to media file
            
        Returns:
            Tuple of (duration, file_size)
        """
        try:
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Get duration using ffprobe
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1",
                file_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                duration = float(result.stdout.strip())
                return duration, file_size
        
        except Exception:
            pass
        
        return 0.0, 0
    
    def get_video_info(self, video_path: str) -> Dict[str, any]:
        """
        Get detailed information about a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video information
        """
        if not self.ffmpeg_available:
            return {}
        
        try:
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_entries", "stream=width,height,codec_name,r_frame_rate,duration",
                "-show_entries", "format=duration,size,bit_rate",
                "-of", "json",
                video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                import json
                return json.loads(result.stdout)
        
        except Exception:
            pass
        
        return {}
    
    def create_thumbnail(self, video_path: str, output_path: str,
                       timestamp: float = 0.0) -> ProcessingResult:
        """
        Create thumbnail from video at specific timestamp.
        
        Args:
            video_path: Path to video file
            output_path: Path for thumbnail image
            timestamp: Timestamp to capture thumbnail from
            
        Returns:
            ProcessingResult with operation information
        """
        if not self.ffmpeg_available:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message="FFmpeg is not available"
            )
        
        cmd = [
            "ffmpeg",
            "-ss", str(timestamp),
            "-i", video_path,
            "-vframes", "1",
            "-q:v", "2",
            "-y",
            output_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                
                return ProcessingResult(
                    success=True,
                    output_path=output_path,
                    duration=0.0,
                    file_size=file_size
                )
            else:
                return ProcessingResult(
                    success=False,
                    output_path=None,
                    duration=0.0,
                    file_size=0,
                    error_message=result.stderr if result.stderr else "Unknown error"
                )
        
        except Exception as e:
            return ProcessingResult(
                success=False,
                output_path=None,
                duration=0.0,
                file_size=0,
                error_message=str(e)
            )
    
    def set_config(self, config: FFmpegConfig):
        """
        Set FFmpeg configuration.
        
        Args:
            config: FFmpegConfig object
        """
        self.config = config
    
    def clear(self):
        """Clear processor state."""
        pass
