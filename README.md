# OnlyBenz ChatBot

## Overview

**OnlyBenz** is a chatbot designed to help users find their dream electric Mercedes-Benz car. During the conversation, the chatbot recognizes and remembers user preferences, analyzes them, and provides a list of cars from the database that match the user's criteria. Each car listed includes a link to the configurator for further customization. The chatbot is highly customizable, allowing companies to easily adjust its behavior. The fine-tuning process for the model is automated, making it simple to optimize the chatbot's performance for specific needs.

### Key Features:

- **Preference Recognition**: The chatbot remembers user preferences throughout the conversation.
- **Personalized Recommendations**: Based on user input, it suggests electric Mercedes-Benz cars that fit the user's criteria.
- **Easy Configuration Access**: Provides a link to the car configurator for further customization.
- **Customizable Behavior**: Companies can fine-tune the chatbot's behavior using an automated process, making it adaptable to various use cases.
- **Automated Fine-Tuning**: Easily refine the chatbot's responses and behavior with automated model tuning.

## How to Launch the Project and Test It

To launch the OnlyBenz project on your local machine, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/OnlyBenz
   cd OnlyBenz
   ```

2. **Set Up the Project**:
   - Run the `setup_project.sh` script to set up the environment, install dependencies, and prepare the database:
   ```bash
   chmod +x setup_project.sh 
   ./setup_project.sh
   ```

3. **Add Your OpenAI API Key**:
   - Before running the project, add your OpenAI API key to the configuration file `config/settings.json` on line 15.

4. **Run the Project**:
   - Use the `run_project.sh` script to start the chatbot server:
   ```bash
   chmod +x run_project.sh 
   ./run_project.sh
   ```

5. **Testing and Customization**:
   - To change the initial context of the chatbot, go to `app/utils.py` and edit the `generate_initial_context_ndtj` function.
   - To modify the training data, edit the file `app/fine_tuning/natural_data_to_json_training_set.jsonl`.

6. **Fine-Tuning**:
   - After making changes to the training data or initial context, open the Jupyter notebook at `app/fine_tuning/natural_data_to_json.ipynb`.
   - Run all the snippets in the notebook one by one.
   - Update the file ID in `In [3]` with the value from `Out [2]`.
   - Update the model ID at line 28 in the file `app/api/gpt_datastructured` with the value from `Out [3]`.

## Background of OnlyBenz

The OnlyBenz project was created at the TUM.ai Makathon 2024 in Munich. I was responsible for implementing the natural language to JSON mapping part, as well as fine-tuning the models used in the chatbot. After the Hackathon, I refined the project further to improve its functionality and usability. You can view our initial project, including contributions from other participants, at the following link: [Automatch Assistant on Devpost](https://devpost.com/software/automatch-assistant?ref_content=user-portfolio&ref_feature=in_progress).
