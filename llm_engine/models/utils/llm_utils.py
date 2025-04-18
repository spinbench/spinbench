from llm_engine.models.engine import EngineLM, get_engine
from llm_engine.models.utils.roles import (SYSTEM_PROMPT_DEFAULT_ROLE)
from typing import Union, List
# from llm_engine.models.variable import Variable


from abc import ABC, abstractmethod

def validate_engine_or_get_default(engine):
    if (engine is None): 
        print("please provide and llm engine")
    if isinstance(engine, str):
        engine = get_engine(engine)
    return engine

class Function(ABC):
    """
    The class to define a function that can be called and backpropagated through.
    """
    
    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)
    
    @abstractmethod
    def forward(self, *args, **kwargs) -> str:
        pass
    


class LLMPlanCall(Function):
    def __init__(self, engine: EngineLM, system_prompt: str = None):
        """The simple LLM call function. This function will call the LLM with the input and return the response, also register the grad_fn for backpropagation.

        :param engine: engine to use for the LLM call
        :type engine: EngineLM
        :param system_prompt: system prompt to use for the LLM call, default depends on the engine.
        :type system_prompt: Variable, optional
        """
        super().__init__()
        self.engine = validate_engine_or_get_default(engine)
        self.system_prompt = system_prompt
        if self.system_prompt and self.system_prompt.get_role_description() is None:
            self.system_prompt.set_role_description(SYSTEM_PROMPT_DEFAULT_ROLE)
    # TODO(Kevin): Potentially use LLM as formatter 
    # Currently still directly output plan


    def forward(self, input_variable: Union[str, List], response_role_description: str = SYSTEM_PROMPT_DEFAULT_ROLE) -> str:
        """
        The LLM call. This function will call the LLM with the input and return the response,
        
        :param input_variable: The input variable (aka prompt) to use for the LLM call.
        :type input_variable: str
        :param response_role_description: Role description for the LLM response, defaults to VARIABLE_OUTPUT_DEFAULT_ROLE
        :type response_role_description: str, optional
        :return: response sampled from the LLM
        :rtype: str
        
        :example:
        >>> from textgrad import Variable, get_engine
        >>> from textgrad.autograd.llm_ops import LLMCall
        >>> engine = get_engine("gpt-3.5-turbo")
        >>> llm_call = LLMCall(engine)
        >>> prompt = Variable("What is the capital of France?", role_description="prompt to the LM")
        >>> response = llm_call(prompt, engine=engine) 
        # This returns something like Variable(data=The capital of France is Paris., grads=)
        """
        # TODO: Should we allow default roles? It will make things less performant.
        system_prompt_value = self.system_prompt.value if self.system_prompt else None

        # Make the LLM Call
        response_text = self.engine(input_variable, system_prompt=system_prompt_value)
        # TODO(kevin): add promopt generation step. 
        response = response_text
        # Create the response variable
        # response = Variable(
        #     value=response_text,
        #     predecessors=[self.system_prompt, input_variable] if self.system_prompt else [input_variable],
        #     role_description=response_role_description
        # )
        
        # logger.info(f"LLMCall function forward", extra={"text": f"System:{system_prompt_value}\nQuery: {input_variable.value}\nResponse: {response_text}"})
        
        return response
