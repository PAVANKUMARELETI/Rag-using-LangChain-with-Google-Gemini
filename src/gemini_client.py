"""
Google Gemini client wrapper for easier interaction with the API.
"""
import google.generativeai as genai
from typing import Optional, Dict, Any, List
import logging
from .config import Config

logger = logging.getLogger(__name__)

class GeminiClient:
    """Wrapper class for Google Gemini API interactions."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the Gemini client.
        
        Args:
            api_key: Google AI API key. If None, uses Config.GOOGLE_API_KEY
            model_name: Model name to use. If None, uses Config.GEMINI_MODEL
        """
        self.api_key = api_key or Config.GOOGLE_API_KEY
        self.model_name = model_name or Config.GEMINI_MODEL
        
        if not self.api_key:
            raise ValueError("Google AI API key is required")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Initialize the model
        self.model = genai.GenerativeModel(self.model_name)
        
        logger.info(f"Initialized Gemini client with model: {self.model_name}")
    
    def generate_content(
        self, 
        prompt: str, 
        generation_config: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate content using the Gemini model.
        
        Args:
            prompt: Input prompt for generation
            generation_config: Optional generation configuration
            
        Returns:
            Generated text response
        """
        try:
            config = generation_config or Config.get_generation_config()
            response = self.model.generate_content(
                contents=prompt,
                generation_config=genai.types.GenerationConfig(**config)
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            raise
    
    def start_chat(self) -> Any:
        """
        Start a chat session.
        
        Returns:
            Chat session object
        """
        return self.model.start_chat()
    
    def count_tokens(self, text: str) -> int:
        """
        Count tokens in the given text.
        
        Args:
            text: Input text to count tokens for
            
        Returns:
            Number of tokens
        """
        return self.model.count_tokens(text).total_tokens
    
    def experiment_temperature(
        self, 
        prompt: str, 
        temperature_values: List[float] = [0.0, 0.25, 0.5, 0.75, 1.0]
    ) -> Dict[float, str]:
        """
        Experiment with different temperature values.
        
        Args:
            prompt: Input prompt
            temperature_values: List of temperature values to test
            
        Returns:
            Dictionary mapping temperature values to responses
        """
        results = {}
        for temp in temperature_values:
            config = Config.get_generation_config(temperature=temp)
            response = self.generate_content(prompt, config)
            results[temp] = response
        return results
    
    def experiment_max_tokens(
        self,
        prompt: str,
        max_token_values: List[int] = [50, 100, 150, 200, 300]
    ) -> Dict[int, str]:
        """
        Experiment with different max output token values.
        
        Args:
            prompt: Input prompt
            max_token_values: List of max token values to test
            
        Returns:
            Dictionary mapping max token values to responses
        """
        results = {}
        for tokens in max_token_values:
            config = Config.get_generation_config(max_output_tokens=tokens)
            response = self.generate_content(prompt, config)
            results[tokens] = response
        return results
    
    def experiment_top_k(
        self,
        prompt: str,
        top_k_values: List[int] = [1, 4, 16, 32, 40]
    ) -> Dict[int, str]:
        """
        Experiment with different top-k values.
        
        Args:
            prompt: Input prompt
            top_k_values: List of top-k values to test
            
        Returns:
            Dictionary mapping top-k values to responses
        """
        results = {}
        for k in top_k_values:
            config = Config.get_generation_config(top_k=k)
            response = self.generate_content(prompt, config)
            results[k] = response
        return results
    
    def experiment_top_p(
        self,
        prompt: str,
        top_p_values: List[float] = [0.1, 0.3, 0.5, 0.8, 1.0]
    ) -> Dict[float, str]:
        """
        Experiment with different top-p values.
        
        Args:
            prompt: Input prompt
            top_p_values: List of top-p values to test
            
        Returns:
            Dictionary mapping top-p values to responses
        """
        results = {}
        for p in top_p_values:
            config = Config.get_generation_config(top_p=p)
            response = self.generate_content(prompt, config)
            results[p] = response
        return results
