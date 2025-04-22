from abc import ABC, abstractmethod

# read 
from abc import ABC, abstractmethod
import os


class PromptGenerator(ABC):
    def __init__(self):
        """
        Initialize the prompt generator with PDDL files.
        
        Args:
            domain_pddl (str): Content of the domain PDDL file
            task_pddl (str): Content of the task PDDL file
        """
        # self.domain_pddl = domain_pddl
        # self.task_pddl = task_pddl

    @abstractmethod
    def forward(self, *args, **kwargs) -> str:
        """
        Generate the prompt based on the PDDL files.
        
        Returns:
            str: Generated prompt
        """
        pass

    def save_prompt(self, output_path: str):
        """
        Save the generated prompt to a file.
        
        Args:
            output_path (str): Path where to save the prompt
        """
        prompt = self.forward()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(prompt)

    def __call__(self, output_path: str = None, *args, **kwargs) -> str:
        """
        Generate the prompt and optionally save it.
        
        Args:
            output_path (str, optional): Path to save the prompt. If None, prompt is only returned.
            
        Returns:
            str: Generated prompt
        """
        prompt = self.forward()
        if output_path:
            self.save_prompt(output_path)
        return prompt
    

def read_file(file_path: str) -> str:
    """
    Read PDDL file while preserving all formatting, spacing, and newlines.
    
    Args:
        file_path (str): Path to the PDDL file
        
    Returns:
        str: Content of the file with original formatting
    """
    with open(file_path, 'r') as f:
        return f.read().strip()
    
def read_pddl_file(file_path: str) -> str:
    """
    Read a PDDL file and filter out comment lines.
    
    Args:
        file_path (str): Path to the PDDL file
        
    Returns:
        str: Content of the file with comments removed
    """
    with open(file_path, 'r') as f:
        # Filter out lines that start with semicolon (comments)
        lines = [line for line in f.readlines() if not line.strip().startswith(';')]
        return ''.join(lines)
