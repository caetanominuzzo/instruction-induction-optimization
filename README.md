# Optimizing Few-Shot Learning with Instruction Induction using ChatGPT

This repository contains a Python implementation of a brute force method to optimize few-shot learning using instruction induction with ChatGPT.

## Index

[Introduction](#introduction)  
[How it works](#how-it-works)  
[Requirements](#requirements)  
[Installation](#installation)  
[Usage](#usage)  
[Contributing](#contributing)  
[Included Datasets](#included-datasets)  
[Usage in the Small Texts Editor](#usage-in-the-small-texts-editor)  
[License](#license)  
[Disclaimer](#disclaimer)  

  
## <a  id="introduction"></a>Introduction

The primary goal of this project is to find the most robust yet minimal dataset that still maintains the original instruction induction. This is useful for developers who want to leverage ChatGPT to create applications with minimal training data and costs.

This approach was initially developed as part of the Small Texts Editor, a commercial product focused on providing context-aware personalization and human-centered solutions for AI-driven text editing. For more information on the Small Texts Editor, please visit the official website at labdqnt.com.
  
## <a  id="how-it-works"></a>How it works

> Please note that using this method with large datasets might consume a significant amount of tokens when interacting with the ChatGPT API. Therefore, it is essential to use it cautiously and consider the associated costs when processing extensive data.

The method performs the following steps:

1. Extract initial instructions from the original dataset using ChatGPT.
2. Iterate through data points, generating different combinations of the remaining data points, and evaluate them using a brute-force approach.
3. Compare the instructions generated from these subsets to the original instructions to determine the importance of each data point in maintaining the original instructions.
4. Calculate dependency and redundancy to find the best combination among equally minimal datasets.

We utilized two base prompts to interact with ChatGPT:

- For deducing the transformation:  
  `Given the following input/output pairs, determine the transformation rule that turns the input into the output. Provide the result in plain text and be concise: %s`
- For comparing instructions:  
  `Compare these two sets of instructions and indicate if they are equivalent. Provide the result as 'Yes' or 'No', without any additional explanation: %s %s`
  
## <a  id="requirements"></a>Requirements

- Python 3.7+
- openai Python library
- tiktoken Python library
- An OpenAI API key
  
## <a  id="installation"></a>Installation

Clone the repository:

```bash
git clone  https://github.com/caetanominuzzo/instruction-induction-optimization.git
```

Change to the repository directory:

```bash
cd  instruction-induction-optimization
```

Install the required packages:

```bash
pip install  -r  requirements.txt
```

Set your OpenAI API key as an environment variable:

```bash
export  OPENAI_API_KEY='your_api_key_here'
```
  
## <a  id="usage"></a>Usage

Your dataset JSON file should follow this format:

```json
[
  {
    "input": "1",
    "output": "1"
  },
  {
    "input": "1",
    "output": "2"
  },
  {
    "input": "2",
    "output": "3"
  },
  {
    "input": "3",
    "output": "5"
  }
]
```

This example JSON format is taken from the included dataset-example-fibonacci-sequence.json file.
See the `dataset-example-*.json` files for more examples.
Run the main script with the dataset file path as a command-line argument:

```bash
python main.py  /path/to/your/dataset.json
```

Alternatively, you can run the main script without any arguments, and it will prompt you to use the provided example dataset.
  
## <a  id="contributing"></a>Contributing

If you would like to contribute to this project, feel free to submit a pull request or open an issue with your suggestions and bug reports.
  
## <a  id="included-datasets"></a>Included Datasets

This repository includes three example datasets:

1. `dataset-example-multiply-by-two.json` - A dataset containing input/output pairs for multiplying by two.
2. `dataset-example-fibonacci-sequence.json` - A dataset containing input/output pairs for the Fibonacci sequence.
3. `dataset-example-even-triple-odd-add.json` - A dataset containing input/output pairs for a function that triples even numbers and adds one to odd numbers.

Feel free to use these datasets for testing purposes or as a reference for creating your own datasets.
  
## <a  id="usage-in-the-small-texts-editor"></a>Usage in the Small Texts Editor

This method has been successfully integrated into the Small Texts Editor, a state-of-the-art AI-driven text editor that focuses on generating short, contextually relevant text suggestions. The Small Texts Editor uses it to optimize the dataset for instruction induction, allowing it to provide highly personalized suggestions while maintaining a budget-friendly approach.
By leveraging this approach, the Small Texts Editor can deliver high-quality results for various use cases, including:

- Writing precise storytelling prompts for AI image generators, such as Stable Diffusion and Midjourney,
- Crafting engaging Twitter posts,
- Creating catchy slogans.

For more information on the Small Texts Editor and to try it out, please visit the official website at labdqnt.com.

This repository provides the underlying optimization method that powers the Small Texts Editor's dataset optimization feature.
  
## <a  id="disclaimer"></a>Disclaimer

ChatGPT is a product of OpenAI Inc., Midjourney is a product of Midjourney Inc., and Stable Diffusion is a product of StabilityAI. This project is independently developed and is not directly associated with or endorsed by OpenAI, Midjourney, or StabilityAI.
  
## <a  id="license"></a>License

This project is licensed under the GNU Lesser General Public License v3 (LGPL-3). See the [LICENSE](LICENSE) file for details.
