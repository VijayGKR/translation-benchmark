import os
from typing import Optional, Dict, Any
from openai import AsyncOpenAI, RateLimitError
from dotenv import load_dotenv

load_dotenv()

class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass

class LLMRateLimitError(LLMError):
    def __init__(self, message: str, cooldown: int = 60):
        super().__init__(message)
        self.cooldown = cooldown

class LLM:
    def __init__(self, model_name: str, session: Optional[Any] = None):
        """Initialize LLM with OpenRouter configuration"""
        self.model_name = model_name
        self.session = session
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable is not set")
            
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    async def __call__(
        self, 
        prompt: str, 
        system_prompt: str, 
        temperature: float = 0.0
    ) -> str:
        """Make an async call to the LLM"""
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            return completion.choices[0].message.content
            
        except RateLimitError as e:
            cooldown = getattr(e, 'retry_after', 60)
            raise LLMRateLimitError(
                f"Rate limit exceeded for {self.model_name}. Please try again later.",
                cooldown
            )
        except Exception as e:
            raise LLMError(f"Error calling {self.model_name}: {str(e)}")

    async def call_with_function(
        self,
        prompt: str,
        functions: Dict[str, Any],
        system_prompt: str,
        temperature: float = 0.0
    ) -> Dict[str, Any]:
        """Make a function call to the LLM"""
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                functions=functions,
                temperature=temperature,
                function_call='auto',
            )
            response_message = completion.choices[0].message
            return response_message.function_call.arguments
            
        except Exception as e:
            raise LLMError(f"Error in function call to {self.model_name}: {str(e)}")