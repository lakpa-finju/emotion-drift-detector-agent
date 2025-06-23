from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from typing import Dict, Optional, Tuple
import json
import re
from datetime import datetime
from textblob import TextBlob

from config.config import config
from core.wave_emotion_analyzer import EmotionalWavePoint

class EmotionProcessor:
    """
    Processes text input to extract emotional dimensions using LLM analysis
    Converts natural language into structured emotional wave data points
    """
    
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or config.default_model
        self.llm = self._initialize_llm()
        
        # Emotion extraction prompt template
        self.emotion_prompt = PromptTemplate(
            input_variables=["text", "context"],
            template="""
You are an expert emotional analyst specializing in wave-based emotional modeling. 
Analyze the following text and extract emotional dimensions with precise numerical values.

Context from previous interactions: {context}

Text to analyze: "{text}"

Please provide a JSON response with the following emotional dimensions:

1. **Valence**: Emotional positivity/negativity (-1.0 to 1.0)
   - -1.0: Extremely negative (despair, hatred, severe depression)
   - -0.5: Moderately negative (sadness, frustration, disappointment)
   - 0.0: Neutral (calm, indifferent, balanced)
   - 0.5: Moderately positive (contentment, mild joy, satisfaction)
   - 1.0: Extremely positive (euphoria, intense joy, love)

2. **Arousal**: Emotional energy/activation level (0.0 to 1.0)
   - 0.0: Very low energy (calm, sleepy, relaxed, peaceful)
   - 0.3: Low-moderate energy (content, steady, composed)
   - 0.7: High energy (excited, alert, energetic, tense)
   - 1.0: Extremely high energy (frantic, ecstatic, panicked, rage)

3. **Dominance**: Sense of control/power (-1.0 to 1.0)
   - -1.0: Completely powerless (helpless, submissive, controlled)
   - -0.5: Low control (uncertain, dependent, guided by others)
   - 0.0: Balanced control (cooperative, equal partnership)
   - 0.5: High control (confident, leading, influential)
   - 1.0: Complete dominance (commanding, controlling, authoritative)

4. **Intensity**: Overall emotional strength (0.0 to 1.0)
   - 0.0: No emotional response (completely flat, emotionless)
   - 0.3: Mild emotional response (slight feelings, subtle)
   - 0.7: Strong emotional response (clear, noticeable feelings)
   - 1.0: Overwhelming emotional response (intense, all-consuming)

Consider:
- Subtle emotional cues and implicit feelings
- Context from previous interactions for emotional continuity
- Linguistic patterns that indicate emotional states
- Both explicit emotional words and implicit emotional undertones

Respond ONLY with a valid JSON object in this exact format:
{{
  "valence": <float>,
  "arousal": <float>, 
  "dominance": <float>,
  "intensity": <float>,
  "reasoning": "<brief explanation of the emotional analysis>",
  "key_indicators": ["<word/phrase 1>", "<word/phrase 2>", "<word/phrase 3>"]
}}
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
    
    def extract_emotions(self, text: str, context: str = "") -> EmotionalWavePoint:
        """
        Extract emotional dimensions from text using LLM analysis
        
        Args:
            text: The input text to analyze
            context: Previous conversation context for continuity
            
        Returns:
            EmotionalWavePoint with extracted emotional dimensions
        """
        try:
            # Create the prompt
            prompt = self.emotion_prompt.format(text=text, context=context)
            
            # Get LLM response
            if isinstance(self.llm, ChatAnthropic) or isinstance(self.llm, ChatOpenAI):
                messages = [
                    SystemMessage(content="You are an expert emotional analyst. Respond only with valid JSON."),
                    HumanMessage(content=prompt)
                ]
                response = self.llm(messages)
                response_text = response.content
            else:
                response_text = self.llm(prompt)
            
            # Parse the JSON response
            emotion_data = self._parse_emotion_response(response_text)
            
            # Create emotional wave point
            return EmotionalWavePoint(
                timestamp=datetime.now(),
                valence=emotion_data["valence"],
                arousal=emotion_data["arousal"],
                dominance=emotion_data["dominance"],
                intensity=emotion_data["intensity"]
            )
            
        except Exception as e:
            print(f"Error in emotion extraction: {e}")
            # Fallback to basic sentiment analysis
            return self._fallback_emotion_analysis(text)
    
    def _parse_emotion_response(self, response_text: str) -> Dict[str, float]:
        """Parse the LLM response to extract emotional dimensions"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                emotion_data = json.loads(json_str)
                
                # Validate and clamp values
                return {
                    "valence": max(-1.0, min(1.0, float(emotion_data.get("valence", 0.0)))),
                    "arousal": max(0.0, min(1.0, float(emotion_data.get("arousal", 0.5)))),
                    "dominance": max(-1.0, min(1.0, float(emotion_data.get("dominance", 0.0)))),
                    "intensity": max(0.0, min(1.0, float(emotion_data.get("intensity", 0.5))))
                }
            else:
                raise ValueError("No JSON found in response")
                
        except Exception as e:
            print(f"Error parsing emotion response: {e}")
            print(f"Response text: {response_text}")
            
            # Return neutral values as fallback
            return {
                "valence": 0.0,
                "arousal": 0.5,
                "dominance": 0.0,
                "intensity": 0.3
            }
    
    def _fallback_emotion_analysis(self, text: str) -> EmotionalWavePoint:
        """
        Fallback emotion analysis using TextBlob sentiment analysis
        Used when LLM analysis fails
        """
        try:
            blob = TextBlob(text)
            sentiment = blob.sentiment
            
            # Map TextBlob sentiment to our dimensions
            valence = float(sentiment.polarity)  # Already -1 to 1
            intensity = abs(valence) * 0.7  # Intensity based on absolute sentiment
            arousal = min(0.9, abs(valence) * 1.2)  # Higher arousal for stronger sentiment
            dominance = 0.0  # Neutral dominance as fallback
            
            return EmotionalWavePoint(
                timestamp=datetime.now(),
                valence=valence,
                arousal=arousal,
                dominance=dominance,
                intensity=intensity
            )
            
        except Exception as e:
            print(f"Fallback analysis failed: {e}")
            # Return completely neutral point
            return EmotionalWavePoint(
                timestamp=datetime.now(),
                valence=0.0,
                arousal=0.5,
                dominance=0.0,
                intensity=0.3
            )
    
    def generate_emotional_context(self, recent_points: list) -> str:
        """Generate context string from recent emotional points for continuity"""
        if not recent_points:
            return "No previous emotional context available."
        
        context_parts = []
        for i, point in enumerate(recent_points[-3:], 1):  # Last 3 points
            context_parts.append(
                f"Point {i}: Valence={point.valence:.2f}, "
                f"Arousal={point.arousal:.2f}, "
                f"Dominance={point.dominance:.2f}, "
                f"Intensity={point.intensity:.2f}"
            )
        
        return "Recent emotional trajectory: " + "; ".join(context_parts)
    
    def analyze_emotional_language(self, text: str) -> Dict[str, any]:
        """
        Additional analysis of emotional language patterns
        Provides supplementary insights beyond dimensional analysis
        """
        # Emotional word detection
        emotional_words = {
            'positive': ['happy', 'joy', 'excited', 'love', 'amazing', 'wonderful', 'great', 'fantastic'],
            'negative': ['sad', 'angry', 'frustrated', 'hate', 'terrible', 'awful', 'bad', 'horrible'],
            'high_arousal': ['excited', 'energetic', 'frantic', 'panicked', 'thrilled', 'ecstatic'],
            'low_arousal': ['calm', 'peaceful', 'relaxed', 'sleepy', 'tired', 'serene'],
            'dominant': ['control', 'power', 'command', 'lead', 'dominate', 'authority'],
            'submissive': ['helpless', 'powerless', 'dependent', 'submissive', 'controlled']
        }
        
        text_lower = text.lower()
        found_words = {}
        
        for category, words in emotional_words.items():
            found_words[category] = [word for word in words if word in text_lower]
        
        # Calculate emotional complexity (variety of emotional expressions)
        total_emotional_words = sum(len(words) for words in found_words.values())
        emotional_complexity = min(1.0, total_emotional_words / 10.0)
        
        return {
            'emotional_words': found_words,
            'emotional_complexity': emotional_complexity,
            'text_length': len(text),
            'sentence_count': len(text.split('.')),
            'word_count': len(text.split())
        } 