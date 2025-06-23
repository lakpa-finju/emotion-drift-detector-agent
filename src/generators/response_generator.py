from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.memory import ConversationBufferWindowMemory
from typing import Dict, List, Optional
import json

from config.config import config
from core.wave_emotion_analyzer import WaveAnalysisResult, EmotionalWavePoint

class EmotionalResponseGenerator:
    """
    Generates contextually appropriate responses based on emotional drift analysis
    Uses wave-based emotional modeling to create empathetic, adaptive responses
    """
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or config.default_model
        self.llm = self._initialize_llm()
        
        # Conversation memory for context
        self.memory = ConversationBufferWindowMemory(
            k=5,  # Remember last 5 exchanges
            return_messages=True
        )
        
        # Response generation prompt template
        self.response_prompt = PromptTemplate(
            input_variables=[
                "user_input", 
                "current_emotion", 
                "wave_analysis", 
                "conversation_history",
                "emotional_trajectory"
            ],
            template="""
You are a warm, empathetic companion who understands emotions naturally. Respond like a caring friend, not a therapist.

Current situation:
- User just said: "{user_input}"
- Their emotional journey: {emotional_trajectory}
- Current mood: {current_emotion[valence]:.1f} valence, {current_emotion[arousal]:.1f} energy
- Trend: {wave_analysis.trend_direction}

CRITICAL RESPONSE RULES:

1. **Match their energy level**: 
   - Low energy (arousal < 0.4): Use calm, gentle language
   - High energy (arousal > 0.6): Match their intensity appropriately
   - Moderate energy: Stay balanced and steady

2. **Empathy without overreach**:
   - Acknowledge what they're feeling WITHOUT analyzing them
   - Don't be a therapist or give clinical advice
   - Be a supportive friend, not a counselor

3. **Compact, emotionally coherent**:
   - Keep it to 1-3 sentences maximum
   - Each sentence should feel natural and connected
   - No bullet points, no clinical terms, no therapy-speak

4. **Reference their journey subtly**:
   - If there's a clear emotional shift, acknowledge it naturally
   - Example: "You've been gradually moving from energized to flat"
   - Don't over-explain or analyze

5. **Natural conversation flow**:
   - Respond like you're texting a friend
   - Use contractions, casual language
   - Ask simple questions if appropriate

6. **Tone examples for different states**:
   - Exhausted/Done: "That sounds draining" or "I can hear how tired you are"
   - Excited: "I can feel your energy!" or "That's awesome!"
   - Flat/Meh: "Sounds like one of those blah days" or "I get that feeling"
   - Frustrated: "That's really frustrating" or "Ugh, that's the worst"

Generate a response that feels like it's from someone who genuinely cares and gets it, without being clinical or overly helpful. Just be human.
"""
        )
    
    def _initialize_llm(self):
        """Initialize the appropriate LLM based on configuration"""
        if "claude" in self.model_name.lower():
            return ChatAnthropic(
                model=self.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                anthropic_api_key=config.anthropic_api_key
            )
        else:
            return ChatOpenAI(
                model=self.model_name,
                temperature=config.temperature,
                max_tokens=config.max_tokens,
                openai_api_key=config.openai_api_key
            )
    
    def generate_response(
        self, 
        user_input: str, 
        current_emotion: EmotionalWavePoint,
        wave_analysis: WaveAnalysisResult,
        emotional_history: List[EmotionalWavePoint]
    ) -> str:
        """
        Generate an emotionally-aware response based on wave analysis
        
        Args:
            user_input: The user's current message
            current_emotion: Current emotional state
            wave_analysis: Results from wave-based drift analysis
            emotional_history: Recent emotional trajectory
            
        Returns:
            Generated empathetic response
        """
        try:
            # Prepare emotional trajectory summary
            emotional_trajectory = self._create_emotional_trajectory_summary(emotional_history)
            
            # Get conversation history
            conversation_history = self._get_conversation_history()
            
            # Prepare current emotion data
            current_emotion_dict = {
                'valence': current_emotion.valence,
                'arousal': current_emotion.arousal,
                'dominance': current_emotion.dominance,
                'intensity': current_emotion.intensity
            }
            
            # Create the prompt
            prompt = self.response_prompt.format(
                user_input=user_input,
                current_emotion=current_emotion_dict,
                wave_analysis=wave_analysis,
                conversation_history=conversation_history,
                emotional_trajectory=emotional_trajectory
            )
            
            # Generate response
            if isinstance(self.llm, ChatAnthropic) or isinstance(self.llm, ChatOpenAI):
                messages = [
                    SystemMessage(content="You are an emotionally intelligent AI companion. Be warm, empathetic, and naturally conversational."),
                    HumanMessage(content=prompt)
                ]
                response = self.llm(messages)
                response_text = response.content
            else:
                response_text = self.llm(prompt)
            
            # Add to conversation memory
            self.memory.chat_memory.add_user_message(user_input)
            self.memory.chat_memory.add_ai_message(response_text)
            
            return response_text.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return self._generate_fallback_response(current_emotion, wave_analysis)
    
    def _create_emotional_trajectory_summary(self, emotional_history: List[EmotionalWavePoint]) -> str:
        """Create a summary of recent emotional trajectory"""
        if len(emotional_history) < 2:
            return "Insufficient data for trajectory analysis."
        
        recent_points = emotional_history[-5:]  # Last 5 points
        
        # Calculate trends
        valence_trend = self._calculate_trend([p.valence for p in recent_points])
        arousal_trend = self._calculate_trend([p.arousal for p in recent_points])
        intensity_trend = self._calculate_trend([p.intensity for p in recent_points])
        
        trajectory_parts = []
        
        if abs(valence_trend) > 0.1:
            direction = "improving" if valence_trend > 0 else "declining"
            trajectory_parts.append(f"Mood has been {direction}")
        
        if abs(arousal_trend) > 0.1:
            direction = "increasing" if arousal_trend > 0 else "decreasing"
            trajectory_parts.append(f"Energy levels {direction}")
        
        if abs(intensity_trend) > 0.1:
            direction = "intensifying" if intensity_trend > 0 else "calming"
            trajectory_parts.append(f"Emotions {direction}")
        
        if not trajectory_parts:
            return "Emotional state has been relatively stable recently."
        
        return "Recent patterns: " + ", ".join(trajectory_parts) + "."
    
    def _calculate_trend(self, values: List[float]) -> float:
        """Calculate simple linear trend from values"""
        if len(values) < 2:
            return 0.0
        
        # Simple slope calculation
        n = len(values)
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n
        
        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        return numerator / denominator
    
    def _get_conversation_history(self) -> str:
        """Get formatted conversation history from memory"""
        try:
            messages = self.memory.chat_memory.messages
            if not messages:
                return "No previous conversation."
            
            history_parts = []
            for msg in messages[-6:]:  # Last 3 exchanges
                if hasattr(msg, 'content'):
                    role = "User" if msg.__class__.__name__ == "HumanMessage" else "Assistant"
                    content = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                    history_parts.append(f"{role}: {content}")
            
            return "\n".join(history_parts)
            
        except Exception:
            return "Conversation history unavailable."
    
    def _generate_fallback_response(self, current_emotion: EmotionalWavePoint, wave_analysis: WaveAnalysisResult) -> str:
        """Generate a fallback response when the main generation fails"""
        
        valence = current_emotion.valence
        arousal = current_emotion.arousal
        trend = wave_analysis.trend_direction
        
        # Match energy level and emotional state naturally
        if trend == "declining" and valence < -0.3:
            if arousal < 0.3:  # Low energy, negative
                return "You've been gradually moving from energized to flat. It's okay to name that. Want to pause for a 2-minute breath reset?"
            else:  # Higher energy, negative  
                return "That sounds really draining. I can hear how done you are with all this."
        
        if trend == "improving" and valence > 0.2:
            if arousal > 0.5:  # High energy, positive
                return "I can feel your energy picking up! That's awesome to hear."
            else:  # Lower energy, positive
                return "Sounds like things are looking up a bit. That's really good."
        
        if abs(valence) < 0.2:  # Neutral/flat
            if arousal < 0.3:
                return "Sounds like one of those blah days. I get that feeling."
            else:
                return "How's your day been treating you?"
        
        if valence < -0.4:  # Strong negative
            return "That's really tough. I'm here if you want to talk about it."
        
        if valence > 0.4:  # Strong positive
            return "I can hear how good that feels! Tell me more."
        
        # Default gentle response
        return "Thanks for sharing that with me. How are you doing?"
    
    def generate_drift_alert(self, wave_analysis: WaveAnalysisResult) -> Optional[str]:
        """
        Generate alert message for significant emotional drift
        
        Args:
            wave_analysis: Wave analysis results
            
        Returns:
            Alert message if drift is significant, None otherwise
        """
        if wave_analysis.drift_score < 0.6:
            return None
        
        alert_parts = []
        
        if wave_analysis.emotional_volatility > 0.7:
            alert_parts.append("high emotional volatility")
        
        if wave_analysis.stability_index < 0.3:
            alert_parts.append("emotional instability")
        
        if wave_analysis.trend_direction == "declining" and wave_analysis.drift_score > 0.7:
            alert_parts.append("concerning downward trend")
        
        if not alert_parts:
            alert_parts.append("significant emotional shift")
        
        alert_message = f"⚠️  Emotional Drift Alert: Detected {', '.join(alert_parts)}. "
        alert_message += "Consider checking in more frequently or seeking additional support."
        
        return alert_message
    
    def generate_insight_summary(self, wave_analysis: WaveAnalysisResult, emotional_history: List[EmotionalWavePoint]) -> str:
        """
        Generate insights summary based on wave analysis
        
        Args:
            wave_analysis: Wave analysis results
            emotional_history: Recent emotional history
            
        Returns:
            Formatted insights summary
        """
        insights = []
        
        # Drift insights
        if wave_analysis.drift_score > 0.5:
            insights.append(f"🌊 Significant emotional drift detected (score: {wave_analysis.drift_score:.2f})")
        
        # Trend insights
        if wave_analysis.trend_direction != "stable":
            trend_emoji = "📈" if wave_analysis.trend_direction == "improving" else "📉"
            insights.append(f"{trend_emoji} Overall trend: {wave_analysis.trend_direction}")
        
        # Stability insights
        if wave_analysis.stability_index < 0.4:
            insights.append(f"⚡ High emotional variability (stability: {wave_analysis.stability_index:.2f})")
        elif wave_analysis.stability_index > 0.8:
            insights.append(f"🧘 High emotional stability (stability: {wave_analysis.stability_index:.2f})")
        
        # Frequency insights
        if wave_analysis.dominant_frequency > 0.5:
            insights.append(f"🔄 Rapid emotional cycles detected (frequency: {wave_analysis.dominant_frequency:.2f})")
        
        # Prediction insights
        predicted = wave_analysis.predicted_next_state
        if abs(predicted['valence']) > 0.5:
            direction = "positive" if predicted['valence'] > 0 else "negative"
            insights.append(f"🔮 Predicted shift toward {direction} emotions")
        
        if not insights:
            insights.append("😌 Emotional patterns appear stable and balanced")
        
        return "\n".join(insights)
    
    def clear_memory(self):
        """Clear conversation memory"""
        self.memory.clear() 