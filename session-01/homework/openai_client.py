# pip install openai
from openai import OpenAI
# replace the random example string with your own key, take care not to share this file with others - otherwise they can use your ressoures

openai_api_key = "< Enter your OpenAI API key here >"

client = OpenAI(api_key = openai_api_key)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": "Write a one-sentence bedtime story about a unicorn."
        }
    ]
)

print(completion.choices[0].message.content)