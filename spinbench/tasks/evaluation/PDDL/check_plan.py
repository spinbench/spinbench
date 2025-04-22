from collections import Counter
import re
import json  # Added missing json import

def analyze_validation_results(file_path):
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
    output_file = "validation_analysis_detailed.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

# Run the analysis
# experiments/01_30_final_results/claude-3-5-sonnet-20241022
file_path = "experiments/01_30_final_results/DeepSeek-R1/pddl/validation_results.json"
results = analyze_validation_results(file_path)

# Print summary
print("\nValidation Analysis Summary:")
print("=" * 50)
print("\nStatistics:")
for stat, value in results["statistics"].items():
    if isinstance(value, float):
        print(f"{stat}: {value:.2f}%")
    else:
        print(f"{stat}: {value}")

print("\nDetailed Results by Category:")
print("-" * 50)
for category, category_results in results["categorized_results"].items():
    if category_results:  # Only print categories that have results
        print(f"\n{category.upper()}:")
        for result_type, count in category_results.items():
            print(f"  {result_type}: {count}")
