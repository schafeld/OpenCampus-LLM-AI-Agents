# https://huggingface.co/learn/agents-course/unit1/dummy-agent-library
# Note: client.text_generation didn't work for the suggested model, so we use client.chat_completion instead.

# pip install python-dotenv
# pip install huggingface_hub

import os
import json
import re
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

# print("Client initialized successfully. \n")

location = "Rome"  # Default location for weather information

SYSTEM_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

get_weather: Get the current weather in a given location

The way you use the tools is by specifying a json blob.
Specifically, this json should have an `action` key (with the name of the tool to use) and an `action_input` key (with the input to the tool going here).

The only values that should be in the "action" field are:
get_weather: Get the current weather in a given location, args: {"location": {"type": "string"}}
example use :

{{
  "action": "get_weather",
  "action_input": {"location": " """ + "{{location}}" + """ }
}}


ALWAYS use the following format:

Question: the input question you must answer
Thought: you should always think about one action to take. Only one action at a time in this format:
Action:

$JSON_BLOB (inside markdown cell)

Observation: the result of the action. This Observation is unique, complete, and the source of truth.
... (this Thought/Action/Observation can repeat N times, you should take several steps when needed. The $JSON_BLOB must be formatted as markdown and only use a SINGLE action at a time.)

You must always end your output with the following format:

Thought: I now know the final answer
Final Answer: the final answer to the original input question

Now begin! Reminder to ALWAYS use the exact characters `Final Answer:` when you provide a definitive answer. """


# Dummy function to simulate getting weather information
def get_weather(location):
    return f"The weather in {location} is sunny with 22°C."


def extract_action_from_response(response):
    """Extract JSON action from the model response"""
    # Look for JSON blocks in markdown
    json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(json_pattern, response, re.DOTALL)
    
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    # Fallback: look for JSON-like structure without markdown
    json_pattern = r'\{[^}]*"action"[^}]*\}'
    matches = re.findall(json_pattern, response, re.DOTALL)
    
    if matches:
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass
    
    return None


def execute_action(action_json):
    """Execute the requested action"""
    if action_json["action"] == "get_weather":
        location = action_json["action_input"]["location"]
        return get_weather(location)
    else:
        return f"Unknown action: {action_json['action']}"


def generate_response(prompt, max_iterations=5):
    conversation = prompt
    
    for i in range(max_iterations):
        messages = [
           {"role": "system", "content": SYSTEM_PROMPT},
           {"role": "user", "content": conversation}
        ]
        
        response = client.chat_completion(
            messages=messages,
            temperature=0.7,
            top_p=0.9,
            max_tokens=1024,
            stream=False,
            stop=["Observation:"] # Prevent the model from hallucinating a result, we want to use the (mocked) get_weather function to get the result
        )
        
        model_response = response.choices[0].message.content
        print(f"Model response (iteration {i+1}):")
        print(model_response)
        print("-" * 50, "\n\n")
        
        # Check if we have a final answer
        if "Final Answer:" in model_response:
            # Extract only the final answer part
            final_answer_start = model_response.find("Final Answer:")
            # final_answer = model_response[final_answer_start + len("Final Answer:"):].strip()
            # Final answer should be everything after "Final Answer:" including Final Answer:
            final_answer = model_response[final_answer_start:].strip()
            return final_answer
        
        # Extract and execute action
        action_json = extract_action_from_response(model_response)
        if action_json:
            observation = execute_action(action_json)
            conversation += model_response + f"\nObservation: {observation}\n"
            print(f"Observation: {observation}")
            print("-" * 50, "\n\n")
        else:
            # If no action found, return the response as is
            return model_response
    
    return "Maximum iterations reached without final answer."


# Example usage
if __name__ == "__main__":
    prompt = f"What is the weather in {location}?"
    print("Prompt:", prompt)
    print("Generating response... \n\n")
    response = generate_response(prompt)
    # print("\nFinal Response:")
    print(response)
