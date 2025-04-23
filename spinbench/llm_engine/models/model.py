from typing import Union, List
from spinbench.llm_engine.models.engine import EngineLM, get_engine
from spinbench.llm_engine.models.utils.llm_utils import LLMPlanCall
from abc import ABC, abstractmethod

class Module(ABC):
    """Abstract module class with parameters akin to PyTorch's nn.Module.
    """
    parameters: List[str]
    def zero_grad(self):
        for p in self.parameters():
            p.reset_gradients()

    def named_parameters(self):
        for p in self.parameters():
            yield p.get_role_description(), p
            
    @abstractmethod
    def forward(self, *args, **kwargs):
        pass
    
    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)


class BlackboxLLM(Module):
    def __init__(self, engine: Union[EngineLM, str] = None, system_prompt: Union[str] = None, device=None):
        """
        Initialize the LLM module.
        :param engine: The language model engine to use.
        :type engine: EngineLM
        :param system_prompt: The system prompt variable, defaults to None.
        :type system_prompt: Variable, optional
        """
        if ((engine is None)):
            raise Exception("No engine provided. please provide an engine as the argument to this call.")
        if isinstance(engine, str):
            engine = get_engine(engine, device=device)
        self.engine = engine
        self.system_prompt = system_prompt
        self.llm_call = LLMPlanCall(self.engine, self.system_prompt)

    def parameters(self):
        """
        Get the parameters of the blackbox LLM.

        :return: A list of parameters.
        :rtype: list
        """
        params = []
        if self.system_prompt:
            params.append(self.system_prompt)
        return params

    def forward(self, x: Union[str, List]) -> str:
        """
        Perform an LLM call.

        :param x: The input variable.
        :type x: Variable
        :return: The output variable.
        :rtype: Variable
        """
        return self.llm_call(x)
    
