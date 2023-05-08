import openai
import os
import itertools
import logging
import tiktoken
from typing import List, Dict, Tuple


openai.api_key = os.environ["OPENAI_API_KEY"]


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def extract_instructions(
    dataset: List[Dict[str, str]],
    model: str,
    max_tokens: int,
    temperature: float,
    penalty: float,
    prompt: str,
) -> Tuple[str, Dict[str, int]]:
    # Function to extract instructions from ChatGPT using the dataset
    prompt = f"{prompt} {dataset}"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        presence_penalty=penalty,
    )

    logging.info(
        "\nSubset:\n\t%s\nInduced instruction:\n\t%s",
        dataset,
        response.choices[0].text.strip().replace("\n", " ")
    )

    token_usage = {
        "prompt_tokens": response["usage"]["prompt_tokens"],
        "completion_tokens": response["usage"]["completion_tokens"],
    }

    return (
        response.choices[0].text.strip().replace("\n", ""),
        token_usage,
    )


def compare_instructions(
    instructions_1: str,
    instructions_2: str,
    model: str,
    max_tokens: int,
    temperature: float,
    penalty: float,
    prompt: str,
) -> Tuple[bool, Dict[str, int]]:
    # Function to compare two sets of instructions using ChatGPT
    prompt = f"{prompt}\n\t{instructions_1}\n\t{instructions_2}"
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        n=1,
        stop=None,
        temperature=temperature,
        presence_penalty=penalty,
    )
    logging.info(
        "\nInstructions A:\n\t%s\nInstructions B:\n\t%s\nInstructions are equivalent:\n\t%s",
        instructions_1,
        instructions_2,
        response.choices[0].text.strip().replace("\n", " "))

    token_usage = {
        "prompt_tokens": response["usage"]["prompt_tokens"],
        "completion_tokens": response["usage"]["completion_tokens"],
    }

    return "Yes" in response.choices[0].text.strip(), token_usage


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
