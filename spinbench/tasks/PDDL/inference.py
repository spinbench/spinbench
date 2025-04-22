import json
from typing import List, Dict, Union, Optional, Any
import argparse
import os
from pathlib import Path
import openai
import concurrent.futures
import threading
from queue import Queue
from tools.chat_service import get_chat


def extract_json_from_response(response: str) -> str:
    """
    Clean and extract JSON content from the response.
    
    Args:
        response (str): Raw response from LLM
        
    Returns:
        str: Cleaned JSON string
    """
    try:
        start_idx = response.find("$$\n")
        end_idx = response.rfind("\n$$")
        
        if start_idx != -1 and end_idx != -1:
            return response[start_idx + 3:end_idx].strip()
        return response
    except Exception:
        return response

def extract_plan_from_response(response: str) -> str:
    """
    Extract the plan from the LLM response.
    
    Args:
        response (str): Raw response from LLM
        
    Returns:
        str: Extracted plan or error message
    """
    try:
        json_str = extract_json_from_response(response)
        response_json = json.loads(json_str)
        return response_json.get("plan", "No plan found in response")
    except json.JSONDecodeError:
        return "Error: Could not parse response as JSON"

def process_instance(args):
    """
    Process a single PDDL instance.
    
    Args:
        args: Tuple containing (model, prompt_data, output_file, full_text_file)
    
    Returns:
        tuple: (success, instance_name, error_message)
    """
    model, prompt_data, output_file, full_text_file = args
    instance_name = prompt_data["instance"]
    
    try:
        # Send prompt to LLM
        # response = model(prompt_data["prompt"])
        # todo: add device specification for local model
        response = get_chat(model, prompt_data["prompt"])
        
        # Save full text response
        with open(full_text_file, 'w') as f:
            f.write(response)
        
        # Extract and save plan
        plan = extract_plan_from_response(response)
        with open(output_file, 'w') as f:
            f.write(plan)
            
        return True, instance_name, None
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        # Write error to both files
        for file_path in [output_file, full_text_file]:
            with open(file_path, 'w') as f:
                f.write(error_msg)
        return False, instance_name, str(e)

def process_domain(domain_data: Dict[str, Any], output_base: Path, model, is_api_model: bool) -> None:
    """
    Process all instances in a domain using thread pool for API-based models.
    
    Args:
        domain_data: Domain data from the JSON file
        output_base: Base path for output
        model: the model name or model path
        is_api_model: boolean indicating if model is API-based
    """
    domain_name = domain_data["domain"]
    
    # Create output directories
    domain_output = output_base / "pddl" / domain_name
    domain_output.mkdir(parents=True, exist_ok=True)
    
    full_text_dir = output_base / "full_text" / domain_name
    full_text_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing domain: {domain_name}")
    
    # Prepare tasks list
    tasks = []
    for prompt_data in domain_data["prompts"]:
        instance_name = prompt_data["instance"]
        output_file = domain_output / f"{Path(instance_name).stem}.sol"
        full_text_file = full_text_dir / f"{Path(instance_name).stem}.txt"
        
        tasks.append((model, prompt_data, output_file, full_text_file))
    
    if is_api_model:
        # Process with thread pool for API models
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(process_instance, task) for task in tasks]
            
            for future in concurrent.futures.as_completed(futures):
                success, instance_name, error = future.result()
                if success:
                    print(f"  Completed instance: {instance_name}")
                else:
                    print(f"  Error processing {instance_name}: {error}")
    else:
        # Process sequentially for local models
        for task in tasks:
            success, instance_name, error = process_instance(task)
            if success:
                print(f"  Completed instance: {instance_name}")
            else:
                print(f"  Error processing {instance_name}: {error}")

def read_json_input(input_path: str) -> Dict[str, Any]:
    """
    Read and parse input JSON file, handling both all_domains.json and single domain JSON.
    
    Args:
        input_path: Path to the JSON file
        
    Returns:
        dict: Dictionary containing domain data
    """
    with open(input_path, 'r') as f:
        data = json.load(f)
        
    if "domain" in data:
        return {"single_domain": data}
    else:
        return data

def main():
    parser = argparse.ArgumentParser(description='Generate solutions for PDDL problems')
    parser.add_argument('--input', default="spinbench/tasks/PDDL/planning_task_with_prompts/all_domains.json",
                        help='Path to domains.json, default would be all_domains.json')
    parser.add_argument('--output', required=True,
                        help='Base path for output directories')
    parser.add_argument('--model', default="gpt-4o",
                        help='Model type/name to use')
# 
    args = parser.parse_args()
    output_base = Path(args.output)
    output_base.mkdir(parents=True, exist_ok=True)
    
    domains_data = read_json_input(args.input)
    
    # Check if model is API-based before initialization
    model_type = args.model
    # for api based, create threading to increase speed
    is_api_model = any(name in model_type for name in ['gpt', 'o1', 'o3','o4','claude', 'deepseek', 'together','gemini'])
    
    print(is_api_model)
    # Initialize model
    # if is_api_model:
    #     model = lpb.BlackboxLLM(args.model)
    # else:
    #     model = lpb.BlackboxLLM(args.model, device='cuda:1')

    for domain_name, domain_data in domains_data.items():
        process_domain(domain_data, output_base, args.model, is_api_model)
        
    print("\nProcessing complete!")
    print(f"Solutions saved to: {output_base}")

if __name__ == "__main__":
    main()
