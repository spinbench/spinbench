import os
import json
import platformdirs
import torch
from typing import List, Union
from transformers import AutoModelForCausalLM, AutoTokenizer
from .base import EngineLM, CachedEngine
from transformers import pipeline


class ChatLocalLLM(EngineLM, CachedEngine):
    DEFAULT_SYSTEM_PROMPT = "You are a helpful, creative, and smart assistant."

    def __init__(
        self,
        model_string: str = "meta-llama/Meta-Llama-3-8B",
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        **kwargs,
    ):
        root = platformdirs.user_cache_dir("textgrad")
        cache_path = os.path.join(
            root, f"cache_transformers_{model_string.replace('/', '_')}.db"
        )
        self.device = kwargs.get(
            "device", "cuda" if torch.cuda.is_available() else "cpu"
        )

        super().__init__(cache_path=cache_path)

        self.system_prompt = system_prompt
        self.model_string = model_string

        self.tokenizer = AutoTokenizer.from_pretrained(model_string)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

        self.model = AutoModelForCausalLM.from_pretrained(
            model_string,
            torch_dtype=torch.float16,
            quantization_config={
                "load_in_4bit": True,
                "bnb_4bit_compute_dtype": torch.float16,
                "bnb_4bit_use_double_quant": True,
                "bnb_4bit_quant_type": "nf4",
            },
            use_flash_attention_2=True,
            trust_remote_code=True,
            low_cpu_mem_usage=True,
            device_map="auto",
        )
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
        )

    def _format_prompt(self, prompt: str, system_prompt: str = None) -> str:
        sys_prompt = system_prompt if system_prompt else self.system_prompt
        return f"System: {sys_prompt}\nHuman: {prompt}\n <|eot_id|>:"

    def generate(
        self,
        prompt: Union[str, List[Union[str, dict]]],
        system_prompt: str = None,
        **kwargs,
    ) -> str:
        if isinstance(prompt, list) and all(isinstance(item, dict) for item in prompt):
            return self._generate_from_history(prompt, system_prompt, **kwargs)
        if isinstance(prompt, list):
            prompt = "\n".join(prompt)
        return self._generate_response(prompt, system_prompt, **kwargs)

    def _generate_from_history(
        self,
        history,
        system_prompt: str = None,
        temperature: float = 0.95,
        max_tokens: int = 40960,
        top_p: float = 0.95,
    ) -> str:
        # data format:
        # history = [
        # {"role": "user", "content": "Hi, my name is Albert"},
        # {"role": "assistant", "content": "Hello Albert, how can I help you today?"},
        # {"role": "user", "content": "Hi, my name is Albert"},
        # ]
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        else:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.extend(history)
        response = self.pipe(
            messages,
            max_length=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        # print("the response is", response)
        content = response[0]["generated_text"][-1]["content"]
        # total_tokens = response[0]['generated_text'][-1]["total_tokens"]

        return content

    def _generate_response(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        top_p: float = 0.95,
        cache: bool = False,
    ) -> str:
        if cache:
            cache_key = (system_prompt if system_prompt else self.system_prompt) + prompt
            if cache_hit := self._check_cache(cache_key):
                return cache_hit
        messages = []
        if system_prompt or self.system_prompt:
            messages.append(
                {"role": "system", "content": system_prompt or self.system_prompt}
            )
        messages.append({"role": "user", "content": prompt})

        # Use pipeline instead of manual generation
        response = self.pipe(
            messages,
            max_length=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        content = response[0]["generated_text"][-1]["content"]

        if cache:
            self._save_cache(cache_key, content)
        return content

    def __call__(self, prompt, **kwargs):
        return self.generate(prompt, **kwargs)
