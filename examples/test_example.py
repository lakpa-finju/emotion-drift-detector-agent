#!/usr/bin/env python3
"""
Test Example for Wave-Based Emotional Drift Tracker
Demonstrates the system without requiring API keys
"""

import numpy as np
from datetime import datetime, timedelta
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import matplotlib.pyplot as plt
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))

from core.wave_emotion_analyzer import WaveBasedEmotionAnalyzer, EmotionalWavePoint, WaveAnalysisResult
from processors.emotion_processor import EmotionProcessor
from generators.response_generator import EmotionalResponseGenerator
from config.config import config

def create_sample_emotional_data():
    """Create realistic sample emotional data for demonstration"""
    
    # Simulate a week of emotional data with various patterns
    sample_data = [
        # Monday - Starting week anxious about work
        {"text": "Feeling anxious about the big presentation this week", 
         "valence": -0.4, "arousal": 0.7, "dominance": -0.3, "intensity": 0.6},
        
        # Tuesday - Presentation went well, feeling better
        {"text": "The presentation went really well! Feeling relieved and proud", 
         "valence": 0.6, "arousal": 0.5, "dominance": 0.4, "intensity": 0.7},
        
        # Wednesday - Normal day, stable mood
        {"text": "Just a regular day, nothing special happening", 
         "valence": 0.1, "arousal": 0.3, "dominance": 0.0, "intensity": 0.3},
        
        # Thursday - Got some bad news
        {"text": "Received some disappointing news about the project delay", 
         "valence": -0.5, "arousal": 0.4, "dominance": -0.2, "intensity": 0.5},
        
        # Friday - Weekend excitement
        {"text": "Finally Friday! Looking forward to the weekend plans", 
         "valence": 0.5, "arousal": 0.6, "dominance": 0.3, "intensity": 0.6},
        
        # Saturday - Relaxing weekend
        {"text": "Having a peaceful Saturday morning with coffee and books", 
         "valence": 0.4, "arousal": 0.2, "dominance": 0.2, "intensity": 0.4},
        
        # Sunday - Weekend ending anxiety
        {"text": "Sunday evening blues, dreading Monday morning", 
         "valence": -0.3, "arousal": 0.5, "dominance": -0.1, "intensity": 0.4},
        
        # Monday - New week, mixed feelings
        {"text": "New week starting, feeling cautiously optimistic", 
         "valence": 0.2, "arousal": 0.4, "dominance": 0.1, "intensity": 0.4},
        
        # Tuesday - Stress building
        {"text": "Deadlines approaching, feeling the pressure mounting", 
         "valence": -0.6, "arousal": 0.8, "dominance": -0.4, "intensity": 0.8},
        
        # Wednesday - Breakthrough moment
        {"text": "Had a breakthrough on the difficult problem! Feeling energized", 
         "valence": 0.8, "arousal": 0.7, "dominance": 0.6, "intensity": 0.9},
        
        # Thursday - Maintaining momentum
        {"text": "Building on yesterday's success, feeling confident and focused", 
         "valence": 0.6, "arousal": 0.6, "dominance": 0.5, "intensity": 0.7},
        
        # Friday - Week ending well
        {"text": "Great week overall, accomplished a lot and feeling satisfied", 
         "valence": 0.5, "arousal": 0.4, "dominance": 0.4, "intensity": 0.6}
    ]
    
    # Convert to EmotionalWavePoint objects with realistic timestamps
    emotional_points = []
    base_time = datetime.now() - timedelta(days=12)
    
    for i, data in enumerate(sample_data):
        timestamp = base_time + timedelta(days=i, hours=np.random.randint(8, 20))
        point = EmotionalWavePoint(
            timestamp=timestamp,
            valence=data["valence"],
            arousal=data["arousal"],
            dominance=data["dominance"],
            intensity=data["intensity"]
        )
        emotional_points.append(point)
    
    return emotional_points, [data["text"] for data in sample_data]

def demonstrate_wave_analysis():
    """Demonstrate the wave-based emotional analysis"""
    
    console = Console()
    
    # Create title
    console.print(Panel.fit(
        "[bold blue]🌊 Wave-Based Emotional Drift Tracker - Demo[/bold blue]\n"
        "[dim]Demonstrating advanced emotional intelligence without API calls[/dim]",
        border_style="blue"
    ))
    
    # Create sample data
    console.print("\n[yellow]📊 Generating sample emotional data...[/yellow]")
    emotional_points, sample_texts = create_sample_emotional_data()
    
    # Initialize analyzer
    analyzer = WaveBasedEmotionAnalyzer(window_size=8)
    
    # Add all points to analyzer
    for point in emotional_points:
        analyzer.add_emotional_point(point)
    
    # Perform wave analysis
    console.print("[yellow]🔬 Performing wave-based drift analysis...[/yellow]")
    wave_analysis = analyzer.detect_emotional_drift()
    
    # Display sample emotional journey
    console.print("\n")
    console.print(Panel(
        "[bold cyan]Sample Emotional Journey (Last 5 Entries):[/bold cyan]\n\n" +
        "\n".join([f"• {text}" for text in sample_texts[-5:]]),
        title="Input Data",
        border_style="cyan"
    ))
    
    # Display current emotional state
    current_emotion = emotional_points[-1]
    display_emotional_state(console, current_emotion)
    
    # Display wave analysis
    display_wave_analysis(console, wave_analysis)
    
    # Display insights
    display_insights(console, wave_analysis, emotional_points)
    
    # Create visualization
    create_demonstration_visualization(emotional_points)
    
    # Show predictions
    display_predictions(console, wave_analysis)
    
    console.print("\n[green]✅ Demo completed! This showcases the wave-based analysis capabilities.[/green]")
    console.print("[dim]In the full system, these emotional dimensions would be extracted from your text using AI.[/dim]")

def display_emotional_state(console, emotion):
    """Display current emotional state"""
    emotion_table = Table(title="Current Emotional State", show_header=True, header_style="bold magenta")
    emotion_table.add_column("Dimension", style="cyan", width=12)
    emotion_table.add_column("Value", style="white", width=8)
    emotion_table.add_column("Interpretation", style="dim")
    
    # Add emotional dimensions with interpretations
    emotion_table.add_row(
        "Valence", 
        f"{emotion.valence:+.2f}",
        interpret_valence(emotion.valence)
    )
    emotion_table.add_row(
        "Arousal", 
        f"{emotion.arousal:.2f}",
        interpret_arousal(emotion.arousal)
    )
    emotion_table.add_row(
        "Dominance", 
        f"{emotion.dominance:+.2f}",
        interpret_dominance(emotion.dominance)
    )
    emotion_table.add_row(
        "Intensity", 
        f"{emotion.intensity:.2f}",
        interpret_intensity(emotion.intensity)
    )
    
    console.print("\n")
    console.print(emotion_table)

def display_wave_analysis(console, analysis):
    """Display wave analysis results"""
    wave_table = Table(title="Wave-Based Drift Analysis", show_header=True, header_style="bold blue")
    wave_table.add_column("Metric", style="cyan", width=18)
    wave_table.add_column("Value", style="white", width=10)
    wave_table.add_column("Status", style="dim")
    
    # Add wave metrics
    wave_table.add_row(
        "Drift Score",
        f"{analysis.drift_score:.3f}",
        interpret_drift_score(analysis.drift_score)
    )
    
    wave_table.add_row(
        "Trend Direction",
        analysis.trend_direction,
        get_trend_emoji(analysis.trend_direction)
    )
    
    wave_table.add_row(
        "Stability Index",
        f"{analysis.stability_index:.3f}",
        interpret_stability(analysis.stability_index)
    )
    
    wave_table.add_row(
        "Volatility",
        f"{analysis.emotional_volatility:.3f}",
        interpret_volatility(analysis.emotional_volatility)
    )
    
    wave_table.add_row(
        "Dominant Frequency",
        f"{analysis.dominant_frequency:.3f}",
        interpret_frequency(analysis.dominant_frequency)
    )
    
    console.print("\n")
    console.print(wave_table)

def display_insights(console, analysis, emotional_history):
    """Display key insights from the analysis"""
    insights = []
    
    # Drift insights
    if analysis.drift_score > 0.5:
        insights.append(f"🌊 Significant emotional drift detected (score: {analysis.drift_score:.2f})")
    
    # Trend insights
    if analysis.trend_direction != "stable":
        trend_emoji = "📈" if analysis.trend_direction == "improving" else "📉"
        insights.append(f"{trend_emoji} Overall trend: {analysis.trend_direction}")
    
    # Stability insights
    if analysis.stability_index < 0.4:
        insights.append(f"⚡ High emotional variability (stability: {analysis.stability_index:.2f})")
    elif analysis.stability_index > 0.8:
        insights.append(f"🧘 High emotional stability (stability: {analysis.stability_index:.2f})")
    
    # Frequency insights
    if analysis.dominant_frequency > 0.3:
        insights.append(f"🔄 Rapid emotional cycles detected (frequency: {analysis.dominant_frequency:.2f})")
    
    # Pattern insights
    if len(emotional_history) >= 5:
        recent_valence = [p.valence for p in emotional_history[-5:]]
        valence_range = max(recent_valence) - min(recent_valence)
        if valence_range > 1.0:
            insights.append(f"📊 Wide emotional range in recent history (range: {valence_range:.2f})")
    
    if not insights:
        insights.append("😌 Emotional patterns appear stable and balanced")
    
    console.print("\n")
    console.print(Panel(
        "\n".join(insights),
        title="[bold blue]Emotional Insights[/bold blue]",
        border_style="blue",
        padding=(1, 2)
    ))

def display_predictions(console, analysis):
    """Display emotional predictions"""
    pred_table = Table(title="Predicted Next Emotional State", show_header=True, header_style="bold yellow")
    pred_table.add_column("Dimension", style="cyan")
    pred_table.add_column("Predicted Value", style="yellow")
    pred_table.add_column("Interpretation", style="dim")
    
    predictions = analysis.predicted_next_state
    
    for dim, value in predictions.items():
        if dim == "valence":
            interpretation = interpret_valence(value)
        elif dim == "arousal":
            interpretation = interpret_arousal(value)
        elif dim == "dominance":
            interpretation = interpret_dominance(value)
        elif dim == "intensity":
            interpretation = interpret_intensity(value)
        else:
            interpretation = "N/A"
        
        pred_table.add_row(
            dim.capitalize(),
            f"{value:+.2f}" if dim in ["valence", "dominance"] else f"{value:.2f}",
            interpretation
        )
    
    console.print("\n")
    console.print(pred_table)

def create_demonstration_visualization(emotional_points):
    """Create visualization of emotional waves"""
    try:
        times = list(range(len(emotional_points)))
        valence = [p.valence for p in emotional_points]
        arousal = [p.arousal for p in emotional_points]
        intensity = [p.intensity for p in emotional_points]
        dominance = [p.dominance for p in emotional_points]
        
        plt.figure(figsize=(14, 10))
        
        # Create subplots
        plt.subplot(4, 1, 1)
        plt.plot(times, valence, 'g-o', label='Valence', linewidth=2, markersize=4)
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.ylabel('Valence')
        plt.title('Emotional Wave Analysis - Demonstration Data')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.ylim(-1.1, 1.1)
        
        plt.subplot(4, 1, 2)
        plt.plot(times, arousal, 'b-o', label='Arousal', linewidth=2, markersize=4)
        plt.ylabel('Arousal')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.ylim(-0.1, 1.1)
        
        plt.subplot(4, 1, 3)
        plt.plot(times, dominance, 'purple', marker='o', label='Dominance', linewidth=2, markersize=4)
        plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
        plt.ylabel('Dominance')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.ylim(-1.1, 1.1)
        
        plt.subplot(4, 1, 4)
        plt.plot(times, intensity, 'r-o', label='Intensity', linewidth=2, markersize=4)
        plt.ylabel('Intensity')
        plt.xlabel('Time Points (Days)')
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.ylim(-0.1, 1.1)
        
        plt.tight_layout()
        
        # Save the plot
        plot_filename = f"demo_emotional_waves_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        
        print(f"\n📊 Visualization saved as: {plot_filename}")
        
        # Try to display if possible
        try:
            plt.show()
        except:
            print("Note: Plot saved to file (display not available in this environment)")
        
        plt.close()
        
    except Exception as e:
        print(f"Error creating visualization: {e}")

# Interpretation helper functions
def interpret_valence(valence):
    if valence > 0.5: return "Very positive 😊"
    elif valence > 0.2: return "Positive 🙂"
    elif valence > -0.2: return "Neutral 😐"
    elif valence > -0.5: return "Negative 😔"
    else: return "Very negative 😢"

def interpret_arousal(arousal):
    if arousal > 0.7: return "High energy ⚡"
    elif arousal > 0.4: return "Moderate energy 🔋"
    else: return "Low energy 😴"

def interpret_dominance(dominance):
    if dominance > 0.3: return "In control 💪"
    elif dominance > -0.3: return "Balanced ⚖️"
    else: return "Less control 🤝"

def interpret_intensity(intensity):
    if intensity > 0.7: return "Very intense 🔥"
    elif intensity > 0.4: return "Moderate 📊"
    else: return "Mild 🌱"

def interpret_drift_score(score):
    if score > 0.7: return "High drift 🌊"
    elif score > 0.4: return "Moderate drift 〰️"
    else: return "Stable 🧘"

def interpret_stability(stability):
    if stability > 0.7: return "Very stable 🏔️"
    elif stability > 0.4: return "Moderately stable ⛰️"
    else: return "Unstable 🌪️"

def interpret_volatility(volatility):
    if volatility > 0.5: return "High volatility ⚡"
    elif volatility > 0.2: return "Moderate volatility 〰️"
    else: return "Low volatility 😌"

def interpret_frequency(frequency):
    if frequency > 0.5: return "Rapid cycles 🔄"
    elif frequency > 0.2: return "Moderate cycles ↩️"
    else: return "Slow cycles 🐌"

def get_trend_emoji(trend):
    if trend == "improving": return "📈"
    elif trend == "declining": return "📉"
    else: return "➡️"

if __name__ == "__main__":
    demonstrate_wave_analysis() 