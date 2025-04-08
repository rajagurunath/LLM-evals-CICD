from datasets import load_dataset
from evaluate import load
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
from tqdm import tqdm

# Load HumanEval dataset
human_eval = load_dataset("openai_humaneval")['test']

# Load code evaluation metric
code_eval_metric = load("code_eval")


for problem in tqdm(human_eval, desc="Problems", unit="problem"):
    prompt = problem['prompt']
    test_code = problem['test']
    # print(problem)
    print("prompt:",prompt)
    print("======================================================")
    # print(test_code)
    print("======================================================")


# # Compute pass@k
# k_values = [1, 5]
# print("Evaluating generated code...")
# pass_at_k, results = code_eval_metric.compute(
#     references=test_cases,
#     predictions=candidates,
#     k=k_values,
#     num_workers=4,  # Adjust based on your system
#     timeout=10.0,   # Adjust the timeout as needed
# )

# # Print the results
# for k in k_values:
#     print(f"Pass@{k}: {pass_at_k[f'pass@{k}'] * 100:.2f}%")