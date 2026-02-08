try:
    from xai_sdk import Client
    from xai_sdk.chat import user, system, assistant
except ImportError:
    raise ImportError("If you'd like to use XAI models, please install the xai_sdk package. ")

import os
import json
import base64
import platformdirs
from typing import List, Union
from .base import EngineLM, CachedEngine
from .engine_utils import get_image_type_from_bytes


class ChatXAI(EngineLM, CachedEngine):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."

    def __init__(
        self,
        model_string: str="grok-4",
        system_prompt: str=DEFAULT_SYSTEM_PROMPT,
        is_multimodal: bool=False,
        **kwargs):
        """
        :param model_string:
        :param system_prompt:
        :param base_url: Used to support Ollama
        """
        root = platformdirs.user_cache_dir("textgrad")
        cache_path = os.path.join(root, f"cache_openai_{model_string}.db")
        
        super().__init__(cache_path=cache_path)

        self.system_prompt = system_prompt
        self.client = Client(
            api_key=os.getenv("XAI_API_KEY"),
            timeout=3600,  # Override default timeout with longer timeout for reasoning models
        )
        self.model_string = model_string
        self.is_multimodal = is_multimodal

    def generate(self, content: Union[str, List[Union[str, bytes,dict]]], system_prompt: str=None, **kwargs):
        if isinstance(content, str):
            return self._generate_from_single_prompt(content, system_prompt=system_prompt, **kwargs)
        elif isinstance(content, list) and not any(isinstance(item, dict) for item in content):
            has_multimodal_input = any(isinstance(item, bytes) for item in content)
            if (has_multimodal_input) and (not self.is_multimodal):
                raise NotImplementedError("Multimodal generation is not supported in this library yet")
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
        try:
            chat = self.client.chat.create(
                model=self.model_string,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
        except:
            chat = self.client.chat.create(
                model=self.model_string,
            )
        if system_prompt:
            chat.append(system(system_prompt))
        chat.append(user(prompt))
        response = chat.sample()
        self.total_tokens += response.usage.total_tokens
        self._save_cache(sys_prompt_arg + prompt, response.content)
        return response.content

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
        
        try:
            chat = self.client.chat.create(
                    model=self.model_string,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p
            )
        except:
            chat = self.client.chat.create(
                model=self.model_string,
            )
        if sys_prompt_arg:
            chat.append(system(sys_prompt_arg))
        chat.append(user(formatted_content))
        response = chat.sample()
        response_text = response.content
        self.total_tokens += response.usage.total_tokens
        self._save_cache(cache_key, response_text)
        return response_text

    def _generate_from_history(
            self, history, system_prompt=None, temperature=0.95, max_tokens=4096, top_p=0.99
    ):
        sys_prompt_arg = system_prompt if system_prompt else self.system_prompt
        try:
            chat = self.client.chat.create(
                model=self.model_string,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p
            )
        except:
            chat = self.client.chat.create(
                model=self.model_string,
            )
        if sys_prompt_arg:
            chat.append(system(sys_prompt_arg))
        for m in history:
            if m["role"] == "user":
                chat.append(user(m["content"]))
            elif m["role"] == "assistant":
                chat.append(assistant(m["content"]))
        response = chat.sample()
        self.total_tokens += response.usage.total_tokens
        response_text = response.content
        return response_text