import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, Any
import os 
from collections import Counter  # Add Counter import

def save_summary_csv(results: Dict[str, Any], output_path: str):
    """
    Save domain summary results to a CSV file.
    
    Args:
        results: Dictionary containing validation results
        output_path: Path to save the CSV file
    """
    import csv
    
    csv_path = os.path.join(output_path, "summary.csv")
    
    # Prepare CSV headers and rows
    headers = ['Domain', 'Accuracy', 'Valid', 'Total']
    rows = []
    
    # Generate rows for each domain
    for domain, data in results.items():
        if domain != "overall_summary":  # Skip overall summary in CSV
            summary = data["summary"]
            rows.append([
                domain,
                f"{summary['accuracy']:.2f}",
                str(summary['valid']),
                str(summary['total'])
            ])
    
    # Sort rows by domain name
    rows.sort(key=lambda x: x[0])
    
    # Write to CSV
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"Summary CSV saved to: {csv_path}")


def save_domain_scores_csv(results: Dict[str, Any], output_path: str):
    """
    Save domain scores to a CSV file, grouped by domain type.
    
    Args:
        results: Dictionary containing validation results
        output_path: Path to save the CSV file
    """
    import csv
    
    # Domain classification mapping
    domain_classifications = {
        # Spatial Planning Domains
        "drone": "spatial",
        "floortile": "spatial",
        "grid": "spatial",
        "logistics": "spatial",
        "sokoban": "spatial",
        "termes": "spatial",
        
        # Sequential Reasoning Domains
        "assembly": "sequential",
        "blocksworld": "sequential",
        "briefcaseworld": "sequential",
        "Multi_Agent_coordination": "sequential",
        "cooperate_sequential_gripper": "sequential",
        "elevator": "sequential",
        "barman": "sequential",
        
        # Resource Management Domains
        "counters": "resource",
        "depots": "resource",
        "markettrader": "resource",
        "satellite": "resource",
        "freecell": "resource",
        "rovers": "resource",
        "settlersnumeric": "resource",
        "sugar": "resource"
    }
    
    # Calculate scores by domain type
    domain_type_scores = {
        "spatial": {"total_valid": 0, "total_instances": 0},
        "sequential": {"total_valid": 0, "total_instances": 0},
        "resource": {"total_valid": 0, "total_instances": 0}
    }
    
    # Collect scores for each domain
    domain_scores = []
    for domain, data in results.items():
        if domain != "overall_summary":
            domain_type = domain_classifications.get(domain, "unknown")
            summary = data["summary"]
            
            score_entry = {
                "domain": domain,
                "type": domain_type,
                "accuracy": summary["accuracy"],
                "valid": summary["valid"],
                "total": summary["total"]
            }
            domain_scores.append(score_entry)
            
            # Add to type totals
            if domain_type in domain_type_scores:
                domain_type_scores[domain_type]["total_valid"] += summary["valid"]
                domain_type_scores[domain_type]["total_instances"] += summary["total"]
    
    # Calculate averages by type
    type_averages = {}
    for dtype, scores in domain_type_scores.items():
        if scores["total_instances"] > 0:
            avg = (scores["total_valid"] / scores["total_instances"]) * 100
            type_averages[dtype] = avg
        else:
            type_averages[dtype] = 0.0
    
    # Save to CSV
    csv_path = os.path.join(output_path, "domain_scores.csv")
    headers = ['Domain', 'Type', 'Accuracy', 'Valid', 'Total']
    
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        # Write individual domain scores
        for score in sorted(domain_scores, key=lambda x: (x["type"], x["domain"])):
            writer.writerow([
                score["domain"],
                score["type"],
                f"{score['accuracy']:.2f}",
                score["valid"],
                score["total"]
            ])
        
        # Write type averages
        writer.writerow([])  # Empty row for separation
        writer.writerow(["Type Averages", "", "", "", ""])
        for dtype, avg in sorted(type_averages.items()):
            writer.writerow([
                dtype,
                "average",
                f"{avg:.2f}",
                domain_type_scores[dtype]["total_valid"],
                domain_type_scores[dtype]["total_instances"]
            ])
    
    print(f"Domain scores saved to: {csv_path}")


def validate_plan(domain_file: str, problem_file: str, plan_file: str) -> Dict[str, Any]:
    """
    Validate a single plan using VAL.
    
    Returns:
        dict with validation results
    """
    # try:
    result = subprocess.run(
        ["spinbench/tasks/PDDL/submodules/VAL/validate", domain_file, problem_file, plan_file],
        capture_output=True,
        text=True,
        check=False
    )
    
    output = result.stdout + result.stderr
    is_valid = "Plan valid" in output
    
    # Try to extract plan cost if available
    cost = None
    for line in output.split('\n'):
        if "Plan cost: " in line:
            try:
                cost = float(line.split("Plan cost: ")[1].strip())
            except (ValueError, IndexError):
                pass
    
    return {
        "valid": is_valid,
        "output": output,
        "cost": cost,
        "error": None
    }
    # except Exception as e:
    #     return {
    #         "valid": False,
    #         "output": None,
    #         "cost": None,
    #         "error": str(e)
    #     }

def validate_domain(domain_name: str, data_path: str, solutions_path: str) -> Dict[str, Any]:
    """
    Validate all solutions for a domain.
    """
    domain_path = Path(data_path) / domain_name
    domain_file = None
    
    # Find domain file
    for file in domain_path.glob("domain*.pddl"):
        domain_file = file
        break
    if not domain_file:
        return {
            "error": f"No domain file found in {domain_path}",
            "instances": {}
        }
    
    results = {
        "domain_file": str(domain_file),
        "instances": {},
        "summary": {
            "total": 0,
            "valid": 0,
            "accuracy": 0.0
        }
    }
    
    # Process each instance
    instance_dir = domain_path / "instances"
    solutions_dir = Path(solutions_path) / domain_name
    
    if not instance_dir.exists():
        results["error"] = f"No instances directory found in {domain_path}"
        return results
        
    valid_count = 0
    total_count = 0
    # breakpoint()
    for instance_file in sorted(instance_dir.glob("*.pddl")):
        instance_name = instance_file.stem
        solution_file = solutions_dir / f"{instance_name}.sol"
        
        if solution_file.exists():
            # breakpoint()
            total_count += 1
            validation_result = validate_plan(
                str(domain_file),
                str(instance_file),
                str(solution_file)
            )
            
            if validation_result["valid"]:
                valid_count += 1
                
            results["instances"][instance_name] = {
                "problem_file": str(instance_file),
                "solution_file": str(solution_file),
                **validation_result
            }
    
    # Calculate summary
    results["summary"]["total"] = total_count
    results["summary"]["valid"] = valid_count
    results["summary"]["accuracy"] = (valid_count / total_count * 100) if total_count > 0 else 0
    
    return results

def analyze_validation_results(file_path, output_path):
    """
    Analyze validation results and categorize errors and successes.
    
    Args:
        file_path: Path to the validation results JSON file
        output_path: Path to save the detailed analysis JSON file
    """
    # Read the JSON file
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Initialize counters
    result_types = Counter()
    
    # Process each domain
    for domain_name, domain_data in data.items():
        if isinstance(domain_data, dict) and 'instances' in domain_data:
            # Process each instance
            for instance_name, instance_data in domain_data['instances'].items():
                if 'output' in instance_data and instance_data['output']:
                    output = instance_data['output']
                    valid = instance_data.get('valid', False)
                    
                    # Success patterns
                    if "Plan valid" in output:
                        result_types["Success: Plan valid"] += 1
                    elif "Plan executed successfully" in output and valid:
                        result_types["Success: Plan executed successfully"] += 1
                    # Error patterns
                    elif "Plan failed to execute" in output:
                        result_types["Error: Plan failed to execute"] += 1
                    elif "Bad plan description" in output:
                        result_types["Error: Bad plan description"] += 1
                    elif "Error in type-checking" in output:
                        result_types["Error: Type checking failed"] += 1
                    elif "Goal not satisfied" in output:
                        result_types["Error: Goal not satisfied"] += 1
                    else:
                        result_types["Other: Unclassified"] += 1

                    # Additional checks for specific error messages
                    if "syntax error" in output.lower():
                        result_types["Error: Syntax error"] += 1
                    if "invalid operator" in output.lower():
                        result_types["Error: Invalid operator"] += 1
                    if "undefined" in output.lower():
                        result_types["Error: Undefined reference"] += 1
                    if "precondition" in output.lower():
                        result_types["Error: Precondition failure"] += 1
    
    # Group results by category
    categorized_results = {
        "successes": {k: v for k, v in result_types.items() if k.startswith("Success")},
        "errors": {k: v for k, v in result_types.items() if k.startswith("Error")},
        "warnings": {k: v for k, v in result_types.items() if k.startswith("Warning")},
        "other": {k: v for k, v in result_types.items() if k.startswith("Other")}
    }
    
    # Calculate statistics
    stats = {
        "total_instances": sum(result_types.values()),
        "total_successes": sum(v for k, v in result_types.items() if k.startswith("Success")),
        "total_errors": sum(v for k, v in result_types.items() if k.startswith("Error")),
        "total_warnings": sum(v for k, v in result_types.items() if k.startswith("Warning")),
        "success_rate": round(sum(v for k, v in result_types.items() if k.startswith("Success")) / 
                            sum(result_types.values()) * 100, 2) if sum(result_types.values()) > 0 else 0
    }
    
    # Prepare final results
    results = {
        "detailed_counts": dict(result_types),
        "categorized_results": categorized_results,
        "statistics": stats
    }
    
    # Save results to JSON
    output_file = os.path.join(output_path, "validation_analysis_detailed.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\nValidation Analysis Summary:")
    print("=" * 50)
    print("\nStatistics:")
    for stat, value in stats.items():
        if isinstance(value, float):
            print(f"{stat}: {value:.2f}%")
        else:
            print(f"{stat}: {value}")

    print("\nDetailed Results by Category:")
    print("-" * 50)
    for category, category_results in categorized_results.items():
        if category_results:  # Only print categories that have results
            print(f"\n{category.upper()}:")
            for result_type, count in category_results.items():
                print(f"  {result_type}: {count}")
    
    print(f"\nDetailed analysis saved to: {output_file}")
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Validate PDDL solutions")
    parser.add_argument('--data_path', default='spinbench/tasks/PDDL/classical_planning_dataset',
                        help='Base path containing domain directories')
    parser.add_argument('--solutions_path', default='save/<model_name>/pddl',
                        help='Base path containing solution directories')
    parser.add_argument('--output_path', default='results/<model_name>',
                        help='Path to save validation results')
    parser.add_argument('--domain', default='',
                        help='Specific domain to validate (empty for all domains)')
    parser.add_argument('--analyze_only', action='store_true',
                        help='Only analyze existing validation results without running validation')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output_path, exist_ok=True)
    
    json_path = os.path.join(args.output_path, "validation_results.json")
    
    if args.analyze_only:
        if os.path.exists(json_path):
            print(f"Analyzing existing validation results from: {json_path}")
            analyze_validation_results(json_path, args.output_path)
            return
        else:
            print(f"Error: Validation results file not found at {json_path}")
            print("Run validation first or specify the correct path.")
            return
    
    # data_path = Path(args.data_path)
    results = {}
    
    try:
        if args.domain:
            # Validate specific domain
            domains = [args.domain]
        else:
            # Validate all domains
            domains = [d.name for d in Path(args.solutions_path).iterdir() if d.is_dir()]
        
        total_instances = 0
        total_valid = 0
        
        for domain in sorted(domains):
            print(f"Validating domain: {domain}")
            domain_results = validate_domain(domain, args.data_path, args.solutions_path)
            results[domain] = domain_results
            
            # Update totals
            total_instances += domain_results["summary"]["total"]
            total_valid += domain_results["summary"]["valid"]
            
            # Print domain summary
            print(f"  Instances: {domain_results['summary']['total']}")
            print(f"  Valid solutions: {domain_results['summary']['valid']}")
            print(f"  Accuracy: {domain_results['summary']['accuracy']:.2f}%")
            print()
        
        # Add overall summary
        results["overall_summary"] = {
            "total_instances": total_instances,
            "total_valid": total_valid,
            "overall_accuracy": (total_valid / total_instances * 100) if total_instances > 0 else 0
        }
        
        # Save results
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save CSV summary - now to output_path instead of solutions_path
        save_summary_csv(results, args.output_path)
        save_domain_scores_csv(results, args.output_path)
        
        print("Overall Summary:")
        print(f"Total instances: {total_instances}")
        print(f"Total valid solutions: {total_valid}")
        print(f"Overall accuracy: {results['overall_summary']['overall_accuracy']:.2f}%")
        print(f"\nResults saved to: {json_path}")
        
        # Run detailed analysis on the results
        print("\nRunning detailed analysis of validation results...")
        analyze_validation_results(json_path, args.output_path)
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
