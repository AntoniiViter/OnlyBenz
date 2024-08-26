from openai import OpenAI
from app.utils import generate_initial_context_ndtj
import json


def generate_description(raw_message):
    # Setting up OpenAI API key
    with open('config/settings.json', 'r') as config_file:
        config = json.load(config_file)

    client = OpenAI(api_key=config['openAI_api']['key'])

    # Prepare the input message
    messages = generate_initial_context_ndtj()

    full_system_message = ""
    for message in messages:
        full_system_message += message["messages"][0]["content"] + "\n"
    full_system_message = full_system_message.strip()  # Remove trailing newline

    messages = [
        {"role": "system", "content": full_system_message},
        {"role": "user", "content": f"{raw_message}"},
    ]

    # Generate a response using the fine-tuned model
    completion = client.chat.completions.create(
        model="ft:gpt-4o-mini-2024-07-18:personal::9y66brQq",
        messages=messages,
        temperature=1,  # You can adjust the temperature for creativity
        max_tokens=250,  # Adjust the max tokens based on the expected response length
    )

    # Extract and return the generated reply
    reply = completion.choices[0].message.content
    return reply



