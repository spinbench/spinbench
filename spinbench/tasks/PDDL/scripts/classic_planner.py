import subprocess
import os
import time
import glob
import argparse
from pathlib import Path
import shutil
import signal

def generate_plan(domain_file, problem_file, output_file, downward_path='submodule/downward/fast-downward.py', timeout=10):
    """
    Generate plan for a single problem instance with timeout
    """
    try:
        cmd = [
            "python3", downward_path,
            "--alias", "lama-first",
            "--plan-file", output_file,
            domain_file,
            problem_file
        ]

        print(f"\nGenerating plan for problem: {problem_file}")
        print(f"Output will be saved to: {output_file}")

        # Run process with timeout
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, preexec_fn=os.setsid)
        
        try:
            # Wait for process with timeout
            stdout, stderr = process.communicate(timeout=timeout)
            
            # Check if plan file exists
            if os.path.exists(output_file):
                print(f"Plan generated successfully: {output_file}")
                return True
            else:
                print("No plan generated within time limit.")
                return False
                
        except subprocess.TimeoutExpired:
            # Kill the entire process group
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            print(f"Plan generation timed out after {timeout} seconds.")
            return False

    except Exception as e:
        print(f"Error during plan generation: {e}")
        return False

def process_domain(domain_name, base_path, output_base_path, downward_path):
    """
    Process all instances for a specific domain
    """
    print(f"\nProcessing domain: {domain_name}")
    
    # Set up paths
    domain_path = os.path.join(base_path, domain_name)
    instance_path = os.path.join(domain_path, "instances")
    output_path = os.path.join(output_base_path, domain_name)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Find domain file
    domain_file = None
    for file in os.listdir(domain_path):
        if file.startswith("domain") and file.endswith(".pddl"):
            domain_file = os.path.join(domain_path, file)
            break
    
    if not domain_file:
        print(f"No domain file found in {domain_path}")
        return
    
    # Process all problem instances
    problem_files = sorted([f for f in os.listdir(instance_path) if f.endswith('.pddl')])
    
    for idx, problem_file in enumerate(problem_files, 1):
        problem_path = os.path.join(instance_path, problem_file)
        # Get the base name without .pddl and add .sol
        output_filename = problem_file.replace('.pddl', '.sol')
        output_file = os.path.join(output_path, output_filename)
        
        print(f"\nProcessing problem {idx}/{len(problem_files)}: {problem_file}")
        generate_plan(domain_file, problem_path, output_file, downward_path)

def main():
    parser = argparse.ArgumentParser(description='Generate plans for PDDL domains and problems')
    parser.add_argument('--domain', default='', help='Specific domain to process (leave empty for all domains)')
    parser.add_argument('--input', default='data/pddl', help='Base path for domains')
    parser.add_argument('--output_path', default='experiments/fd_init_final', help='Base path for output')
    parser.add_argument('--downward_path', default='submodule/downward/fast-downward.py', 
                        help='Path to fast-downward.py')
    
    args = parser.parse_args()
    
    # Create base output directory
    os.makedirs(args.output_path, exist_ok=True)
    
    if args.domain:
        # Process specific domain
        process_domain(args.domain, args.input, args.output_path, args.downward_path)
    else:
        # Process all domains
        domains = [d for d in os.listdir(args.input) 
                  if os.path.isdir(os.path.join(args.input, d)) and 
                  not d.startswith('.') and
                  os.path.exists(os.path.join(args.input, d, 'instances'))]
        
        print(f"Found {len(domains)} domains: {domains}")
        
        for domain in domains:
            process_domain(domain, args.input, args.output_path, args.downward_path)

if __name__ == "__main__":
    main()