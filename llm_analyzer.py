"""
LLM Integration for Screen Analysis using Google Gemini
"""

import os
from typing import Optional
import base64
from google import genai
from PIL import Image
import io


class LLMAnalyzer:
    """Gemini LLM integration for screen analysis"""
    
    def __init__(self, api_key=None):
        """
        Initialize Gemini analyzer
        
        Args:
            api_key: Gemini API key (or set GEMINI_API_KEY environment variable)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("Gemini API key not found. Get one free at: https://aistudio.google.com/apikey")
        
        # Set environment variable for client
        os.environ['GEMINI_API_KEY'] = self.api_key
        self.client = genai.Client(api_key=self.api_key)
    
    def analyze_image(self, image_base64: str, question: str, model: Optional[str] = None) -> str:
        """
        Analyze an image using Gemini
        
        Args:
            image_base64: Base64 encoded image
            question: Question to ask about the image
            model: Model to use (default: gemini-3-flash-preview for free tier)
        
        Returns:
            Gemini response text
        """
        if model is None:
            model = "gemini-3-flash-preview"  # Official model from docs
        
        # Convert base64 to PIL Image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Generate content directly with the image
        response = self.client.models.generate_content(
            model=model,
            contents=[question, image]
        )
        
        return response.text


if __name__ == "__main__":
    # Test Gemini analyzer (requires API key)
    try:
        analyzer = LLMAnalyzer()
        print("Gemini Analyzer initialized successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print("Get a free API key at: https://aistudio.google.com/apikey")
