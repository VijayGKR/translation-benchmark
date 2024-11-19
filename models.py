import os
from dotenv import load_dotenv

load_dotenv()

import json
from openai import AsyncOpenAI, RateLimitError as OpenAIRateLimitError
import anthropic
from anthropic import RateLimitError as AnthropicRateLimitError
import google.generativeai as genai
from google.api_core.exceptions import TooManyRequests as GoogleRateLimitError
from google.generativeai.types import HarmCategory, HarmBlockThreshold


MODELS = {
    "gpt-4": "OpenAI",
    "gpt-4o": "OpenAI",
    "gpt-4o-mini": "OpenAI",
    "claude-3-5-sonnet": "Anthropic",
    "claude-3-haiku": "Anthropic",
    "gemini-1.5-pro": "Google",
    "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo": "Together"
}

__all__ = ['MODELS']


# Custom error classes
class LLMAPIError(Exception):
    pass

class LLMRateLimitError(Exception):
    def __init__(self, message, cooldown=0):
        super().__init__(message)
        self.cooldown = cooldown


# Define LLM classes
class LLM:
    def __init__(self):
        pass

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        raise NotImplementedError("Subclasses must implement this method")
    
class o1LLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                )
            return completion.choices[0].message.content
        except OpenAIRateLimitError as e:
            cooldown = e.retry_after if hasattr(e, 'retry_after') else 60
            raise LLMRateLimitError(f"OpenAI rate limit exceeded. Please try again later.", cooldown)
        except Exception as e:
            raise LLMAPIError(f"Unexpected error calling OpenAI: {str(e)}")


class OpenAILLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        )

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
                )
            return completion.choices[0].message.content
        except OpenAIRateLimitError as e:
            cooldown = e.retry_after if hasattr(e, 'retry_after') else 60
            raise LLMRateLimitError(f"OpenAI rate limit exceeded. Please try again later.", cooldown)
        except Exception as e:
            raise LLMAPIError(f"Unexpected error calling OpenAI: {str(e)}")


    async def call_with_function(self, prompt, functions, system_prompt, temperature=0.0):
        completion = await self.client.chat.completions.create(
            model=self.model_name,
            functions=functions,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            function_call='auto'
        )
        response_message = completion.choices[0].message
        return json.loads(response_message.function_call.arguments)

class AnthropicLLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        self.client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        try:
            completion = await self.client.messages.create(
                model=self.model_name,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return completion.content[0].text
        except AnthropicRateLimitError as e:
            cooldown = 60
            raise LLMRateLimitError(f"Anthropic rate limit exceeded. Please try again later.", cooldown)
        except Exception as e:
            raise LLMAPIError(f"Unexpected error calling Anthropic: {str(e)}")

    async def call_with_function(self, prompt, functions, system_prompt, temperature=0.0):
        completion = await self.client.messages.create(
            model=self.model_name,
            max_tokens=1000,
            system=system_prompt,
            tools=functions,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            tool_choice={"type": "any"}
        )
        tool_use_block = next((block for block in completion.content if block.type == 'tool_use'), None)
        if tool_use_block:
            return tool_use_block.input
        else:
            return {"Error": "No tool use block found"}

class GoogleLLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    async def __call__(self, prompt, system_prompt, temperature=0.0, response_format='text/plain'):
        try:
            model = genai.GenerativeModel(model_name=self.model_name,
                                        system_instruction=system_prompt)
            result = await model.generate_content_async(
                [prompt],
                safety_settings={
                    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                },
                generation_config={"response_mime_type": response_format, "temperature": temperature}
            )
            return result.text
        except GoogleRateLimitError as e:
            cooldown = 60
            raise LLMRateLimitError(f"Google API quota exceeded. Please try again later.", cooldown)
        except Exception as e:
            raise LLMAPIError(f"Unexpected error calling Google: {str(e)}")

class TogetherLLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        self.client = AsyncOpenAI(
            api_key=os.getenv("TOGETHER_API_KEY"),
            base_url=os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1")
        )

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        try:
            completion = await self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature
            )
            return completion.choices[0].message.content
        except OpenAIRateLimitError as e:
            cooldown = e.retry_after if hasattr(e, 'retry_after') else 60
            raise LLMRateLimitError(f"Together rate limit exceeded. Please try again later.", cooldown)
        except Exception as e:
            raise LLMAPIError(f"Unexpected error calling Together: {str(e)}")