import json
import os


def load_db_data():
    # Get the directory where the current script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the db_new.json file
    db_path = os.path.join(script_dir, 'db_new.json')

    with open(db_path, 'r') as db_file:
        return json.load(db_file)


def generate_initial_context_hptj():
    task_overview = (
        "Your job is to check the customer's preferences against a list of electric cars provided by the system. "
        "You need to find out if any of the suggested cars match what the customer is looking for."
    )

    verify_match = (
        "1) **Check for a Match:**\n"
        "- A match occurs if the customer has explicitly or implicitly mentioned a car model, and one or more of the "
        "suggested cars meet these criteria."
    )

    handling_matches = (
        "2) **If a Match is Found:**\n"
        "- Replace the placeholder values in the provided JSON template with the actual "
        "name(s) of the matched car(s).\n"
        "- The template will look like this:\n"
        "{\n\"chosenCars\": [\"ACTUAL_CAR_NAME_1\", \"ACTUAL_CAR_NAME_2\", ...],\n\"anyMatches\": true\n}"
    )

    handling_no_matches = (
        "3) **If No Match is Found:**\n"
        "- Set the \"anyMatches\" field in the JSON template to `false`, like this:\n"
        "{\n\"anyMatches\": false\n}"
    )

    initial_context = [
        {"messages": [{"role": "system", "content": task_overview}]},
        {"messages": [{"role": "system", "content": verify_match}]},
        {"messages": [{"role": "system", "content": handling_matches}]},
        {"messages": [{"role": "system", "content": handling_no_matches}]},
    ]

    return initial_context


def generate_initial_context_ndtj():
    db_data = load_db_data()

    model_names = [entry['name'] for entry in db_data]

    dynamic_rules = {
        "name": f"If specified and matches a model name, set the exact value; otherwise, set 'Mercedes'. Allowed names: {model_names}",
        "horsepower": f"Range [{min(entry['horsepower'] for entry in db_data)}-{max(entry['horsepower'] for entry in db_data)}].",
        "consumption": f"Range [{min(entry['consumption'] for entry in db_data)}-{max(entry['consumption'] for entry in db_data)}] W/100km.",
        "range": f"Highway range, Range [{min(entry['range'] for entry in db_data)}-{max(entry['range'] for entry in db_data)}].",
        "size": f"Range [{min(entry['size'] for entry in db_data)}-{max(entry['size'] for entry in db_data)}]. Also can be referred # of seats in a car",
        "chargeTime": f"Range [{min(entry['chargeTime'] for entry in db_data)}-{max(entry['chargeTime'] for entry in db_data)}] minutes.",
        "is4Matic": "Boolean.",
        "budget": f"Range [{min(entry['budget'] for entry in db_data)}-{max(entry['budget'] for entry in db_data)}]."
    }

    task_overview = (
        "Your primary task is to structure and validate data based on user inputs "
        "regarding Mercedes-Benz electric cars. Generate two JSON structures. One "
        "with values extracted from the input, and another with weights that represent "
        "how important each parameter is for the user."
    )

    json_structure_instructions = (
        "The first JSON structure should include the extracted parameters with specific "
        "values. If a value isn't provided, use logical defaults or set them to null. "
        "Follow the given parameter ranges and rules strictly."
    )

    weight_structure_instructions = (
        "The second JSON structure should include weights for each parameter, where 10 "
        "means the user explicitly mentioned and defined the parameter, and lower values "
        "represent lesser importance."
    )

    flag_var_instructions = (
        "Additionally, provide a 'ready' flag in your response, which should be true if "
        "at least 50% of the parameters are set or if the car name matches a specific "
        "list of models."
    )

    output_constraints = (
        "Do not include any extraneous information in your response; only provide the two "
        "JSON structures and the ready flag."
    )

    parameter_rules = "Rules for parameter values:\n" + "\n".join(
        f"- **{key}**: {value}" for key, value in dynamic_rules.items())

    initial_context = [
        {"messages": [{"role": "system", "content": task_overview}]},
        {"messages": [{"role": "system", "content": json_structure_instructions}]},
        {"messages": [{"role": "system", "content": weight_structure_instructions}]},
        {"messages": [{"role": "system", "content": flag_var_instructions}]},
        {"messages": [{"role": "system", "content": output_constraints}]},
        {"messages": [{"role": "system", "content": parameter_rules}]}
    ]
    return initial_context


def prepend_initial_context_to_jsonl(messages, filename):
    # Create a new filename with '_with_initial_context' suffix
    base_name, ext = os.path.splitext(filename)
    new_filename = f"{base_name}_with_initial_context{ext}"

    # Concatenate all system messages into a single string
    full_system_message = ""
    for message in messages:
        full_system_message += message["messages"][0]["content"] + "\n"
    full_system_message = full_system_message.strip()  # Remove trailing newline

    # Read the existing content of the original file
    with open(filename, 'r') as file:
        existing_content = file.readlines()

    # Write the new data to the new file in the current directory
    with open(new_filename, 'w') as new_file:
        for i, line in enumerate(existing_content):
            entry = json.loads(line)

            # Check if an original system message exists
            if entry['messages'][0]['role'] == 'system':
                original_system_message = entry['messages'][0]['content']
                user_message = entry['messages'][1]['content']
                assistant_message = entry['messages'][2]['content']
            else:
                original_system_message = ""
                user_message = entry['messages'][0]['content']
                assistant_message = entry['messages'][1]['content']

            # Combine the full system message with the original system message if it exists
            combined_system_message = full_system_message
            if original_system_message:
                combined_system_message += "\n" + original_system_message
            combined_system_message = combined_system_message.strip()  # Remove any extra newlines

            # Create the combined message
            combined_message = {
                "messages": [
                    {"role": "system", "content": combined_system_message},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": assistant_message}
                ]
            }
            if i < len(existing_content) - 1:
                new_file.write(json.dumps(combined_message) + '\n')
            else:
                new_file.write(json.dumps(combined_message))

    print(f"New file created with initial context: {new_filename}")