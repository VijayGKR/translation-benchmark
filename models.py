import os
from dotenv import load_dotenv

load_dotenv()

import json
from openai import AsyncOpenAI
import anthropic
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


MODELS = {
    "gpt-4": "OpenAI",
    "gpt-4o": "OpenAI",
    "gpt-4o-mini": "OpenAI",
    "claude-3-5-sonnet": "Anthropic",
    "claude-3-haiku": "Anthropic",
    "gemini-1.5-pro": "Google"
}

__all__ = ['MODELS']

# Define LLM classes
class LLM:
    def __init__(self):
        pass

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        raise NotImplementedError("Subclasses must implement this method")

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
        completion = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content

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
    
    
class TogetherLLM(LLM):
    def __init__(self, model_name, session):
        super().__init__()
        self.model_name = model_name
        self.session = session
        self.client = together.AsyncTogether(api_key=os.getenv("TOGETHER_API_KEY"))

    async def __call__(self, prompt, system_prompt, temperature=0.0):
        completion = await self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return completion.choices[0].message.content