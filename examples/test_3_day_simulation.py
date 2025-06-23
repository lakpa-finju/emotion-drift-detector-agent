#!/usr/bin/env python3
"""
3-Day Emotional Check-in Simulation
Demonstrates emotional drift detection with multiple test scenarios
"""

import os
import sys
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import IntPrompt

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from core.wave_emotion_analyzer import WaveBasedEmotionAnalyzer, EmotionalWavePoint
from processors.emotion_processor import EmotionProcessor
from generators.response_generator import EmotionalResponseGenerator

def show_scenario_options():
    """Display available test scenarios"""
    console = Console()
    
    console.print(Panel.fit(
        "[bold blue]🌊 Wave-Based Emotional Drift Tracker - Test Scenarios[/bold blue]",
        border_style="blue"
    ))
    
    options_table = Table(title="Available Test Scenarios", show_header=True, header_style="bold cyan")
    options_table.add_column("Option", style="bold white", width=8)
    options_table.add_column("Scenario", style="yellow", width=25)
    options_table.add_column("Description", style="dim", width=50)
    
    options_table.add_row(
        "1", 
        "Workplace Burnout Journey", 
        "Day 1: 'New project kickoff! Feeling energized.'\nDay 2: 'Lots of meetings but making progress.'\nDay 3: 'Drowning in tasks. Everything urgent.'"
    )
    
    options_table.add_row(
        "2", 
        "Recovery Trajectory", 
        "Day 1: 'Rough week. Everything feels heavy.'\nDay 2: 'Taking some time to reset.'\nDay 3: 'Feeling more like myself again.'"
    )
    
    options_table.add_row(
        "3", 
        "Emotional Volatility", 
        "Day 1: 'Amazing presentation today!'\nDay 2: 'Client meeting went terribly.'\nDay 3: 'Found a way to fix everything.'"
    )
    
    console.print(options_table)
    console.print("\n[dim]Each scenario demonstrates different emotional drift patterns and system responses.[/dim]")

def get_scenario_data(scenario_choice: int) -> list:
    """Get the emotional journey data for the selected scenario"""
    
    scenarios = {
        1: {
            "name": "Workplace Burnout Journey",
            "description": "Shows gradual progression from excitement to overwhelm",
            "data": [
                {
                    "day": 1,
                    "input": "New project kickoff! Feeling energized.",
                    "timestamp": datetime.now() - timedelta(days=2)
                },
                {
                    "day": 2, 
                    "input": "Lots of meetings but making progress.",
                    "timestamp": datetime.now() - timedelta(days=1)
                },
                {
                    "day": 3,
                    "input": "Drowning in tasks. Everything urgent.",
                    "timestamp": datetime.now()
                }
            ]
        },
        2: {
            "name": "Recovery Trajectory", 
            "description": "Demonstrates emotional recovery and healing patterns",
            "data": [
                {
                    "day": 1,
                    "input": "Rough week. Everything feels heavy.",
                    "timestamp": datetime.now() - timedelta(days=2)
                },
                {
                    "day": 2, 
                    "input": "Taking some time to reset.",
                    "timestamp": datetime.now() - timedelta(days=1)
                },
                {
                    "day": 3,
                    "input": "Feeling more like myself again.",
                    "timestamp": datetime.now()
                }
            ]
        },
        3: {
            "name": "Emotional Volatility",
            "description": "Shows high emotional swings and system adaptation",
            "data": [
                {
                    "day": 1,
                    "input": "Amazing presentation today!",
                    "timestamp": datetime.now() - timedelta(days=2)
                },
                {
                    "day": 2, 
                    "input": "Client meeting went terribly.",
                    "timestamp": datetime.now() - timedelta(days=1)
                },
                {
                    "day": 3,
                    "input": "Found a way to fix everything.",
                    "timestamp": datetime.now()
                }
            ]
        }
    }
    
    return scenarios.get(scenario_choice, scenarios[1])

def run_scenario_simulation(scenario_choice: int):
    """Run the selected emotional journey scenario"""
    console = Console()
    
    scenario = get_scenario_data(scenario_choice)
    daily_inputs = scenario["data"]
    
    console.print(f"\n[bold green]Running Scenario: {scenario['name']}[/bold green]")
    console.print(f"[dim]{scenario['description']}[/dim]")
    
    # Initialize components
    wave_analyzer = WaveBasedEmotionAnalyzer(window_size=10)
    emotion_processor = EmotionProcessor()
    response_generator = EmotionalResponseGenerator()
    
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
            
            # Fallback emotional states based on scenario
            current_emotion = _get_fallback_emotion(scenario_choice, day_data['day'], day_data['timestamp'])
        
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
            emotional_states[-1],      # Day 3 emotion
            wave_analysis,             # Overall drift analysis
            emotional_states           # All 3 days of history
        )
    except Exception as e:
        console.print(f"[red]LLM Error: {e}[/red]")
        console.print("[yellow]Using fallback response...[/yellow]")
        response = _get_fallback_response(scenario_choice, emotional_states)
    
    console.print(Panel(
        response,
        title="[bold green]AI Response[/bold green]",
        border_style="green",
        padding=(1, 2)
    ))
    
    # Show the emotional trajectory
    _display_emotional_trajectory(daily_inputs, emotional_states, scenario['name'])

def _get_fallback_emotion(scenario_choice: int, day: int, timestamp: datetime) -> EmotionalWavePoint:
    """Get fallback emotional states when LLM fails"""
    
    # Scenario 1: Workplace Burnout Journey
    if scenario_choice == 1:
        if day == 1:
            return EmotionalWavePoint(timestamp=timestamp, valence=0.7, arousal=0.8, dominance=0.5, intensity=0.6)
        elif day == 2:
            return EmotionalWavePoint(timestamp=timestamp, valence=0.2, arousal=0.6, dominance=0.3, intensity=0.5)
        else:  # Day 3
            return EmotionalWavePoint(timestamp=timestamp, valence=-0.6, arousal=0.4, dominance=-0.4, intensity=0.8)
    
    # Scenario 2: Recovery Trajectory
    elif scenario_choice == 2:
        if day == 1:
            return EmotionalWavePoint(timestamp=timestamp, valence=-0.5, arousal=0.2, dominance=-0.3, intensity=0.7)
        elif day == 2:
            return EmotionalWavePoint(timestamp=timestamp, valence=0.0, arousal=0.4, dominance=0.1, intensity=0.4)
        else:  # Day 3
            return EmotionalWavePoint(timestamp=timestamp, valence=0.6, arousal=0.5, dominance=0.4, intensity=0.5)
    
    # Scenario 3: Emotional Volatility
    else:
        if day == 1:
            return EmotionalWavePoint(timestamp=timestamp, valence=0.8, arousal=0.9, dominance=0.6, intensity=0.8)
        elif day == 2:
            return EmotionalWavePoint(timestamp=timestamp, valence=-0.7, arousal=0.3, dominance=-0.5, intensity=0.8)
        else:  # Day 3
            return EmotionalWavePoint(timestamp=timestamp, valence=0.7, arousal=0.7, dominance=0.5, intensity=0.7)

def _get_fallback_response(scenario_choice: int, emotional_states: list) -> str:
    """Get fallback responses when LLM fails"""
    
    if scenario_choice == 1:  # Burnout
        return "I can see a clear pattern of burnout developing over these three days. You started energized but the workload is clearly overwhelming you now. This is a common pattern - want to talk about ways to manage this transition?"
    
    elif scenario_choice == 2:  # Recovery
        return "What a beautiful recovery journey! You've moved from heaviness to reconnecting with yourself. This shows real resilience and self-awareness. How does it feel to notice this positive shift?"
    
    else:  # Volatility
        return "You've been on quite an emotional rollercoaster! High success, deep disappointment, then problem-solving triumph. Your ability to bounce back and find solutions is remarkable, even amid the ups and downs."

def _display_emotional_trajectory(daily_inputs: list, emotional_states: list, scenario_name: str):
    """Display the complete emotional journey"""
    console = Console()
    
    console.print(f"\n[bold cyan]Emotional Journey: {scenario_name}[/bold cyan]")
    
    trajectory_table = Table(title="3-Day Progression", show_header=True)
    trajectory_table.add_column("Day", style="bold")
    trajectory_table.add_column("Input", style="yellow")
    trajectory_table.add_column("Valence", style="green")
    trajectory_table.add_column("Arousal", style="blue")
    trajectory_table.add_column("Dominance", style="purple")
    trajectory_table.add_column("Intensity", style="red")
    
    for i, (day_data, emotion) in enumerate(zip(daily_inputs, emotional_states)):
        trajectory_table.add_row(
            f"Day {day_data['day']}",
            f'"{day_data["input"]}"',
            f"{emotion.valence:+.2f}",
            f"{emotion.arousal:.2f}",
            f"{emotion.dominance:+.2f}",
            f"{emotion.intensity:.2f}"
        )
    
    console.print(trajectory_table)

def main():
    """Main function to run the test scenarios"""
    console = Console()
    
    # Show available scenarios
    show_scenario_options()
    
    # Get user choice
    try:
        choice = IntPrompt.ask(
            "\n[bold cyan]Choose a scenario to run[/bold cyan]",
            choices=["1", "2", "3"],
            default=1
        )
        
        # Run the selected scenario
        run_scenario_simulation(choice)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Simulation cancelled.[/yellow]")
        return
    except Exception as e:
        console.print(f"\n[red]Error: {e}[/red]")
        return

# Legacy function for backwards compatibility
def simulate_3_day_checkins():
    """
    Legacy function - runs the original scenario (now Scenario 1: Workplace Burnout)
    """
    run_scenario_simulation(1)

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
    main() 