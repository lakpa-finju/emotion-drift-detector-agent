#!/usr/bin/env python3
"""
Wave-Based Emotional Drift Tracker Agent
Main CLI Interface
"""

import os
import sys
from datetime import datetime
from typing import Optional
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.text import Text
from rich import print as rprint
import matplotlib.pyplot as plt
import numpy as np

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.wave_emotion_analyzer import WaveBasedEmotionAnalyzer, EmotionalWavePoint
from processors.emotion_processor import EmotionProcessor
from generators.response_generator import EmotionalResponseGenerator
from config.config import config

class EmotionalDriftTracker:
    """Main application class for the Wave-Based Emotional Drift Tracker"""
    
    def __init__(self):
        self.console = Console()
        self.wave_analyzer = WaveBasedEmotionAnalyzer(window_size=config.wave_analysis_window)
        self.emotion_processor = EmotionProcessor()
        self.response_generator = EmotionalResponseGenerator()
        
        # Load existing emotional history
        self.wave_analyzer.load_history(config.memory_file)
        
        self.console.print(Panel.fit(
            "[bold blue]🌊 Wave-Based Emotional Drift Tracker[/bold blue]\n"
            "[dim]Advanced emotional intelligence using signal processing[/dim]",
            border_style="blue"
        ))
    
    def run_interactive_session(self):
        """Run the main interactive session"""
        self.console.print("\n[green]Welcome to your emotional journey companion![/green]")
        self.console.print("[dim]Type 'quit', 'exit', or 'help' for commands[/dim]\n")
        
        while True:
            try:
                # Get user input
                user_input = Prompt.ask("\n[bold cyan]How are you feeling?[/bold cyan]")
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    self.console.print("\n[green]Take care! Your emotional journey continues...[/green]")
                    break
                
                if user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                if user_input.lower() == 'analyze':
                    self._show_analysis_dashboard()
                    continue
                
                if user_input.lower() == 'visualize':
                    self._create_emotional_visualization()
                    continue
                
                if user_input.lower() == 'clear':
                    self._clear_history()
                    continue
                
                # Process the emotional input
                self._process_emotional_input(user_input)
                
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Session interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Error: {e}[/red]")
                continue
        
        # Save history before exit
        self.wave_analyzer.save_history(config.memory_file)
    
    def _process_emotional_input(self, user_input: str):
        """Process user input through the emotional analysis pipeline"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            # Step 1: Extract emotions
            task1 = progress.add_task("Analyzing emotional content...", total=None)
            
            # Generate context from recent history
            context = self.emotion_processor.generate_emotional_context(
                self.wave_analyzer.emotional_history[-3:]
            )
            
            # Extract emotional dimensions
            current_emotion = self.emotion_processor.extract_emotions(user_input, context)
            progress.remove_task(task1)
            
            # Step 2: Wave analysis
            task2 = progress.add_task("Performing wave-based drift analysis...", total=None)
            
            # Add to wave analyzer
            self.wave_analyzer.add_emotional_point(current_emotion)
            
            # Perform drift analysis
            wave_analysis = self.wave_analyzer.detect_emotional_drift()
            progress.remove_task(task2)
            
            # Step 3: Generate response
            task3 = progress.add_task("Generating empathetic response...", total=None)
            
            response = self.response_generator.generate_response(
                user_input,
                current_emotion,
                wave_analysis,
                self.wave_analyzer.emotional_history
            )
            progress.remove_task(task3)
        
        # Display results
        self._display_analysis_results(current_emotion, wave_analysis, response)
    
    def _display_analysis_results(self, emotion: EmotionalWavePoint, analysis, response: str):
        """Display the analysis results in a formatted way"""
        
        # Create emotional state table
        emotion_table = Table(title="Current Emotional State", show_header=True, header_style="bold magenta")
        emotion_table.add_column("Dimension", style="cyan", width=12)
        emotion_table.add_column("Value", style="white", width=8)
        emotion_table.add_column("Interpretation", style="dim")
        
        # Add emotional dimensions
        emotion_table.add_row(
            "Valence", 
            f"{emotion.valence:+.2f}",
            self._interpret_valence(emotion.valence)
        )
        emotion_table.add_row(
            "Arousal", 
            f"{emotion.arousal:.2f}",
            self._interpret_arousal(emotion.arousal)
        )
        emotion_table.add_row(
            "Dominance", 
            f"{emotion.dominance:+.2f}",
            self._interpret_dominance(emotion.dominance)
        )
        emotion_table.add_row(
            "Intensity", 
            f"{emotion.intensity:.2f}",
            self._interpret_intensity(emotion.intensity)
        )
        
        self.console.print("\n")
        self.console.print(emotion_table)
        
        # Display wave analysis
        self._display_wave_analysis(analysis)
        
        # Display AI response
        self.console.print("\n")
        self.console.print(Panel(
            response,
            title="[bold green]AI Response[/bold green]",
            border_style="green",
            padding=(1, 2)
        ))
        
        # Check for drift alerts
        alert = self.response_generator.generate_drift_alert(analysis)
        if alert:
            self.console.print("\n")
            self.console.print(Panel(
                alert,
                title="[bold red]Drift Alert[/bold red]",
                border_style="red"
            ))
    
    def _display_wave_analysis(self, analysis):
        """Display wave analysis results"""
        
        # Create wave analysis table
        wave_table = Table(title="Wave-Based Drift Analysis", show_header=True, header_style="bold blue")
        wave_table.add_column("Metric", style="cyan", width=18)
        wave_table.add_column("Value", style="white", width=10)
        wave_table.add_column("Status", style="dim")
        
        # Add wave metrics
        wave_table.add_row(
            "Drift Score",
            f"{analysis.drift_score:.3f}",
            self._interpret_drift_score(analysis.drift_score)
        )
        
        wave_table.add_row(
            "Trend Direction",
            analysis.trend_direction,
            self._get_trend_emoji(analysis.trend_direction)
        )
        
        wave_table.add_row(
            "Stability Index",
            f"{analysis.stability_index:.3f}",
            self._interpret_stability(analysis.stability_index)
        )
        
        wave_table.add_row(
            "Volatility",
            f"{analysis.emotional_volatility:.3f}",
            self._interpret_volatility(analysis.emotional_volatility)
        )
        
        wave_table.add_row(
            "Dominant Frequency",
            f"{analysis.dominant_frequency:.3f}",
            self._interpret_frequency(analysis.dominant_frequency)
        )
        
        self.console.print("\n")
        self.console.print(wave_table)
        
        # Show predictions if significant
        if any(abs(v) > 0.3 for v in analysis.predicted_next_state.values()):
            self._display_predictions(analysis.predicted_next_state)
    
    def _display_predictions(self, predictions):
        """Display emotional state predictions"""
        pred_table = Table(title="Predicted Next State", show_header=True, header_style="bold yellow")
        pred_table.add_column("Dimension", style="cyan")
        pred_table.add_column("Predicted Value", style="yellow")
        pred_table.add_column("Change Direction", style="dim")
        
        for dim, value in predictions.items():
            if hasattr(self.wave_analyzer, 'emotional_history') and self.wave_analyzer.emotional_history:
                current_val = getattr(self.wave_analyzer.emotional_history[-1], dim)
                change = value - current_val
                direction = "↗️" if change > 0.1 else "↘️" if change < -0.1 else "→"
            else:
                direction = "→"
            
            pred_table.add_row(
                dim.capitalize(),
                f"{value:+.2f}",
                direction
            )
        
        self.console.print("\n")
        self.console.print(pred_table)
    
    def _show_analysis_dashboard(self):
        """Show comprehensive analysis dashboard"""
        if len(self.wave_analyzer.emotional_history) < 2:
            self.console.print("[yellow]Need more data points for comprehensive analysis[/yellow]")
            return
        
        analysis = self.wave_analyzer.detect_emotional_drift()
        insights = self.response_generator.generate_insight_summary(
            analysis, 
            self.wave_analyzer.emotional_history
        )
        
        self.console.print("\n")
        self.console.print(Panel(
            insights,
            title="[bold blue]Emotional Insights Dashboard[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Show recent trajectory
        if len(self.wave_analyzer.emotional_history) >= 5:
            self._show_recent_trajectory()
    
    def _show_recent_trajectory(self):
        """Show recent emotional trajectory"""
        recent = self.wave_analyzer.emotional_history[-5:]
        
        traj_table = Table(title="Recent Emotional Trajectory", show_header=True)
        traj_table.add_column("Time", style="dim")
        traj_table.add_column("Valence", style="green")
        traj_table.add_column("Arousal", style="yellow")
        traj_table.add_column("Intensity", style="red")
        
        for point in recent:
            traj_table.add_row(
                point.timestamp.strftime("%H:%M"),
                f"{point.valence:+.2f}",
                f"{point.arousal:.2f}",
                f"{point.intensity:.2f}"
            )
        
        self.console.print("\n")
        self.console.print(traj_table)
    
    def _create_emotional_visualization(self):
        """Create and display emotional wave visualization"""
        if len(self.wave_analyzer.emotional_history) < 3:
            self.console.print("[yellow]Need at least 3 data points for visualization[/yellow]")
            return
        
        try:
            history = self.wave_analyzer.emotional_history[-20:]  # Last 20 points
            
            times = [i for i in range(len(history))]
            valence = [p.valence for p in history]
            arousal = [p.arousal for p in history]
            intensity = [p.intensity for p in history]
            
            plt.figure(figsize=(12, 8))
            
            # Create subplots
            plt.subplot(3, 1, 1)
            plt.plot(times, valence, 'g-o', label='Valence', linewidth=2, markersize=4)
            plt.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
            plt.ylabel('Valence')
            plt.title('Emotional Wave Analysis - Recent History')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            plt.subplot(3, 1, 2)
            plt.plot(times, arousal, 'b-o', label='Arousal', linewidth=2, markersize=4)
            plt.ylabel('Arousal')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            plt.subplot(3, 1, 3)
            plt.plot(times, intensity, 'r-o', label='Intensity', linewidth=2, markersize=4)
            plt.ylabel('Intensity')
            plt.xlabel('Time Points')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            plt.tight_layout()
            
            # Save the plot
            plot_filename = f"emotional_waves_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
            
            self.console.print(f"\n[green]Visualization saved as: {plot_filename}[/green]")
            
            # Try to display if possible
            try:
                plt.show()
            except:
                self.console.print("[dim]Note: Plot saved to file (display not available in this environment)[/dim]")
            
            plt.close()
            
        except Exception as e:
            self.console.print(f"[red]Error creating visualization: {e}[/red]")
    
    def _clear_history(self):
        """Clear emotional history"""
        if Confirm.ask("Are you sure you want to clear all emotional history?"):
            self.wave_analyzer.emotional_history = []
            self.response_generator.clear_memory()
            if os.path.exists(config.memory_file):
                os.remove(config.memory_file)
            self.console.print("[green]Emotional history cleared[/green]")
    
    def _show_help(self):
        """Show help information"""
        help_text = """
[bold cyan]Available Commands:[/bold cyan]

[green]Regular conversation:[/green] Just type how you're feeling
[green]analyze[/green] - Show detailed emotional analysis dashboard
[green]visualize[/green] - Create emotional wave visualization
[green]clear[/green] - Clear emotional history
[green]help[/green] - Show this help message
[green]quit/exit[/green] - End session

[bold cyan]How it works:[/bold cyan]
• Your emotional state is analyzed using advanced AI
• Wave-based modeling tracks emotional patterns over time
• Drift detection identifies significant emotional changes
• Personalized responses adapt to your emotional journey
"""
        self.console.print(Panel(help_text, title="Help", border_style="cyan"))
    
    # Interpretation methods
    def _interpret_valence(self, valence: float) -> str:
        if valence > 0.5: return "Very positive 😊"
        elif valence > 0.2: return "Positive 🙂"
        elif valence > -0.2: return "Neutral 😐"
        elif valence > -0.5: return "Negative 😔"
        else: return "Very negative 😢"
    
    def _interpret_arousal(self, arousal: float) -> str:
        if arousal > 0.7: return "High energy ⚡"
        elif arousal > 0.4: return "Moderate energy 🔋"
        else: return "Low energy 😴"
    
    def _interpret_dominance(self, dominance: float) -> str:
        if dominance > 0.3: return "In control 💪"
        elif dominance > -0.3: return "Balanced ⚖️"
        else: return "Less control 🤝"
    
    def _interpret_intensity(self, intensity: float) -> str:
        if intensity > 0.7: return "Very intense 🔥"
        elif intensity > 0.4: return "Moderate 📊"
        else: return "Mild 🌱"
    
    def _interpret_drift_score(self, score: float) -> str:
        if score > 0.7: return "High drift 🌊"
        elif score > 0.4: return "Moderate drift 〰️"
        else: return "Stable 🧘"
    
    def _interpret_stability(self, stability: float) -> str:
        if stability > 0.7: return "Very stable 🏔️"
        elif stability > 0.4: return "Moderately stable ⛰️"
        else: return "Unstable 🌪️"
    
    def _interpret_volatility(self, volatility: float) -> str:
        if volatility > 0.5: return "High volatility ⚡"
        elif volatility > 0.2: return "Moderate volatility 〰️"
        else: return "Low volatility 😌"
    
    def _interpret_frequency(self, frequency: float) -> str:
        if frequency > 0.5: return "Rapid cycles 🔄"
        elif frequency > 0.2: return "Moderate cycles ↩️"
        else: return "Slow cycles 🐌"
    
    def _get_trend_emoji(self, trend: str) -> str:
        if trend == "improving": return "📈"
        elif trend == "declining": return "📉"
        else: return "➡️"

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Wave-Based Emotional Drift Tracker")
    parser.add_argument("--model", help="LLM model to use", default=config.default_model)
    parser.add_argument("--window", type=int, help="Analysis window size", default=config.wave_analysis_window)
    
    args = parser.parse_args()
    
    # Check for API keys
    if not config.openai_api_key and not config.anthropic_api_key:
        print("Error: Please set OPENAI_API_KEY or ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    # Create and run the tracker
    tracker = EmotionalDriftTracker()
    
    try:
        tracker.run_interactive_session()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 