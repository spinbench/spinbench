try:
    from openai import OpenAI, AzureOpenAI
except ImportError:
    raise ImportError("If you'd like to use OpenAI models, please install the openai package by running `pip install openai`, and add 'OPENAI_API_KEY' to your environment variables.")
import json
import requests

import os
import json
import base64
import platformdirs
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from typing import List, Union
from icecream import ic 
from .base import EngineLM, CachedEngine
from .engine_utils import get_image_type_from_bytes
from icecream import ic
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"
# Check if the user set the OPENROUTER_BASE_URL environment variable
if os.getenv("OPENROUTER_BASE_URL") is not None:
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")

class ChatOpenRouter(EngineLM, CachedEngine):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."

    def __init__(
        self,
        model_string: str,
        system_prompt: str=DEFAULT_SYSTEM_PROMPT,
        is_multimodal: bool=False,
        base_url: str=None,
        **kwargs):
        """
        :param model_string:
        :param system_prompt:
        :param base_url: Used to support Ollama
        """
        root = platformdirs.user_cache_dir("textgrad")
        cache_path = os.path.join(root, f"cache_openrouter_{model_string}.db")
        
        super().__init__(cache_path=cache_path)

        self.system_prompt = system_prompt
        self.base_url = OPENROUTER_BASE_URL
        
        self.headers = {
            'Authorization': "Bearer "+os.environ.get("OPENROUTER_API_KEY"),
            'Content-Type': "application/json",
        }
        self.model_string = model_string
        self.is_multimodal = is_multimodal

    def generate(self, content: Union[str, List[Union[str, bytes,dict]]], system_prompt: str=None, **kwargs):
        if isinstance(content, str):
            return self._generate_from_single_prompt(content, system_prompt=system_prompt, **kwargs)
        
        elif isinstance(content, list) and not any(isinstance(item, dict) for item in content):
            has_multimodal_input = any(isinstance(item, bytes) for item in content)
            if (has_multimodal_input) and (not self.is_multimodal):
                raise NotImplementedError("Multimodal generation is not supported.")
            
            return self._generate_from_multiple_input(content, system_prompt=system_prompt, **kwargs)
        elif isinstance(content, list) and all(isinstance(item, dict) for item in content):
            return self._generate_from_history(content, system_prompt=system_prompt, **kwargs)


    def _generate_from_single_prompt(
        self, prompt: str, system_prompt: str=None, temperature=0, max_tokens=10000, top_p=0.99
    ):

        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt

        cache_or_none = self._check_cache(sys_prompt_arg + prompt)
        if cache_or_none is not None:
            return cache_or_none

        response = requests.post('https://openrouter.ai/api/v1/chat/completions', headers=self.headers, json={
            'model': self.model_string,
            'messages': [
                {"role": "user", "content": prompt},
            ],
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
        }).json()
        content = response["choices"][0]["message"]["content"]
        self.total_tokens += response["usage"]["total_tokens"]
        self._save_cache(sys_prompt_arg + prompt, content)
        return content

    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)

    def _format_content(self, content: List[Union[str, bytes]]) -> List[dict]:
        """Helper function to format a list of strings and bytes into a list of dictionaries to pass as messages to the API.
        """
        formatted_content = []
        for item in content:
            if isinstance(item, bytes):
                # For now, bytes are assumed to be images
                image_type = get_image_type_from_bytes(item)
                base64_image = base64.b64encode(item).decode('utf-8')
                formatted_content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/{image_type};base64,{base64_image}"
                    }
                })
            elif isinstance(item, str):
                formatted_content.append({
                    "type": "text",
                    "text": item
                })
            else:
                raise ValueError(f"Unsupported input type: {type(item)}")
        return formatted_content

    def _generate_from_multiple_input(
        self, content: List[Union[str, bytes]], system_prompt=None, temperature=0, max_tokens=2000, top_p=0.99
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt
        formatted_content = self._format_content(content)

        cache_key = sys_prompt_arg + json.dumps(formatted_content)
        cache_or_none = self._check_cache(cache_key)
        if cache_or_none is not None:
            return cache_or_none
        response = requests.post(OPENROUTER_BASE_URL, headers=self.headers, json={
            'model': self.model_string,
            'messages': [{"role": "user", "content": formatted_content}],
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
        }).json()
        response_text = response["choices"][0]["message"]["content"]
        self.total_tokens += response["usage"]["total_tokens"]
        self._save_cache(cache_key, response_text)
        return response_text

    def _generate_from_history(
            self, history, system_prompt=None, temperature=0.95, max_tokens=4096, top_p=0.99
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt
        response = requests.post(OPENROUTER_BASE_URL, headers=self.headers, json={
            'model': self.model_string,
            'messages': history,
            'temperature': temperature,
            'max_tokens': max_tokens,
            'top_p': top_p,
        }).json()
        self.total_tokens += response["usage"]["total_tokens"]
        response_text = response["choices"][0]["message"]["content"]
        return response_text

