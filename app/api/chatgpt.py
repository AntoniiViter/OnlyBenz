import json
import traceback

from openai import OpenAI

from app.api.gpt_datastructured import generate_description
from app.api.gpt_wrap_up import generate_wrapup
from app.preprocess import matchCars, get_matching_names, get_links

# Load CSS styles from styles.css


# Define the initial context for ChatGPT acting as a knowledgeable car dealer for Mercedes EQ cars
initial_context = ("You are a knowledgeable car dealer for Mercedes-Benz, specializing in cars. Your goal is to guide "
                   "customers in choosing the best car for their needs, emphasizing the benefits of electric cars. "
                   "And you need to suggest EQ Mercedes cars to the users, as if it is really the best line of cars "
                   "suiting them. An you must be friendly. And before suggesting any car models you need to know what "
                   "size of the car the user want, for what does he need a car, will he use it for riding to work or "
                   "for anything else, and only when you have enough data you can make an assumption about the best "
                   "suitting car. And when a user says he wants to buy any car that is not electric, try to convice "
                   "him of buying an electric car")


def extract_user_inputs(history):
    user_inputs = [message['content'] for message in history if message['role'] == 'user']
    return '. '.join(user_inputs)


# Function to craft a message list for the API call
def create_message_list(history, user_input):
    # Check if the initial context is already in history
    if not any(message.get("role") == "system" and message.get("content") == initial_context for message in history):
        message_list = [{"role": "system", "content": initial_context}]
    else:
        message_list = []

    message_list.extend(history)
    message_list.append({"role": "user", "content": user_input})
    return message_list


# Function that manages the conversation
def chat_with_gpt(user_input, state):
    if not state:
        state = [[], []]

    # Retrieve current state
    with open('config/settings.json', 'r') as config_file:
        config = json.load(config_file)
    response = ""
    response_from_chat = False
    is_obtained_link = False

    client = OpenAI(api_key=config['openAI_api']['key'])
    
    # Create the list of messages for the API call
    messages = create_message_list(state[0], user_input)

    # time.sleep(0.05)
    print(extract_user_inputs(messages))
    description = generate_description(extract_user_inputs(messages))
    print(description)
    try:
        if state[1]:
            check_link = generate_wrapup(user_input, state[1])
        
            print("check_link->")
            print(check_link)

            state[1] = []
            json_resp = json.loads(check_link)
            if not (json_resp.get('anyMatches') is None) and not (json_resp.get('chosenCars') is None):
                print("A link coms")
                print(json_resp)
                if json_resp.get('anyMatches'):
                    response = get_links(json_resp.get('chosenCars'))
                    is_obtained_link = True

        if not is_obtained_link:
            json_resp = json.loads(description)

            possible_names = ("EQE 350", "EQE 500", "EQE 43", "EQS 450", "EQS 500", "EQS 580", "EQS 53", "EQA 250", "EQA 300",
                              "EQA 350", "EQB 250", "EQB 300", "EQB 350", "EQT 200", "EQV 250", "G-Klasse", "Maybach", "EQS 450",
                              "EQS 500", "EQS 580", "EQE 300", "EQE 350", "EQE 500", "EQE 43", "EQS 450")
            if len(response) == 0:
                if not (json_resp.get('configuration') is None) and not (json_resp.get('weights') is None) and not (json_resp.get('ready') is None):
                    if json_resp.get('ready'):
                        name_to_extract = ""
                        print("good")
                        if json_resp.get('configuration').get('name') is not None:
                            for name in possible_names:
                                if name in json_resp.get('configuration').get('name'):
                                    name_to_extract = name
                        if len(name_to_extract) == 0:
                            tmp = matchCars(json_resp.get('weights'), json_resp.get('configuration'))
                            response = str(tmp[0])
                            state[1] = tmp[1]
                        else:
                            tmp = get_matching_names(name_to_extract)
                            response = str(tmp[0])
                            state[1] = tmp[1]
                    else:
                        response_from_chat = True
                else:
                    response_from_chat = True
    except Exception:
        print(traceback.format_exc())
        print("JSON exception")
        response_from_chat = True

        # Call the OpenAI API with the conversation history
    print("response_from_chat: " + str(response_from_chat))
    if response_from_chat:
        response = client.chat.completions.create(
            model="gpt-4",
            temperature=1,
            messages=messages
        )

        # Extract the assistant's message from the response
        response = response.choices[0].message.content

    if is_obtained_link:
        response_gpt = client.chat.completions.create(
            model="gpt-4",
            temperature=1,
            messages=messages
        )

        # Extract the assistant's message from the response
        response = response_gpt.choices[0].message.content + "\n" + response

    # Update conversation history
    state[0].append({"role": "user", "content": user_input})
    state[0].append({"role": "assistant", "content": response})
    print(state[0])

    # If a recommendation is made, append a URL to the configurator. This is a placeholder logic.
    if "recommendation" in response.lower():
        response += ("\nYou can configure your Mercedes EQ car here: [Mercedes EQ Configurator]("
                     "https://www.mercedes-benz.com/en/vehicles/configurator/#/main/car)")

    return response, state


