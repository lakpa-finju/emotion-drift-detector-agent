# 🌊 Wave-Based Emotional Drift Tracker Agent

A sophisticated emotional intelligence system that uses wave-based mathematical modeling to track, analyze, and respond to emotional patterns over time. This system treats emotions as oscillatory phenomena with amplitude, frequency, and phase characteristics, enabling advanced drift detection and predictive capabilities.

## 📋 Table of Contents

- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [How It Works](#-how-it-works)
- [Multi-Day Tracking](#-multi-day-tracking)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Technical Architecture](#-technical-architecture)
- [Research Foundations](#-research-foundations)
- [Future Integration](#-future-integration)

## 📁 Project Structure

```
emotion-drift-detector-agent/
├── README.md                    # Complete project documentation
├── requirements.txt             # Python dependencies
├── main.py                     # Main CLI application
├── .env.example                # Environment variables template
│
├── src/
│   ├── core/
│   │   └── wave_emotion_analyzer.py    # Wave-based mathematical analysis
│   ├── processors/
│   │   └── emotion_processor.py        # LLM-powered emotion extraction
│   ├── generators/
│   │   └── response_generator.py       # Context-aware response generation
│   └── config/
│       └── config.py                   # Centralized configuration
│
└── examples/
    ├── test_3_day_simulation.py        # 3-day emotional journey demo
    └── test_example.py                 # Basic functionality demo
```

## 🎯 Key Features

- **Wave-Based Analysis**: Treats emotions as oscillatory phenomena with frequency, amplitude, and phase
- **Drift Detection**: Identifies emotional shifts using mathematical wave analysis
- **Multi-Day Tracking**: Analyzes emotional patterns over 10-15 day periods
- **Context-Aware Responses**: Uses Claude AI for empathetic, personalized replies
- **Rich Visualizations**: Real-time emotional dashboards and wave plots
- **Persistent Memory**: Maintains conversation history across sessions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- **Claude API key (REQUIRED)** - This system has been tested exclusively with Claude

### Installation

1. **Clone and Install**
```bash
git clone https://github.com/lakpa-finju/emotion-drift-detector-agent.git
cd emotion-drift-detector-agent
pip install -r requirements.txt
```

2. **Set Up Environment**
```bash
# Copy the example environment file and rename it
cp .env.example .env

# Edit .env and add your Claude API key
ANTHROPIC_API_KEY=your_claude_api_key_here

# Important: This system has been tested ONLY with Claude API
# Use Claude for best results
```

3. **Run the Application**
```bash
python main.py
```

## 💡 How It Works

The system models emotions as four-dimensional waves:

1. **Valence** (-1 to 1): Negative ↔ Positive emotions
2. **Arousal** (0 to 1): Low ↔ High energy states  
3. **Dominance** (-1 to 1): Powerless ↔ Empowered feelings
4. **Intensity** (0 to 1): Mild ↔ Overwhelming emotional strength

### Drift Detection Algorithm
```
drift_score = (0.4 × frequency_score) + (0.4 × amplitude_score) + (0.2 × phase_score)
```

The system uses FFT analysis, Hilbert transforms, and signal processing to detect emotional shifts before they become obvious.

## 📅 Multi-Day Tracking

The system tracks emotional patterns over extended periods:

- **Optimal Range**: 10-15 days for comprehensive analysis
- **Minimum**: 3-5 days for basic trends
- **Memory**: Recent days weighted more heavily

Example progression:
```
Day 1: "I'm excited but a bit tired" → Valence: +0.30, Arousal: 0.40
Day 2: "Meh. I don't feel much today" → Valence: -0.10, Arousal: 0.20  
Day 3: "Back-to-back meetings again. I'm done" → Valence: -0.40, Arousal: 0.20

AI Response: "You've been gradually moving from energized to flat. It's okay to name that. 
Want to pause for a 2-minute breath reset?"
```

## 🎮 Usage Examples

### Basic Interaction
```
> How are you feeling? I'm feeling really anxious about my presentation tomorrow

Current Emotional State:
┌───────────┬────────┬─────────────────────┐
│ Dimension │ Value  │ Interpretation      │
├───────────┼────────┼─────────────────────┤
│ Valence   │ -0.45  │ Negative 😔         │
│ Arousal   │  0.78  │ High energy ⚡      │
│ Dominance │ -0.32  │ Less control 🤝     │
│ Intensity │  0.72  │ Very intense 🔥     │
└───────────┴────────┴─────────────────────┘

AI Response: I can sense the high energy and tension about tomorrow's presentation. 
It's natural to feel anxious before something important. What specific aspects are 
weighing on your mind the most?
```

### Available Commands
- `analyze` - Full emotional dashboard
- `visualize` - Generate wave plots
- `clear` - Reset history
- `help` - Show commands

## 🔧 Configuration

### API Setup
```bash
# In .env file
ANTHROPIC_API_KEY=your_claude_api_key_here
DEFAULT_MODEL=claude-3-5-sonnet-20241022
```

### Wave Parameters
```python
WAVE_ANALYSIS_WINDOW = 10      # Data points for analysis
DRIFT_THRESHOLD = 0.3          # Sensitivity threshold
```

## 📊 Technical Architecture

### Core Components

1. **`src/core/wave_emotion_analyzer.py`**: Mathematical wave analysis engine
2. **`src/processors/emotion_processor.py`**: LLM-powered emotion extraction
3. **`src/generators/response_generator.py`**: Context-aware response generation
4. **`src/config/config.py`**: Configuration management
5. **`main.py`**: CLI interface

### Data Flow
```
Text Input → LLM Analysis → Wave Features → Drift Detection → Response Generation
```

## 🔬 Research Foundations

The wave-based approach is grounded in research showing emotions exhibit oscillatory patterns:

**Core Research:**
- [Emotions as Sine Waves](https://alexcaza.com/personal/emotions-as-a-sine-wave/) - Foundational work on emotional oscillations
- [Emotional State Transitions](https://www.pnas.org/doi/10.1073/pnas.1616056114) - Predictable emotional flow patterns
- [Ultradian Emotional Rhythms](https://pubmed.ncbi.nlm.nih.gov/26035478/) - 77% of people show 65-110 minute emotional cycles

**Mathematical Foundation:**
The drift score weights are based on signal processing research:
- **Frequency (40%)**: Primary indicator of emotional cycling changes
- **Amplitude (40%)**: Reflects emotional intensity variations
- **Phase (20%)**: Indicates timing changes in emotional patterns

## 🚀 Future Integration

### Biometric Expansion
The wave-based framework can easily integrate physiological data:
- **Heart Rate Variability**: HRV correlates 0.7-0.8 with emotional states
- **Breathing Patterns**: Respiratory frequencies align with anxiety patterns
- **Voice Analysis**: Vocal prosody validates text-based analysis

### Applications
- **Organizational**: Detect team burnout and quiet quitting patterns
- **Leadership**: Track executive emotional patterns to prevent burnout
- **Personal**: Long-term emotional pattern recognition and intervention

The modular architecture makes expansion straightforward without requiring fundamental changes.

---

*"Understanding emotions as waves helps navigate the ocean of human experience with greater wisdom and compassion."*