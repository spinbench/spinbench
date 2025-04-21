from llm_engine.models.prompt_generation import PromptGenerator, read_file, read_pddl_file
import argparse
import os
import json
from typing import List
from pathlib import Path



class PlanningPromptGenerator(PromptGenerator):
    def __init__(self, use_one_shot: bool = False):
        """
        Initialize the PlanningPromptGenerator.
        
        Args:
            use_one_shot (bool): Whether to use one-shot learning with example. Defaults to False.
        """
        super().__init__()
        self.use_one_shot = use_one_shot
        
        # Example case for one-shot learning
        self.example_domain = """(define (domain blocksworld-4ops)
  (:requirements :strips)
(:predicates (clear ?x)
             (on-table ?x)
             (arm-empty)
             (holding ?x)
             (on ?x ?y))

(:action pickup
  :parameters (?ob)
  :precondition (and (clear ?ob) (on-table ?ob) (arm-empty))
  :effect (and (holding ?ob) (not (clear ?ob)) (not (on-table ?ob)) 
               (not (arm-empty))))

(:action putdown
  :parameters (?ob)
  :precondition (holding ?ob)
  :effect (and (clear ?ob) (arm-empty) (on-table ?ob) 
               (not (holding ?ob))))

(:action stack
  :parameters (?ob ?underob)
  :precondition (and (clear ?underob) (holding ?ob))
  :effect (and (arm-empty) (clear ?ob) (on ?ob ?underob)
               (not (clear ?underob)) (not (holding ?ob))))

(:action unstack
  :parameters (?ob ?underob)
  :precondition (and (on ?ob ?underob) (clear ?ob) (arm-empty))
  :effect (and (holding ?ob) (clear ?underob)
               (not (on ?ob ?underob)) (not (clear ?ob)) (not (arm-empty))))"""

        self.example_task = """(define (problem BW-rand-3)
  (:domain blocksworld-4ops)
  (:objects b1 b2 b3)
  (:init (arm-empty) (on b1 b3) (on-table b2) (on b3 b2) (clear b1))
  (:goal (and (on b2 b3) (on b3 b1))))"""

        self.example_solution = """$$\n{
    "plan": "(unstack b1 b3)
(putdown b1)
(unstack b3 b2)
(stack b3 b1)
(pickup b2)
(stack b2 b3)"
}\n$$"""

    def forward(self) -> str:
        """
        Generate a prompt for PDDL planning.
        
        Returns:
            str: Generated prompt asking for a PDDL format plan
        """
        if self.use_one_shot:
            prompt = "This is an example PDDL:\n\n"
            prompt += f"Example Domain PDDL:\n```\n{self.example_domain}\n```\n\n"
            prompt += f"Example Task PDDL:\n```\n{self.example_task}\n```\n\n"
            prompt += f"Example Solution:\n```\n{self.example_solution}\n```\n\n"
            prompt += "Now, solve this new planning problem:\n\n"
        else:
            prompt = "Solve this planning problem:\n\n"
            
            prompt += f"Domain PDDL:\n```\n{self.domain_pddl}\n```\n\n"
            prompt += f"Task PDDL:\n```\n{self.task_pddl}\n```\n\n"

        # Here’s the key part of the new instruction block:
        prompt += (
            "First, reason about the problem step by step **outside** of the JSON. "
            "Then, provide **only** the final plan in JSON format, enclosed within $$ markers.\n\n"

            "Your final response **must** follow **exactly** this format:\n\n"
            "Reason:\n"
            "```\n"
            "your step by step reasoning...\n"
            "```\n\n"
            "$$\n"
            "{\n"
            '    "plan": "(action1)\\n(action2)\\n(action3)..."'
            "}\n"
            "$$\n\n"
            
            "Important details:\n"
            "1. All newlines **inside** the plan actions should be represented with '\\n'.\n"
            "2. The JSON should contain **only** the key 'plan'.\n"
            "3. The plan should contain **only** the sequence of actions in valid PDDL format.\n"
            "4. The 'Reason:' section (in triple-backticks) **must** remain outside the JSON.\n"
            "5. The entire JSON block **must** be enclosed between $$ markers.\n"
        )

        return prompt











    def save_json(self, output_path: str, domain_path: str, task_path: str):
        """
        Save the prompt to a JSON file with index structure.
        
        Args:
            output_path (str): Path to save the JSON file
            domain_path (str): Path to the domain PDDL file
            task_path (str): Path to the task PDDL file
        """
        prompt = self.forward()
        
        # Create index structure
        data = {
            "prompts": [
                {
                    "domain_file": domain_path,
                    "problem_file": task_path,
                    "prompt": prompt
                }
            ]
        }
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # If file exists, update it, otherwise create new
        if os.path.exists(output_path):
            try:
                with open(output_path, 'r') as f:
                    existing_data = json.load(f)
                    # Check if this domain/problem combination already exists
                    for item in existing_data["prompts"]:
                        if item["domain_file"] == domain_path and item["problem_file"] == task_path:
                            item["prompt"] = prompt
                            break
                    else:  # If not found, append new
                        existing_data["prompts"].append(data["prompts"][0])
                    data = existing_data
            except json.JSONDecodeError:
                pass  # If JSON is invalid, overwrite with new data

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    def process_domain(self, domain_path: str, output_path: str) -> dict:
        """
        Process a single domain and all its instances.
        
        Args:
            domain_path (str): Path to the domain directory
            output_path (str): Base path for output files
        
        Returns:
            dict: Dictionary containing all prompts for this domain
        """
        domain_name = os.path.basename(domain_path)
        
        # Find domain file
        domain_file = None
        for file in os.listdir(domain_path):
            if file.startswith("domain") and file.endswith(".pddl"):
                domain_file = os.path.join(domain_path, file)
                break
        
        if not domain_file:
            print(f"No domain file found in {domain_path}")
            return None
            
        instances_dir = os.path.join(domain_path, "instances")
        
        # Read domain content
        domain_content = read_pddl_file(domain_file)
        
        prompts_data = {
            "domain": domain_name,
            "domain_file": domain_file,
            "prompts": []
        }
        
        # Process each instance
        if os.path.exists(instances_dir):
            instance_files = sorted(os.listdir(instances_dir))
            for instance_file in instance_files:
                if instance_file.endswith('.pddl'):
                    instance_path = os.path.join(instances_dir, instance_file)
                    instance_content = read_file(instance_path)
                    
                    self.domain_pddl = domain_content
                    self.task_pddl = instance_content
                    prompt = self.forward()
                    
                    prompts_data["prompts"].append({
                        "instance": instance_file,
                        "instance_path": instance_path,
                        "prompt": prompt
                    })
            
            # Save domain-specific JSON
            output_file = os.path.join(output_path, f"{domain_name}.json")
            os.makedirs(output_path, exist_ok=True)
            with open(output_file, 'w') as f:
                json.dump(prompts_data, f, indent=2)
                
            return prompts_data
        else:
            print(f"No instances directory found in {domain_path}")
            return None

def get_domains(data_path: str) -> List[str]:
    """
    Get list of all domain directories.
    
    Args:
        data_path (str): Base path containing domain directories
    
    Returns:
        List[str]: List of domain directory paths
    """
    return [d for d in os.listdir(data_path) 
            if os.path.isdir(os.path.join(data_path, d))]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate prompts from PDDL files')
    parser.add_argument('--domain', default='', 
                        help='Specific domain to process (leave empty for all domains)')
    parser.add_argument('--data_path', default='./data/pddl',
                        help='Base path for domains')
    parser.add_argument('--output_path', default='data/inputs/solve_plan',
                        help='Base path for output')
    parser.add_argument('--one_shot', action='store_true',
                        help='Use one-shot learning with example')
    
    args = parser.parse_args()
    
    try:
        # Create generator instance
        generator = PlanningPromptGenerator(use_one_shot=args.one_shot)
        
        # Process domains
        all_data = {}
        data_path = Path(args.data_path)
        output_path = Path(args.output_path)
        if args.domain:
            # Process specific domain
            domain_path = data_path / args.domain
            if not domain_path.exists():
                raise FileNotFoundError(f"Domain {args.domain} not found in {data_path}")
            
            domain_data = generator.process_domain(str(domain_path), str(output_path))
            if domain_data:
                all_data[args.domain] = domain_data
                print(f"Processed domain: {args.domain}")
            
        else:
            # Process all domains
            domains = get_domains(str(data_path))

            for domain in domains:
                domain_path = data_path / domain
                domain_data = generator.process_domain(str(domain_path), str(output_path))
                if domain_data:
                    all_data[domain] = domain_data
                    print(f"Processed domain: {domain}")
        
        if all_data:
            # Save summary JSON with all domains
            summary_file = output_path / "all_domains.json"
            with open(summary_file, 'w') as f:
                json.dump(all_data, f, indent=2)
            
            print(f"\nAll prompts generated and saved to: {output_path}")
            print(f"Summary file created at: {summary_file}")
        else:
            print("No domains were successfully processed")
        
    except FileNotFoundError as e:
        print(f"Error: Could not find file or directory - {e}")
    except Exception as e:
        print(f"Error: An unexpected error occurred - {e}")
