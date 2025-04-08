import requests
import os
import json
from datasets import load_dataset

# API endpoint and headers
API_URL = "https://api.intelligence.io.solutions/api/v1/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('IOINTELLIGENCE_API_KEY')}"    

}

# Models to evaluate
MODELS = [
    "meta-llama/Llama-3.3-70B-Instruct",
    "deepseek-ai/DeepSeek-R1"
]

# Datasets to use
DATASETS = {
    # "HumanEval": {"path": "openai_humaneval", "extra": {},"split": "test"},
    "ARC": {"path": "ai2_arc", "extra": {'name': 'ARC-Challenge'},"split": "test"},
    "TruthfulQA": {"path": "truthful_qa", "extra": {'name': 'multiple_choice'},"split": "validation"},
}

def extract_selected_choices(choices, labels):
    """
    Extracts elements from the 'choices' list where the corresponding index in 'labels' is 1.

    Args:
        choices (list of str): List of choice strings.
        labels (list of int): List of binary labels (0 or 1).

    Returns:
        list of str: List of choices corresponding to label 1.
    """
    return [choice for choice, label in zip(choices, labels) if label == 1]

def call_model(model, prompt):
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=600)
    response_data = response.json()
    return response_data.get("choices", [{}])[0].get("message", {}).get("content", "")

def evaluate_model_on_dataset(model, dataset_name, dataset):
    correct = 0
    total = 0

    for example in dataset.select(range(1)):  # Limiting to 10 examples for demonstration
        if dataset_name == "HumanEval":
            prompt = example['prompt']
            expected_output = example['test']  # Assuming 'test' contains the expected output
            response = call_model(model, prompt)
            # Here, you would execute the response as code and compare the output
            # For demonstration, we'll assume a function `execute_code` exists
            try:
                exec_globals = {}
                exec(response, {}, exec_globals)
                result = exec_globals.get('result', None)
                if result == expected_output:
                    correct += 1
            except Exception as e:
                pass  # Handle execution errors

        elif dataset_name == "ARC":
            prompt = example['question'] + "\nOptions: " + ", ".join(example['choices']['text'])
            correct_answer = example['answerKey']
            response = call_model(model, prompt)
            if response.strip() == correct_answer.strip():
                correct += 1

        elif dataset_name == "TruthfulQA":
            prompt = example['question']
            correct_answer = extract_selected_choices(example['mc1_targets']['choices'], example['mc1_targets']['labels'])
            response = call_model(model, prompt)
            # Use a similarity metric or classifier to assess truthfulness
            # For demonstration, we'll use a placeholder function `assess_truthfulness`
            if assess_truthfulness(response, correct_answer):
                correct += 1

        total += 1

    accuracy = correct / total if total > 0 else 0
    print(f"Model: {model} | Dataset: {dataset_name} | Accuracy: {accuracy:.2%}")
    return accuracy, response,correct_answer

def assess_truthfulness(response, true_answers):
    # Placeholder for a function that assesses the truthfulness of the response
    # This could involve similarity metrics or a classifier like GPT-judge
    return response.strip().lower() in [ans.strip().lower() for ans in true_answers]

def main():
    all_results = []
    for dataset_name, dataset_info in DATASETS.items():
        dataset = load_dataset(dataset_info["path"], split=dataset_info["split"], **dataset_info.get("extra", {}))
        print(f"Loaded {dataset_name} dataset with {len(dataset)} examples.")
        for model in MODELS:
            accuracy, iomodel_response,correct_answer = evaluate_model_on_dataset(model, dataset_name, dataset)
            all_results.append({
                "model": model,
                "dataset": dataset_name,
                "accuracy": accuracy,
                "iomodel_response": iomodel_response,
                "correct_answer": correct_answer
            })

    with open("evaluation_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

if __name__ == "__main__":
    main()
