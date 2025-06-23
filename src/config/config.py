import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional

load_dotenv()

class Config(BaseModel):
    """Configuration settings for the Emotional Drift Tracker Agent"""
    
    # API Configuration
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")
    
    # Model Configuration - Read from environment or use Claude 3.5 Sonnet as default
    default_model: str = os.getenv("DEFAULT_MODEL", "claude-3-5-sonnet-20241022")
    temperature: float = float(os.getenv("TEMPERATURE", "0.3"))
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1000"))
    
    # Wave Analysis Configuration
    wave_analysis_window: int = int(os.getenv("WAVE_ANALYSIS_WINDOW", "10"))
    drift_threshold: float = float(os.getenv("DRIFT_THRESHOLD", "0.3"))
    
    # Memory Configuration
    memory_file: str = "src/utils/emotional_memory.json"
    max_memory_entries: int = 1000
    
    # Emotional Dimensions
    emotion_dimensions: list = [
        "valence",      # Positive/Negative
        "arousal",      # High/Low Energy
        "dominance",    # Control/Submission
        "intensity"     # Strength of emotion
    ]
    
    # Wave Parameters
    wave_frequency_range: tuple = (0.1, 2.0)  # Hz equivalent for emotional cycles
    amplitude_sensitivity: float = 0.1
    phase_shift_threshold: float = 0.5

config = Config() 