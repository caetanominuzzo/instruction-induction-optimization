# Transforming AI Text Editors: Context-Aware Personalization and Human-Centered Solutions

Large language models (LLMs) have become increasingly popular in text editors. However, users often encounter issues such as generic suggestions, lack of customization, expensive token costs, and the complexity of instructing AI with examples.

The Small Texts Editor addresses these challenges by integrating user-specific examples into AI prompts, offering contextually relevant, personalized suggestions at an affordable cost, while catering to users' emotional and cognitive needs.


## LLM Challenge: Cost vs. Context

Fine-tuning LLMs can be expensive, and creating detailed chat prompts with examples to guide the AI is often time-consuming and costly. The Small Texts Editor addresses these challenges with a unique approach.


## Combining Few-Shot Learning & Instruction Induction

Few-shot learning refers to the ability of a model to quickly adapt to new tasks or situations with a limited amount of training data or examples.

For example, if the model is given a small dataset of input/output pairs for a task we could define as ```even numbers triple, odd numbers add 2``` task, like: ```{[1, 3], [2, 6], [3, 5], [4, 12]}``` it can quickly learn the underlying transformation rule and generate relevant output for new inputs.

In the context of the Small Texts Editor, few-shot learning allows the model to learn from a small number of user-specific examples and generate relevant suggestions that align with the user's preferences and writing styles.

Instruction induction is the process of extracting and inferring underlying instructions or rules from a given set of examples. For instance, given a dataset with the same input/output pairs above, the AI can deduce the rule 'even numbers triple, odd numbers add 2' and use it to generate new input values.

The Small Texts Editor utilizes OpenAI's GPT-3.5-turbo and few-shot learning, learning new tasks with limited data, typically between 5 to 20 examples. Incorporating user-specific examples into the AI prompt enhances alignment with user preferences and writing styles. By substituting original items in the sample set with user-inputted ones, the AI retains its Instruction Induction, that is, its capacity to describe the process of suggestions.

Please note that the above dataset is a simplistic example to illustrate the process. When the editor uses this technique, the input/output pairs are user texts and AI-powered suggestions.

By combining these technologies the AI effectively adapts to new tasks with very limited data. This combination of relevant user examples with a curated dataset enables the AI to deliver tailored and affordable suggestions.


## Introducing The Small Texts Editor

Designed for brief texts like tweets, catchy slogans, small emails - or precise AI prompts for image generation - The Small Texts Editor merges user examples and concentrates on texts fewer than 64 words. This approach provides relevant, context-sensitive suggestions while remaining budget-friendly and enhancing the overall writing experience.

The Small Texts Editor utilizes OpenAI's ChatGPT API, but please note that this project is independently developed and not directly associated with OpenAI.

While 64 words may not be enough for everyone, understanding the social media landscape, where short, catchy texts are prevalent, highlights the relevance of the Small Texts Editor.


## Future Development

As we continuously enhance our editor and expand it over larger texts use cases, our focus remains on adapting to the users' multiple writing styles and catering to the needs of the readers. We strive to create a comprehensive writing solution that benefits both the writer and the audience, ensuring impactful communication.

Experience context-sensitive writing assistance tailored to your unique style with The Small Texts Editor. Elevate your writing to new heights and embrace the future of AI-driven text editing. Try the Small Texts Editor now!

## References:

1. Dong, Q., Li, L., Dai, D., Zheng, C., Wu, Z., Chang, B., Sun, X., Xu, J., Li, L., & Sui, Z. (2023). A Survey on In-context Learning. arXiv preprint arXiv:2301.00234. Retrieved from https://arxiv.org/abs/2301.00234

2. Honovich, O., Shaham, U., Bowman, S. R., & Levy, O. (2022). Instruction Induction: From Few Examples to Natural Language Task Descriptions. arXiv preprint arXiv:2205.10782. Retrieved from https://arxiv.org/abs/2205.10782
