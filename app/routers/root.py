from fastapi import APIRouter
import gradio as gr

from app.api.chatgpt import chat_with_gpt

router = APIRouter()

@router.get("/")
async def read_root():
    return {"Hello": "World"}


with open("app/frontend/styles.css", "r") as file:
    css_styles = file.read()

# Function to reset the state
def reset_state():
    return "", []  # Reset outputs: empty response, empty history, False flag


# Create the Gradio interface
with gr.Blocks(css=css_styles, theme=gr.themes.Default()) as iface:
    # Add Title and Description
    gr.Markdown(
        "<span style='background: linear-gradient(90deg, #7FE786, #58A7FE); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px;'>OnlyBenz Chatbot Assistant</span>"
    )
    gr.Markdown(
        "<p>I am your virtual car dealer assistant specializing in the Mercedes EQ electric car line. Let me help you find the perfect car!</p>"
    )

    with gr.Row():
        with gr.Column():
            user_input = gr.Textbox(placeholder="How can I assist you today?", label="Your message")

            # Create a row for the buttons
            with gr.Row():
                submit_btn = gr.Button("Submit", variant="primary")
                reset_btn = gr.Button("Reset")

        with gr.Column():
            ai_response = gr.Textbox(label="Car Dealer AI")

    # Add Examples Section
    gr.Examples(
        examples=[["Hi! I'm thinking about getting a new car and want to explore electric vehicles."]],
        inputs=user_input,
    )

    state = gr.State([])  # Combined state

    # Button functionality
    submit_btn.click(
        chat_with_gpt,
        inputs=[user_input, state],
        outputs=[ai_response, state]
    )

    reset_btn.click(
        reset_state,
        inputs=[],
        outputs=[ai_response, state]
    )


@router.on_event("startup")
def start_gradio():
    iface.launch(share=True)
