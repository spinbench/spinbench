#!/bin/bash

# Default values
DATA_PATH="spinbench/tasks/PDDL/classical_planning_dataset"
MODEL="gpt-4o"

# Function to print usage
print_usage() {
    echo "Usage: $0 -e EXPERIMENT_NAME [-d DOMAIN] [-m MODEL]"
    echo "  -e EXPERIMENT_NAME : Name of the experiment (required)"
    echo "  -d DOMAIN         : Specific domain to process (optional)"
    echo "  -m MODEL          : Model to use (default: gpt-4)"
    echo "  -h               : Display this help message"
}

# Parse command line arguments
while getopts "e:d:m:h" opt; do
    case $opt in
        e) EXPERIMENT_NAME="$OPTARG";;
        d) DOMAIN="$OPTARG";;
        m) MODEL="$OPTARG";;
        h) print_usage; exit 0;;
        ?) print_usage; exit 1;;
    esac
done

# Check if experiment name is provided
if [ -z "$EXPERIMENT_NAME" ]; then
    echo "Error: Experiment name is required"
    print_usage
    exit 1
fi

# Setup directories
PROMPT_DIR="spinbench/tasks/PDDL/planning_task_with_prompts"
EXPERIMENT_DIR="save/PDDL/$EXPERIMENT_NAME/$MODEL"
mkdir -p "$PROMPT_DIR"
mkdir -p "$EXPERIMENT_DIR"

echo "Starting planning pipeline..."
echo "Experiment name: $EXPERIMENT_NAME"
echo "Model: $MODEL"
if [ ! -z "$DOMAIN" ]; then
    echo "Domain: $DOMAIN"
fi

# Step 1: Generate prompts
echo -e "\n=== Generating Prompts ==="
if [ ! -z "$DOMAIN" ]; then
    python -m spinbench.tasks.PDDL.prompt_generation.generate_plan_prompt --domain "$DOMAIN" --data_path "$DATA_PATH" --output_path "$PROMPT_DIR"
else
    python -m spinbench.tasks.PDDL.prompt_generation.generate_plan_prompt --data_path "$DATA_PATH" --output_path "$PROMPT_DIR"
fi

# Check if prompt generation was successful
if [ $? -ne 0 ]; then
    echo "Error: Prompt generation failed"
    exit 1
fi

# Step 2: Solve plans
echo -e "\n=== Solving Plans ==="
if [ ! -z "$DOMAIN" ]; then
    # For single domain, use the domain-specific JSON file
    INPUT_FILE="$PROMPT_DIR/${DOMAIN}.json"
else
    # For all domains, use the combined JSON file
    INPUT_FILE="$PROMPT_DIR/all_domains.json"
fi

python -m spinbench.tasks.PDDL.inference --input "$INPUT_FILE" --output "$EXPERIMENT_DIR" --model "$MODEL"

# Check if solving was successful
if [ $? -ne 0 ]; then
    echo "Error: Plan solving failed"
    exit 1
fi

# Step 3: Validate results
echo -e "\n=== Validating Results ==="
if [ ! -z "$DOMAIN" ]; then
    python -m spinbench.tasks.evaluation.PDDL.validate_plans --data_path "$DATA_PATH" --solutions_path "$EXPERIMENT_DIR/pddl" --domain "$DOMAIN" --output_path "results/PDDL/$MODEL"
else
    python -m spinbench.tasks.evaluation.PDDL.validate_plans --data_path "$DATA_PATH" --solutions_path "$EXPERIMENT_DIR/pddl" --output_path "results/PDDL/$MODEL"
fi

# Check if validation was successful
if [ $? -ne 0 ]; then
    echo "Error: Validation failed"
    exit 1
fi

echo -e "\n=== Pipeline Complete ==="
echo "LLM PDDL results are available in: $EXPERIMENT_DIR"
echo "evluation results are available in: results/PDDL/$MODEL"
echo "- Solutions: $EXPERIMENT_DIR/pddl/"
echo "- Full responses: $EXPERIMENT_DIR/full_text/"
echo "- Validation results: $EXPERIMENT_DIR/validation_results.json"
echo "- Summary: $EXPERIMENT_DIR/summary.csv"