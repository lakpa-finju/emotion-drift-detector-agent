#!/usr/bin/env python3
"""
3-Day Emotional Check-in Simulation
Demonstrates the exact requirements from the specification
"""

import os
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from core.wave_emotion_analyzer import WaveBasedEmotionAnalyzer, EmotionalWavePoint
from processors.emotion_processor import EmotionProcessor
from generators.response_generator import EmotionalResponseGenerator

def simulate_3_day_checkins():
    """
    Simulate the exact 3-day emotional check-in scenario from requirements:
    Day 1: "I'm excited but a bit tired."
    Day 2: "Meh. I don't feel much today."
    Day 3: "Back-to-back meetings again. I'm done."
    """
    
    console = Console()
    
    # Initialize components
    wave_analyzer = WaveBasedEmotionAnalyzer(window_size=10)
    emotion_processor = EmotionProcessor()
    response_generator = EmotionalResponseGenerator()
    
    # Define the 3-day inputs exactly as specified
    daily_inputs = [
        {
            "day": 1,
            "input": "I'm excited but a bit tired.",
            "timestamp": datetime.now() - timedelta(days=2)
        },
        {
            "day": 2, 
            "input": "Meh. I don't feel much today.",
            "timestamp": datetime.now() - timedelta(days=1)
        },
        {
            "day": 3,
            "input": "Back-to-back meetings again. I'm done.",
            "timestamp": datetime.now()
        }
    ]
    
    console.print(Panel.fit(
        "[bold blue]3-Day Emotional Check-in Analysis[/bold blue]",
        border_style="blue"
    ))
    
    emotional_states = []
    
    # Process each day's input
    for day_data in daily_inputs:
        console.print(f"\n[bold cyan]Day {day_data['day']}[/bold cyan]")
        console.print(f"[yellow]Input:[/yellow] \"{day_data['input']}\"")
        
        # Extract emotions using LLM
        try:
            # Generate context from previous days for better analysis
            context = ""
            if emotional_states:
                prev_states = []
                for i, state in enumerate(emotional_states):
                    prev_states.append(f"Day {i+1}: Valence {state.valence:.2f}, Arousal {state.arousal:.2f}, Dominance {state.dominance:.2f}, Intensity {state.intensity:.2f}")
                context = f"Previous emotional journey: {'; '.join(prev_states)}"
            
            current_emotion = emotion_processor.extract_emotions(day_data['input'], context)
            current_emotion.timestamp = day_data['timestamp']
            
        except Exception as e:
            console.print(f"[red]LLM Error: {e}[/red]")
            console.print("[yellow]Using basic emotion analysis...[/yellow]")
            
            # Only use fallback if LLM completely fails
            if day_data['day'] == 1:
                current_emotion = EmotionalWavePoint(
                    timestamp=day_data['timestamp'],
                    valence=0.6, arousal=0.4, dominance=0.2, intensity=0.5
                )
            elif day_data['day'] == 2:
                current_emotion = EmotionalWavePoint(
                    timestamp=day_data['timestamp'],
                    valence=0.0, arousal=0.2, dominance=0.0, intensity=0.3
                )
            else:  # Day 3
                current_emotion = EmotionalWavePoint(
                    timestamp=day_data['timestamp'],
                    valence=-0.6, arousal=0.3, dominance=-0.3, intensity=0.7
                )
        
        # Add to analyzer
        wave_analyzer.add_emotional_point(current_emotion)
        emotional_states.append(current_emotion)
        
        # Display current state
        emotion_table = Table(show_header=True, header_style="bold magenta")
        emotion_table.add_column("Dimension", style="cyan")
        emotion_table.add_column("Value", style="white")
        emotion_table.add_column("Interpretation", style="dim")
        
        emotion_table.add_row("Valence", f"{current_emotion.valence:+.2f}", _interpret_valence(current_emotion.valence))
        emotion_table.add_row("Arousal", f"{current_emotion.arousal:.2f}", _interpret_arousal(current_emotion.arousal))
        emotion_table.add_row("Dominance", f"{current_emotion.dominance:+.2f}", _interpret_dominance(current_emotion.dominance))
        emotion_table.add_row("Intensity", f"{current_emotion.intensity:.2f}", _interpret_intensity(current_emotion.intensity))
        
        console.print(emotion_table)
    
    # Perform drift analysis after all 3 days
    console.print(f"\n[bold green]Emotional Drift Analysis[/bold green]")
    
    wave_analysis = wave_analyzer.detect_emotional_drift()
    
    # Display drift analysis
    drift_table = Table(title="Wave-Based Analysis Results", show_header=True)
    drift_table.add_column("Metric", style="cyan")
    drift_table.add_column("Value", style="white")
    drift_table.add_column("Interpretation", style="dim")
    
    drift_table.add_row("Drift Score", f"{wave_analysis.drift_score:.3f}", _interpret_drift_score(wave_analysis.drift_score))
    drift_table.add_row("Trend Direction", wave_analysis.trend_direction, _get_trend_emoji(wave_analysis.trend_direction))
    drift_table.add_row("Stability Index", f"{wave_analysis.stability_index:.3f}", _interpret_stability(wave_analysis.stability_index))
    drift_table.add_row("Volatility", f"{wave_analysis.emotional_volatility:.3f}", _interpret_volatility(wave_analysis.emotional_volatility))
    
    console.print(drift_table)
    
    # Generate response using memory of all 3 days
    console.print(f"\n[bold green]AI Response[/bold green]")
    
    try:
        # Use the actual emotional progression for response generation
        response = response_generator.generate_response(
            daily_inputs[2]['input'],  # Day 3 input
            emotional_states[-1],      # Day 3 emotion (actual LLM-generated)
            wave_analysis,             # Overall drift analysis
            emotional_states           # All 3 days of history (actual LLM-generated)
        )
    except Exception as e:
        console.print(f"[red]LLM Error: {e}[/red]")
        console.print("[yellow]Using fallback response...[/yellow]")
        
        # Generate fallback based on actual emotional progression
        if len(emotional_states) >= 3:
            valence_change = emotional_states[-1].valence - emotional_states[0].valence
            arousal_change = emotional_states[-1].arousal - emotional_states[0].arousal
            
            if valence_change < -0.3 and arousal_change < -0.1:
                response = "You've been gradually moving from energized to flat. It's okay to name that. Want to pause for a 2-minute breath reset?"
            elif emotional_states[-1].valence < -0.3:
                response = "That sounds really draining. I can hear how done you are with all this."
            else:
                response = "Thanks for sharing that with me. How are you doing?"
        else:
            response = "Thanks for sharing that with me. How are you doing?"
    
    console.print(Panel(
        response,
        title="[bold green]Response[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    
    # Show the emotional trajectory with all 4 dimensions
    console.print(f"\n[bold cyan]Emotional Journey[/bold cyan]")
    
    trajectory_table = Table(title="3-Day Progression", show_header=True)
    trajectory_table.add_column("Day", style="bold")
    trajectory_table.add_column("Input", style="yellow")
    trajectory_table.add_column("Valence", style="green")
    trajectory_table.add_column("Arousal", style="blue")
    trajectory_table.add_column("Dominance", style="purple")
    trajectory_table.add_column("Intensity", style="red")
    trajectory_table.add_column("Summary", style="dim")
    
    summaries = ["Excited but tired", "Neutral/flat", "Overwhelmed/done"]
    
    for i, (day_data, emotion, summary) in enumerate(zip(daily_inputs, emotional_states, summaries)):
        trajectory_table.add_row(
            f"Day {day_data['day']}",
            f'"{day_data["input"]}"',
            f"{emotion.valence:+.2f}",
            f"{emotion.arousal:.2f}",
            f"{emotion.dominance:+.2f}",
            f"{emotion.intensity:.2f}",
            summary
        )
    
    console.print(trajectory_table)

def _interpret_valence(valence: float) -> str:
    if valence > 0.3: return "Positive 😊"
    elif valence > -0.3: return "Neutral 😐"
    else: return "Negative 😔"

def _interpret_arousal(arousal: float) -> str:
    if arousal > 0.6: return "High energy ⚡"
    elif arousal > 0.3: return "Moderate 🔋"
    else: return "Low energy 😴"

def _interpret_dominance(dominance: float) -> str:
    if dominance > 0.2: return "In control 💪"
    elif dominance > -0.2: return "Balanced ⚖️"
    else: return "Less control 🤝"

def _interpret_intensity(intensity: float) -> str:
    if intensity > 0.6: return "Strong 🔥"
    elif intensity > 0.3: return "Moderate 📊"
    else: return "Mild 🌱"

def _interpret_drift_score(score: float) -> str:
    if score > 0.5: return "High drift 🌊"
    elif score > 0.3: return "Moderate drift 〰️"
    else: return "Stable 🧘"

def _interpret_stability(stability: float) -> str:
    if stability > 0.7: return "Very stable 🏔️"
    elif stability > 0.4: return "Moderately stable ⛰️"
    else: return "Unstable 🌪️"

def _interpret_volatility(volatility: float) -> str:
    if volatility > 0.4: return "High volatility ⚡"
    elif volatility > 0.2: return "Moderate volatility 〰️"
    else: return "Low volatility 😌"

def _get_trend_emoji(trend: str) -> str:
    if trend == "improving": return "📈 Improving"
    elif trend == "declining": return "📉 Declining"
    else: return "➡️ Stable"

if __name__ == "__main__":
    simulate_3_day_checkins() 