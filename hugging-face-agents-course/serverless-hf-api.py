# https://huggingface.co/learn/agents-course/unit1/dummy-agent-library
# Note: client.text_generation didn't work for the suggested model, so we use client.chat_completion instead.

# pip install python-dotenv
# pip install huggingface_hub

import os
from huggingface_hub import InferenceClient

from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/Projekte/MOOC/OpenCampus/codespace/.env"))

## You need a token from https://hf.co/settings/tokens, ensure that you select 'read' as the token type. If you run this on Google Colab, you can set it up in the "settings" tab under "secrets". Make sure to call it "HF_TOKEN"
# os.environ["HF_TOKEN"]="hf_xxxxxxxxxxxxxx"
if not os.environ.get("HF_TOKEN"):
  # os.environ["HF_TOKEN"] = getpass.getpass("Enter API key for Hugging Face: ")
  raise EnvironmentError("HF_TOKEN not found in the .env file.")

client = InferenceClient("meta-llama/Llama-3.3-70B-Instruct")
# if the outputs for next cells are wrong, the free model may be overloaded. You can also use this public endpoint that contains Llama-3.2-3B-Instruct
# client = InferenceClient("https://jc26mwg228mkj8dw.us-east-1.aws.endpoints.huggingface.cloud")

print("Client initialized successfully.")

def generate_response(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat_completion(
        messages=messages,
        temperature=0.7,
        top_p=0.9,
        max_tokens=1024,
        stream=False,
    )
    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    prompt = "The capital of France is"
    response = generate_response(prompt)
    print("Response:", response)

