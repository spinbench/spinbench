import argparse
import json
import subprocess
from pathlib import Path
from typing import Dict, Any
import os 

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
        ["submodule/VAL/validate", domain_file, problem_file, plan_file],
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

def main():
    parser = argparse.ArgumentParser(description="Validate PDDL solutions")
    parser.add_argument('--data_path', default='data/pddl',
                        help='Base path containing domain directories')
    parser.add_argument('--solutions_path', default='experiments/init_run',
                        help='Base path containing solution directories')
    # parser.add_argument('--output', default='validation_results.json',
    #                     help='Path to save validation results')
    parser.add_argument('--domain', default='',
                        help='Specific domain to validate (empty for all domains)')
    
    args = parser.parse_args()
    
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
        json_path = os.path.join(args.solutions_path, "validation_results.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Save CSV summary
        save_summary_csv(results, args.solutions_path)
        save_domain_scores_csv(results, args.solutions_path)
        
        print("Overall Summary:")
        print(f"Total instances: {total_instances}")
        print(f"Total valid solutions: {total_valid}")
        print(f"Overall accuracy: {results['overall_summary']['overall_accuracy']:.2f}%")
        print(f"\nResults saved to: {json_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
