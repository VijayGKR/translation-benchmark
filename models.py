import os
import time
import asyncio
from typing import Optional, Dict, Any, TypeVar, Callable, Awaitable
from openai import AsyncOpenAI, RateLimitError
from dotenv import load_dotenv

load_dotenv()

T = TypeVar('T')  # Type variable for return type of retried function

class LLMError(Exception):
    """Base exception for LLM-related errors"""
    pass

class LLMRateLimitError(LLMError):
    def __init__(self, message: str, cooldown: int = 60, headers: Dict = None):
        super().__init__(message)
        self.cooldown = cooldown
        self.headers = headers or {}

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

    async def _retry_with_exponential_backoff(
        self,
        func: Callable[[], Awaitable[T]],
        max_retries: int = 5,
        initial_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
    ) -> T:
        """
        Retry an async function with exponential backoff.
        
        Args:
            func: Async function to retry
            max_retries: Maximum number of retries
            initial_delay: Initial delay between retries in seconds
            max_delay: Maximum delay between retries in seconds
            exponential_base: Base for exponential backoff
            
        Returns:
            The result of the function call
            
        Raises:
            LLMError: If all retries are exhausted
        """
        retries = 0
        delay = initial_delay
        last_exception = None

        while retries < max_retries:
            try:
                return await func()
            except LLMRateLimitError as e:
                last_exception = e
                # Use the cooldown from the rate limit error if available
                delay = min(e.cooldown, max_delay)
                print(f"Rate limit hit, waiting {delay} seconds before retry {retries + 1}/{max_retries}")
            except Exception as e:
                if isinstance(e, LLMError):
                    # Don't retry other LLM errors
                    raise
                last_exception = e
                print(f"Error occurred, retrying in {delay} seconds (retry {retries + 1}/{max_retries})")
            
            await asyncio.sleep(delay)
            delay = min(delay * exponential_base, max_delay)
            retries += 1

        # If we've exhausted all retries, raise the last exception
        raise LLMError(f"Failed after {max_retries} retries. Last error: {str(last_exception)}")

    async def __call__(
        self, 
        prompt: str, 
        system_prompt: str, 
        temperature: float = 0.0,
    ) -> str:
        """Make an async call to the LLM with retry logic"""
        async def _make_call():
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
            )
            
            # Check if completion is None
            if completion is None:
                raise LLMError(f"Received null response from {self.model_name}")
                
            # Check for error field in response
            if getattr(completion, 'error', None):
                error_data = completion.error
                # Check if it's a rate limit error
                if isinstance(error_data, dict):
                    message = error_data.get('message', '')
                    code = error_data.get('code')
                    metadata = error_data.get('metadata', {})
                    headers = metadata.get('headers', {})
                    
                    if code == 429 or 'rate limit' in message.lower():
                        # Get reset time from headers, default to 60 seconds
                        reset_time = int(headers.get('X-RateLimit-Reset', '0'))
                        current_time = int(time.time() * 1000)  # Convert to milliseconds
                        cooldown = max(60, (reset_time - current_time) // 1000)  # Convert to seconds
                        
                        raise LLMRateLimitError(
                            f"Rate limit exceeded for {self.model_name}. Reset at {reset_time}",
                            cooldown=cooldown,
                            headers=headers
                        )
                raise LLMError(f"Error from {self.model_name}: {error_data}")
            
            # Check if choices exist and have content
            if not hasattr(completion, 'choices') or not completion.choices:
                raise LLMError(f"No choices in response from {self.model_name}")
                
            # Check for refusal in message
            message = completion.choices[0].message
            if getattr(message, 'refusal', None):
                raise LLMError(f"Model refused to respond: {message.refusal}")
                
            # Check if content exists
            if not message.content:
                raise LLMError(f"Empty response content from {self.model_name}")
                
            return message.content

        return await self._retry_with_exponential_backoff(_make_call)

    async def call_with_function(
        self,
        prompt: str,
        functions: Dict[str, Any],
        system_prompt: str,
        temperature: float = 0.0,
    ) -> Dict[str, Any]:
        """Make a function call to the LLM with retry logic"""
        async def _make_function_call():
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

        return await self._retry_with_exponential_backoff(_make_function_call)