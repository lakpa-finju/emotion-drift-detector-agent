import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import json
import math

@dataclass
class EmotionalWavePoint:
    """Represents a single point in the emotional wave"""
    timestamp: datetime
    valence: float      # -1 to 1 (negative to positive)
    arousal: float      # 0 to 1 (low to high energy)
    dominance: float    # -1 to 1 (submissive to dominant)
    intensity: float    # 0 to 1 (weak to strong)
    
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp.isoformat(),
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "intensity": self.intensity
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'EmotionalWavePoint':
        return cls(
            timestamp=datetime.fromisoformat(data["timestamp"]),
            valence=data["valence"],
            arousal=data["arousal"],
            dominance=data["dominance"],
            intensity=data["intensity"]
        )

@dataclass
class WaveAnalysisResult:
    """Results from wave-based emotional analysis"""
    drift_score: float
    dominant_frequency: float
    amplitude_change: float
    phase_shift: float
    trend_direction: str
    stability_index: float
    emotional_volatility: float
    predicted_next_state: Dict[str, float]

class WaveBasedEmotionAnalyzer:
    """
    Wave-based emotional drift detection using signal processing techniques
    Based on the research that emotions follow wave-like patterns with:
    - Amplitude (intensity of emotional response)
    - Frequency (rate of emotional change)
    - Phase (timing of emotional peaks/troughs)
    """
    
    def __init__(self, window_size: int = 10):
        self.window_size = window_size
        self.emotional_history: List[EmotionalWavePoint] = []
    
    def add_emotional_point(self, emotion_point: EmotionalWavePoint):
        """Add a new emotional data point to the wave analysis"""
        self.emotional_history.append(emotion_point)
        
        # Keep only the most recent points within the window
        if len(self.emotional_history) > self.window_size * 2:
            self.emotional_history = self.emotional_history[-self.window_size * 2:]
    
    def extract_wave_features(self, dimension: str) -> Dict[str, float]:
        """Extract wave features (amplitude, frequency, phase) for a given emotional dimension"""
        if len(self.emotional_history) < 3:
            return {"amplitude": 0.0, "frequency": 0.0, "phase": 0.0}
        
        # Extract time series for the dimension
        values = [getattr(point, dimension) for point in self.emotional_history[-self.window_size:]]
        timestamps = [point.timestamp for point in self.emotional_history[-self.window_size:]]
        
        if len(values) < 3:
            return {"amplitude": 0.0, "frequency": 0.0, "phase": 0.0}
        
        # Convert to numpy arrays
        values = np.array(values)
        
        # Calculate amplitude (standard deviation as proxy for wave amplitude)
        amplitude = np.std(values)
        
        # Detrend the signal
        detrended = signal.detrend(values)
        
        # Calculate frequency using FFT
        if len(detrended) > 2:  # Need at least 3 points for meaningful FFT
            fft_vals = fft(detrended)
            freqs = fftfreq(len(detrended))
            
            # Find dominant frequency (excluding DC component)
            # Only consider positive frequencies and ensure we have valid range
            positive_freqs = fft_vals[1:len(fft_vals)//2]
            if len(positive_freqs) > 0:
                dominant_freq_idx = np.argmax(np.abs(positive_freqs)) + 1
                dominant_frequency = abs(freqs[dominant_freq_idx])
            else:
                dominant_frequency = 0.0
        else:
            dominant_frequency = 0.0
        
        # Calculate phase using Hilbert transform
        try:
            if len(detrended) > 2:
                analytic_signal = signal.hilbert(detrended)
                phase = np.angle(analytic_signal[-1])  # Phase of most recent point
            else:
                phase = 0.0
        except:
            phase = 0.0
        
        return {
            "amplitude": float(amplitude),
            "frequency": float(dominant_frequency),
            "phase": float(phase)
        }
    
    def detect_emotional_drift(self) -> WaveAnalysisResult:
        """
        Detect emotional drift using wave-based analysis
        Returns comprehensive drift analysis including predictions
        """
        if len(self.emotional_history) < 3:
            return WaveAnalysisResult(
                drift_score=0.0,
                dominant_frequency=0.0,
                amplitude_change=0.0,
                phase_shift=0.0,
                trend_direction="stable",
                stability_index=1.0,
                emotional_volatility=0.0,
                predicted_next_state={"valence": 0.0, "arousal": 0.0, "dominance": 0.0, "intensity": 0.0}
            )
        
        # Analyze each emotional dimension
        dimension_analyses = {}
        for dimension in ["valence", "arousal", "dominance", "intensity"]:
            dimension_analyses[dimension] = self.extract_wave_features(dimension)
        
        # Calculate overall drift score
        drift_score = self._calculate_drift_score(dimension_analyses)
        
        # Calculate amplitude change (comparing first half vs second half of window)
        amplitude_change = self._calculate_amplitude_change()
        
        # Calculate phase shift
        phase_shift = self._calculate_phase_shift(dimension_analyses)
        
        # Determine trend direction
        trend_direction = self._determine_trend_direction()
        
        # Calculate stability index (inverse of volatility)
        stability_index = self._calculate_stability_index()
        
        # Calculate emotional volatility
        emotional_volatility = self._calculate_emotional_volatility()
        
        # Predict next emotional state
        predicted_next_state = self._predict_next_state(dimension_analyses)
        
        # Get dominant frequency across all dimensions
        dominant_frequency = np.mean([analysis["frequency"] for analysis in dimension_analyses.values()])
        
        return WaveAnalysisResult(
            drift_score=drift_score,
            dominant_frequency=dominant_frequency,
            amplitude_change=amplitude_change,
            phase_shift=phase_shift,
            trend_direction=trend_direction,
            stability_index=stability_index,
            emotional_volatility=emotional_volatility,
            predicted_next_state=predicted_next_state
        )
    
    def _calculate_drift_score(self, dimension_analyses: Dict) -> float:
        """Calculate overall drift score based on wave characteristics"""
        # Weighted combination of frequency, amplitude, and phase changes
        freq_weight = 0.4
        amp_weight = 0.4
        phase_weight = 0.2
        
        avg_frequency = np.mean([analysis["frequency"] for analysis in dimension_analyses.values()])
        avg_amplitude = np.mean([analysis["amplitude"] for analysis in dimension_analyses.values()])
        avg_phase = np.mean([abs(analysis["phase"]) for analysis in dimension_analyses.values()])
        
        # Normalize scores (0-1 range)
        freq_score = min(avg_frequency * 10, 1.0)  # Scale frequency
        amp_score = min(avg_amplitude * 2, 1.0)    # Scale amplitude
        phase_score = min(avg_phase / np.pi, 1.0)  # Normalize phase
        
        drift_score = (freq_weight * freq_score + 
                      amp_weight * amp_score + 
                      phase_weight * phase_score)
        
        return float(drift_score)
    
    def _calculate_amplitude_change(self) -> float:
        """Calculate change in emotional amplitude over time"""
        if len(self.emotional_history) < 6:
            return 0.0
        
        mid_point = len(self.emotional_history) // 2
        first_half = self.emotional_history[:mid_point]
        second_half = self.emotional_history[mid_point:]
        
        # Calculate average intensity for each half
        first_half_intensity = np.mean([point.intensity for point in first_half])
        second_half_intensity = np.mean([point.intensity for point in second_half])
        
        return float(second_half_intensity - first_half_intensity)
    
    def _calculate_phase_shift(self, dimension_analyses: Dict) -> float:
        """Calculate overall phase shift across dimensions"""
        phases = [analysis["phase"] for analysis in dimension_analyses.values()]
        return float(np.std(phases))  # Phase coherence measure
    
    def _determine_trend_direction(self) -> str:
        """Determine overall emotional trend direction"""
        if len(self.emotional_history) < 3:
            return "stable"
        
        recent_valence = [point.valence for point in self.emotional_history[-3:]]
        valence_trend = np.polyfit(range(len(recent_valence)), recent_valence, 1)[0]
        
        if valence_trend > 0.1:
            return "improving"
        elif valence_trend < -0.1:
            return "declining"
        else:
            return "stable"
    
    def _calculate_stability_index(self) -> float:
        """Calculate emotional stability (inverse of variability)"""
        if len(self.emotional_history) < 2:
            return 1.0
        
        # Calculate coefficient of variation for each dimension
        dimensions_cv = []
        for dimension in ["valence", "arousal", "dominance", "intensity"]:
            values = [getattr(point, dimension) for point in self.emotional_history[-self.window_size:]]
            if len(values) > 1:
                cv = np.std(values) / (abs(np.mean(values)) + 0.001)  # Add small epsilon to avoid division by zero
                dimensions_cv.append(cv)
        
        if not dimensions_cv:
            return 1.0
        
        avg_cv = np.mean(dimensions_cv)
        stability = 1.0 / (1.0 + avg_cv)  # Convert CV to stability index
        
        return float(stability)
    
    def _calculate_emotional_volatility(self) -> float:
        """Calculate emotional volatility using wave amplitude variations"""
        if len(self.emotional_history) < 3:
            return 0.0
        
        # Calculate rolling standard deviation of intensity
        intensities = [point.intensity for point in self.emotional_history[-self.window_size:]]
        
        if len(intensities) < 3:
            return 0.0
        
        # Use windowed standard deviation as volatility measure
        volatility = np.std(intensities)
        
        return float(volatility)
    
    def _predict_next_state(self, dimension_analyses: Dict) -> Dict[str, float]:
        """Predict next emotional state based on wave patterns"""
        predictions = {}
        
        for dimension in ["valence", "arousal", "dominance", "intensity"]:
            if len(self.emotional_history) < 3:
                predictions[dimension] = 0.0
                continue
            
            # Get recent values
            recent_values = [getattr(point, dimension) for point in self.emotional_history[-3:]]
            
            # Simple wave-based prediction using sine wave extrapolation
            analysis = dimension_analyses[dimension]
            
            if analysis["frequency"] > 0:
                # Use wave parameters to predict next value
                t_next = len(recent_values)
                predicted_value = (analysis["amplitude"] * 
                                 np.sin(2 * np.pi * analysis["frequency"] * t_next + analysis["phase"]))
                
                # Add trend component
                trend = np.polyfit(range(len(recent_values)), recent_values, 1)[0]
                predicted_value += recent_values[-1] + trend
                
                # Clamp to valid ranges
                if dimension in ["valence", "dominance"]:
                    predicted_value = np.clip(predicted_value, -1.0, 1.0)
                else:  # arousal, intensity
                    predicted_value = np.clip(predicted_value, 0.0, 1.0)
                
                predictions[dimension] = float(predicted_value)
            else:
                # Fallback to simple trend extrapolation
                if len(recent_values) >= 2:
                    trend = recent_values[-1] - recent_values[-2]
                    predicted_value = recent_values[-1] + trend
                    
                    if dimension in ["valence", "dominance"]:
                        predicted_value = np.clip(predicted_value, -1.0, 1.0)
                    else:
                        predicted_value = np.clip(predicted_value, 0.0, 1.0)
                    
                    predictions[dimension] = float(predicted_value)
                else:
                    predictions[dimension] = recent_values[-1] if recent_values else 0.0
        
        return predictions
    
    def save_history(self, filename: str):
        """Save emotional history to file"""
        data = [point.to_dict() for point in self.emotional_history]
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_history(self, filename: str):
        """Load emotional history from file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.emotional_history = [EmotionalWavePoint.from_dict(point) for point in data]
        except FileNotFoundError:
            self.emotional_history = [] 