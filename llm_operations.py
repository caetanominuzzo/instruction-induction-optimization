import openai
import os
import itertools
import logging
import tiktoken
from typing import List, Dict, Tuple


openai.api_key = os.environ["OPENAI_API_KEY"]

instruction_extraction_prompt = "Given the following input/output pairs, determine the transformation rule that turns the input into the output. Provide the result in plain text and be concise: "
instruction_comparison_prompt = "Compare these two sets of instructions and indicate if they are equivalent. Provide the result as 'Yes' or 'No', without any additional explanation: "


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def extract_instructions(dataset: List[Dict[str, int]]) -> str:
    # Function to extract instructions from ChatGPT using the dataset
    prompt = f"{instruction_extraction_prompt} {dataset}"
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
        presence_penalty=0


    )
    logging.info(
        "\nSubset:\n\t%s\nInduced instruction:\n\t%s",
        dataset,
        response.choices[0].text.strip().replace("\n", " ")
    )
    return response.choices[0].text.strip().replace("\n", " ")


def compare_instructions(instructions_1: str, instructions_2: str) -> bool:
    # Function to compare two sets of instructions using ChatGPT
    prompt = f"{instruction_comparison_prompt}\n\t{instructions_1}\n\t{instructions_2}"
    model = "text-davinci-002"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0,
        presence_penalty=0
    )
    logging.info(
        "\nInstructions A:\n\t%s\nInstructions B:\n\t%s\nInstructions are equivalent:\n\t%s",
        instructions_1,
        instructions_2,
        response.choices[0].text.strip().replace("\n", " "))
    return "Yes" in response.choices[0].text.strip()


def generate_combinations(dataset: List[Dict[str, int]], num_elements: int) -> List[List[Dict[str, int]]]:
    # Function to generate all combinations of the dataset with 'num_elements'
    return list(itertools.combinations(dataset, num_elements))


def rank_combinations(
    minimal_successful_combinations: List[List[Dict[str, int]]],
    data_point_scores: Dict[Tuple[int, int], int],
    weights: Dict[str, float]
) -> Tuple[List[List[Dict[str, int]]], List[Dict[str, float]], List[float]]:

    def combination_metrics(combination: List[Dict[str, int]]) -> Dict[str, float]:
        total_score = sum(
            data_point_scores[(point['input'], point['output'])] for point in combination)
        avg_dependency = total_score / len(combination)
        redundancy = len(
            combination) - len(set((point['input'], point['output']) for point in combination))

        return {
            'total_score': total_score,
            'avg_dependency': avg_dependency,
            'redundancy': redundancy
        }

    # Calculate metrics for each combination
    combination_metric_lists = [
        combination_metrics(combination) for combination in minimal_successful_combinations
    ]

    # Calculate weighted sum of metrics for each combination
    combination_weighted_sums = [
        sum(metrics[key] * weights[key] for key in weights) for metrics in combination_metric_lists
    ]

    # Sort combinations based on the weighted sum of metrics
    sorted_combinations, sorted_combination_metrics, sorted_combination_weighted_sums = zip(*sorted(
        zip(minimal_successful_combinations,
            combination_metric_lists, combination_weighted_sums),
        key=lambda x: x[2]
    ))

    return list(sorted_combinations), list(sorted_combination_metrics), list(sorted_combination_weighted_sums)
