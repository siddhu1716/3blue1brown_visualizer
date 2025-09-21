import os
import json
import httpx
from typing import Dict, Any
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        
        if not self.use_ollama and not self.openai_api_key:
            logger.warning("No OpenAI API key found and Ollama not enabled. Using mock responses.")
            self.use_mock = True
        else:
            self.use_mock = False
            
        if not self.use_ollama and self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)

    async def refine_prompt(self, user_prompt: str) -> Dict[str, Any]:
        """
        Refine a natural language prompt into a structured request for Manim visualization.
        """
        system_prompt = """You are an expert at converting natural language descriptions into structured requests for mathematical visualizations using Manim.

Given a user's natural language prompt, convert it into a JSON object with the following structure:
{
    "visualization_type": "fourier_series" | "linear_transform" | "function_plot" | "taylor_series" | "eigenvalue_demo",
    "parameters": {
        // specific parameters for the visualization type
    },
    "description": "A clear description of what will be visualized"
}

Visualization types and their parameters:
1. fourier_series: {"terms": [1,3,5,7,9], "target_function": "square_wave"}
2. linear_transform: {"matrix": [[2,1],[1,2]], "show_eigenvectors": true}
3. function_plot: {"expression": "x**2", "x_range": [-3,3]}
4. taylor_series: {"function": "exp(x)", "center": 0, "terms": 5}
5. eigenvalue_demo: {"matrix": [[2,1],[1,2]]}

Examples:
- "Show me how a Fourier series builds a square wave" → fourier_series with square_wave
- "Visualize a 2x2 matrix transformation" → linear_transform
- "Plot the function x squared" → function_plot

Respond only with valid JSON."""

        if self.use_mock:
            return self._get_mock_response(user_prompt)
        
        try:
            if self.use_ollama:
                return await self._call_ollama(system_prompt, user_prompt)
            else:
                return await self._call_openai(system_prompt, user_prompt)
        except Exception as e:
            logger.error(f"Error calling LLM service: {e}")
            return self._get_mock_response(user_prompt)

    async def _call_openai(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        return json.loads(content)

    async def _call_ollama(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Call local Ollama API"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama2",
                    "prompt": f"{system_prompt}\n\nUser: {user_prompt}\nAssistant:",
                    "stream": False
                }
            )
            response.raise_for_status()
            content = response.json()["response"]
            return json.loads(content)

    def _get_mock_response(self, user_prompt: str) -> Dict[str, Any]:
        """Generate mock responses for testing"""
        prompt_lower = user_prompt.lower()
        
        if "fourier" in prompt_lower or "square wave" in prompt_lower:
            return {
                "visualization_type": "fourier_series",
                "parameters": {
                    "terms": [1, 3, 5, 7, 9],
                    "target_function": "square_wave"
                },
                "description": "Fourier series approximation of a square wave using odd harmonics"
            }
        elif "matrix" in prompt_lower or "transform" in prompt_lower:
            return {
                "visualization_type": "linear_transform",
                "parameters": {
                    "matrix": [[2, 1], [1, 2]],
                    "show_eigenvectors": True
                },
                "description": "Linear transformation visualization with eigenvector analysis"
            }
        elif "taylor" in prompt_lower or "series" in prompt_lower:
            return {
                "visualization_type": "taylor_series",
                "parameters": {
                    "function": "exp(x)",
                    "center": 0,
                    "terms": 5
                },
                "description": "Taylor series expansion of e^x around x=0"
            }
        elif "eigenvalue" in prompt_lower or "eigen" in prompt_lower:
            return {
                "visualization_type": "eigenvalue_demo",
                "parameters": {
                    "matrix": [[3, 1], [0, 2]]
                },
                "description": "Eigenvalue and eigenvector demonstration"
            }
        else:
            return {
                "visualization_type": "function_plot",
                "parameters": {
                    "expression": "x**2",
                    "x_range": [-3, 3]
                },
                "description": "Function plot visualization"
            }
