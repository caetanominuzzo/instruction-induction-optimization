import sys
import json
import logging
import itertools
from llm_operations import (
    num_tokens_from_string,
    extract_instructions,
    compare_instructions,
    generate_combinations,
    rank_combinations,
)

# Custom parameters
MODEL = "text-davinci-002"
MAX_TOKENS = 150
TEMPERATURE = 0.0
PENALTY = 0.0
INSTRUCTION_EXTRACTION_PROMPT = "Given the following input/output pairs, determine the transformation rule that turns the input into the output. Provide the result in plain text and be concise: "
INSTRUCTION_COMPARISON_PROMPT = "Compare these two sets of instructions and indicate if both determine the same transformation. Provide the result as 'Yes' or 'No', without any additional explanation: "


token_usage = {
    "prompt_tokens": 0,
    "completion_tokens": 0,
}


def load_dataset_from_file(file_path: str):
    with open(file_path, "r") as file:
        dataset = json.load(file)
    return dataset


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        original_dataset = load_dataset_from_file(file_path)
    else:
        print("No dataset file provided.")
        use_example = input(
            "Do you want to use the example dataset? [y/N] ").lower()
        if use_example == 'y':
            file_path = "dataset-example-fibonacci-sequence.json"
            original_dataset = load_dataset_from_file(file_path)
        else:
            print("No dataset selected. Exiting.")
            sys.exit()

    # Calculate the total number of tokens in the dataset
    total_dataset_tokens = sum(
        num_tokens_from_string(point["input"]) +
        num_tokens_from_string(point["output"])
        for point in original_dataset
    )

    # Calculate the total number of tokens in the system prompts
    total_prompt_tokens = num_tokens_from_string(
        instruction_extraction_prompt) + num_tokens_from_string(instruction_comparison_prompt)

    # Calculate the total number of combinations
    total_combinations = sum(
        len(list(itertools.combinations(original_dataset, i)))
        for i in range(1, len(original_dataset) + 1)
    )

    # Estimate the total number of tokens that will be consumed during the process
    estimated_total_tokens = (
        total_dataset_tokens + total_prompt_tokens) * total_combinations

    # Ask the user to confirm or abort before the main loop takes place
    print(f"Estimated total tokens to be consumed: {estimated_total_tokens}")
    user_confirmation = input("Do you want to proceed? [y/N]: ").lower()
    if user_confirmation != "y":
        print("Aborting.")
        sys.exit()

    # Extract initial instructions
    initial_instructions, instruction_token_usage = extract_instructions(
        original_dataset, MODEL, MAX_TOKENS, TEMPERATURE, PENALTY, INSTRUCTION_EXTRACTION_PROMPT)
    token_usage["prompt_tokens"] += instruction_token_usage["prompt_tokens"]
    token_usage["completion_tokens"] += instruction_token_usage["completion_tokens"]

    # Initialize variables
    iteration_number = 1
    data_point_scores = {
        (point['input'], point['output']): 0 for point in original_dataset}

    successful_combinations = []

    # Iterate through data points
    while len(original_dataset) - iteration_number > 0:

        logging.info(
            f"\n== Starting iteration n. {iteration_number}. ==")

        equivalent_combinations = []

        # Calculate combinations for the current iteration
        combinations = generate_combinations(
            original_dataset, len(original_dataset) - iteration_number)

        # Evaluate each combination
        for combination in combinations:
            new_instructions, comparison_token_usage = extract_instructions(
                combination, MODEL, MAX_TOKENS, TEMPERATURE, PENALTY, INSTRUCTION_EXTRACTION_PROMPT)
            token_usage["prompt_tokens"] += comparison_token_usage["prompt_tokens"]
            token_usage["completion_tokens"] += comparison_token_usage["completion_tokens"]

            # Compare instructions
            are_instructions_equivalent, comparison_token_usage = compare_instructions(
                initial_instructions, new_instructions, MODEL, MAX_TOKENS, TEMPERATURE, PENALTY, INSTRUCTION_COMPARISON_PROMPT
            )
            token_usage["prompt_tokens"] += comparison_token_usage["prompt_tokens"]
            token_usage["completion_tokens"] += comparison_token_usage["completion_tokens"]

            if are_instructions_equivalent:
                equivalent_combinations.append(combination)

                # Update the score for each participating data point
                for point in combination:
                    data_point_scores[(point['input'], point['output'])] += 1

        # If no equivalent combinations are found, stop the iteration process
        if not equivalent_combinations:
            break

        successful_combinations.extend(equivalent_combinations)
        iteration_number += 1

    # Analyze successful combinations and data_point_scores to determine the optimal dataset
    if successful_combinations:
        minimal_size = min(len(comb) for comb in successful_combinations)
    else:
        minimal_size = 0

    minimal_successful_combinations = [
        comb for comb in successful_combinations if len(comb) == minimal_size]

    weights = {'total_score': 1, 'avg_dependency': -1, 'redundancy': -1}
    ranked_combinations, ranked_combination_metrics, ranked_combination_weighted_sums = rank_combinations(
        minimal_successful_combinations, data_point_scores, weights)

    # Print the best combination with its metrics and weighted sum
    print("Ranked combinations with metrics and weighted sum:")
    for i, combination in enumerate(ranked_combinations):
        print(f"Combination {i+1}: {combination}")
        print(f"Metrics: {ranked_combination_metrics[i]}")
        print(f"Weighted sum: {ranked_combination_weighted_sums[i]}\n")

    # Print the token usage report
    print("Token usage report:")
    print(f"Prompt tokens: {token_usage['prompt_tokens']}")
    print(f"Completion tokens: {token_usage['completion_tokens']}")
    print(
        f"Total tokens: {token_usage['prompt_tokens'] + token_usage['completion_tokens']}")


if __name__ == "__main__":
    main()
