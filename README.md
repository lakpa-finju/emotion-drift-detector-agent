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
│   ├── config/
│   │   └── config.py                   # Centralized configuration
│   └── utils/
│       └── emotional_memory.json       # Persistent emotional history storage
│
├── assets/                             # Generated visualizations and plots
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

### Pre-Built Test Scenarios

For testing and demonstration, run the 3-day simulation with predefined emotional journeys:

```bash
python examples/test_3_day_simulation.py
```

The system provides three carefully designed scenarios that demonstrate different emotional patterns. Below are the **actual results** from running each scenario:

#### Scenario 1: Workplace Burnout Journey
*Shows gradual progression from excitement to overwhelm*

```
Running Scenario: Workplace Burnout Journey

Day 1 - Input: "New project kickoff! Feeling energized."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.80 │ Positive 😊    │
│ Arousal   │ 0.70  │ High energy ⚡ │
│ Dominance │ +0.60 │ In control 💪  │
│ Intensity │ 0.70  │ Strong 🔥      │
└───────────┴───────┴────────────────┘

Day 2 - Input: "Lots of meetings but making progress."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.30 │ Neutral 😐     │
│ Arousal   │ 0.60  │ Moderate 🔋    │
│ Dominance │ +0.20 │ Balanced ⚖️    │
│ Intensity │ 0.40  │ Moderate 📊    │
└───────────┴───────┴────────────────┘

Day 3 - Input: "Drowning in tasks. Everything urgent."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation  ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Valence   │ -0.60 │ Negative 😔     │
│ Arousal   │ 0.80  │ High energy ⚡  │
│ Dominance │ -0.70 │ Less control 🤝 │
│ Intensity │ 0.85  │ Strong 🔥       │
└───────────┴───────┴─────────────────┘

Wave-Based Analysis Results:
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value     ┃ Interpretation    ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Drift Score     │ 0.378     │ Moderate drift 〰️ │
│ Trend Direction │ declining │ 📉 Declining      │
│ Stability Index │ 0.169     │ Unstable 🌪️       │
│ Volatility      │ 0.187     │ Low volatility 😌 │
└─────────────────┴───────────┴───────────────────┘

AI Response: "I hear you - it's like everything's coming at you all at once. 
I've noticed you've been carrying more and more lately, and it sounds completely 
overwhelming right now. Want to just take a breath together?"
```

#### Scenario 2: Recovery Trajectory  
*Demonstrates emotional recovery and healing patterns*

```
Running Scenario: Recovery Trajectory

Day 1 - Input: "Rough week. Everything feels heavy."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation  ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Valence   │ -0.60 │ Negative 😔     │
│ Arousal   │ 0.20  │ Low energy 😴   │
│ Dominance │ -0.70 │ Less control 🤝 │
│ Intensity │ 0.65  │ Strong 🔥       │
└───────────┴───────┴─────────────────┘

Day 2 - Input: "Taking some time to reset."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.20 │ Neutral 😐     │
│ Arousal   │ 0.20  │ Low energy 😴  │
│ Dominance │ +0.30 │ In control 💪  │
│ Intensity │ 0.40  │ Moderate 📊    │
└───────────┴───────┴────────────────┘

Day 3 - Input: "Feeling more like myself again."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.45 │ Positive 😊    │
│ Arousal   │ 0.35  │ Moderate 🔋    │
│ Dominance │ +0.40 │ In control 💪  │
│ Intensity │ 0.45  │ Moderate 📊    │
└───────────┴───────┴────────────────┘

Wave-Based Analysis Results:
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value     ┃ Interpretation    ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━┩
│ Drift Score     │ 0.325     │ Moderate drift 〰️ │
│ Trend Direction │ improving │ 📈 Improving      │
│ Stability Index │ 0.008     │ Unstable 🌪️       │
│ Volatility      │ 0.108     │ Low volatility 😌 │
└─────────────────┴───────────┴───────────────────┘

AI Response: "That's really good to hear! I know it hasn't been the easiest road, 
but there's something so comforting about feeling like yourself again, isn't there?"
```

#### Scenario 3: Emotional Volatility
*Shows high emotional swings and system adaptation*

```
Running Scenario: Emotional Volatility

Day 1 - Input: "Amazing presentation today!"
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.80 │ Positive 😊    │
│ Arousal   │ 0.70  │ High energy ⚡ │
│ Dominance │ +0.40 │ In control 💪  │
│ Intensity │ 0.70  │ Strong 🔥      │
└───────────┴───────┴────────────────┘

Day 2 - Input: "Client meeting went terribly."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation  ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Valence   │ -0.60 │ Negative 😔     │
│ Arousal   │ 0.65  │ High energy ⚡  │
│ Dominance │ -0.40 │ Less control 🤝 │
│ Intensity │ 0.75  │ Strong 🔥       │
└───────────┴───────┴─────────────────┘

Day 3 - Input: "Found a way to fix everything."
┏━━━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ Dimension ┃ Value ┃ Interpretation ┃
┡━━━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ Valence   │ +0.85 │ Positive 😊    │
│ Arousal   │ 0.65  │ High energy ⚡ │
│ Dominance │ +0.80 │ In control 💪  │
│ Intensity │ 0.75  │ Strong 🔥      │
└───────────┴───────┴────────────────┘

Wave-Based Analysis Results:
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ Metric          ┃ Value  ┃ Interpretation      ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ Drift Score     │ 0.327  │ Moderate drift 〰️   │
│ Trend Direction │ stable │ ➡️ Stable            │
│ Stability Index │ 0.510  │ Moderately stable ⛰️ │
│ Volatility      │ 0.024  │ Low volatility 😌   │
└─────────────────┴────────┴─────────────────────┘

AI Response: "That's fantastic! I can feel your confidence coming through. 
What's got you feeling so on top of things? 😊"
```

**Key Observations from Real Results:**

1. **Burnout Detection**: Clear degradation from positive (+0.80 valence) to negative (-0.60 valence) with declining trend
2. **Recovery Tracking**: Successful progression from negative (-0.60) to positive (+0.45) with improving trend  
3. **Volatility Management**: High emotional swings but stable overall trend with moderate stability index
4. **Contextual AI Responses**: Each response demonstrates awareness of the emotional journey and provides appropriate support

### Available Commands
- `analyze` - Full emotional dashboard
- `visualize` - Generate wave plots (saved to assets/ directory)
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

## ⚖️ Key Design Tradeoffs

### 1. Mathematical Complexity vs. Implementation Simplicity

**The Tradeoff:** 
Choosing between implementing a sophisticated wave-based mathematical model (involving FFT analysis, Hilbert transforms, and signal processing) versus a simpler approach like basic sentiment scoring or rule-based emotional transitions.

**Decision Made:** 
Chose the mathematically sophisticated wave analysis approach despite the implementation complexity.

**Reasoning:**
The wave-based approach provides significantly more nuanced emotional understanding. Simple sentiment analysis would miss critical patterns like "I'm anxious but excited" (high arousal with mixed valence) or wouldn't detect gradual emotional drift over time. The mathematical complexity enables the system to:
- Detect subtle emotional changes that simpler systems miss
- Predict emotional trajectories rather than just react to current state
- Provide quantifiable drift scores that can trigger appropriate interventions
- Scale to incorporate future biometric data streams

**What Was Given Up:** 
Faster development time, easier debugging, and simpler maintenance in exchange for superior emotional accuracy and future extensibility.

### 2. Real-time Response vs. Comprehensive Analysis

**The Tradeoff:** 
Users expect immediate responses to their emotional inputs, but comprehensive wave analysis requires processing historical data and performing complex mathematical operations that take time.

**Decision Made:** 
Implemented a hybrid approach where the system provides immediate basic emotional acknowledgment while performing deeper wave analysis in the background.

**Reasoning:**
User experience research shows that emotional support systems need to feel responsive and empathetic. A 10-second delay while computing FFT analysis would break the conversational flow and reduce user trust. However, the deep analysis is crucial for accurate drift detection. The hybrid approach allows the system to:
- Maintain conversational flow with immediate responses
- Provide increasingly sophisticated analysis as more data becomes available
- Update drift scores and trajectories without blocking user interaction
- Cache analysis results to improve future response times

**What Was Given Up:** 
Perfect accuracy in first responses and some computational efficiency (running dual processing paths) in exchange for better user experience and practical usability.

### 3. Future Extensibility vs. Current Simplicity

**The Tradeoff:** 
Building a minimal system focused only on the current requirements (3-day text-based emotional tracking) or designing a more complex architecture that could easily accommodate future features like biometric integration, multi-user support, and organizational analytics.

**Decision Made:** 
Chose a modular architecture with clear extension points and standardized interfaces, even though it required more upfront design work.

**Reasoning:**
The modular design prevents costly rewrites later and enables:
- Easy integration of new data sources (HRV, voice, breathing patterns)
- Scaling from individual to team/organizational analysis
- Adding new emotional analysis algorithms without changing core architecture
- Supporting different LLM providers and analysis methods

**What Was Given Up:** 
Faster initial development and simpler codebase structure in exchange for long-term maintainability and growth potential. The system is more complex than needed for just the 3-day demo, but this investment pays off when expanding functionality.

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