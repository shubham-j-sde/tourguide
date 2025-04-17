import os

import gradio as gr
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from google import genai
from google.genai import types
from io import BytesIO

load_dotenv()

GEMINI_API_KEY= os.getenv('GEMINI_API_KEY') or os.environ['GEMINI_API_KEY']

client = genai.Client(api_key=GEMINI_API_KEY)

def chat_bot(message, history, system_prompt, model, max_output_tokens, temperature, top_p, top_k, stop_sequences):
    print(system_prompt)
    response_modalities = ['Text', 'Image'] if model=="gemini-2.0-flash-exp-image-generation" else ['Text']
    contents = [message["text"]]
    if message.get("files"):
        for file in message["files"]:
            contents.append(client.files.upload(file=file))
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            max_output_tokens=max_output_tokens,
            temperature=temperature,
            stop_sequences=stop_sequences.split("###")[:5],
            top_p=top_p,
            top_k=top_k,
            response_modalities=response_modalities
        )
    )
    result = []
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            result.append(part.text)
        elif part.inline_data is not None:
            result.append(gr.Image(Image.open(BytesIO(part.inline_data.data))))
    return result

sample_prompt = "Help me plan a tour to visit /Paris. I am traveling in a group of /x bachelors for /weekend."

chat_input = gr.MultimodalTextbox(interactive=True,
                                  file_count="multiple",
                                  value=sample_prompt,
                                  placeholder="Enter message or upload file...",
                                  show_label=False,
                                  sources=["microphone", "upload"])
models = ["gemini-2.0-flash-exp-image-generation", "gemini-2.5-flash-preview","gemini-2.0-flash" ,"gemini-1.5-flash","gemini-1.5-pro"]

additional_inputs=[
        gr.Textbox(value="Gemini based Chatbot", label="System message"),
        gr.Radio(choices=models,value="gemini-2.0-flash-exp-image-generation", label="Model"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max Output tokens"),
        gr.Slider(minimum=0.2, maximum=2.0, value=1.0, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
        gr.Slider(
            minimum=1,
            maximum=40,
            value=32,
            step=1,
            label="Top-k (nucleus sampling)",
        ),
        gr.Textbox(value="", label="Stop Sequences", placeholder="Input the desired set of character list concatenated with '###' e.g. ['apple', 'mango'] as 'apple###mango'"),
    ]
examples = [["Create a week vacation plan for a young couple to visit Paris","example-1", "gemini-2.0-flash", 800, 1.0, 0.95, 32, "field"],
            ["A family trip to Egypt, where to go, show photos","example-2", "gemini-2.0-flash-exp-image-generation", 1200, 0.5, 0.95, 40, "weather"]]

with gr.Blocks(title='Tourguide') as demo:
    gr.Markdown("""<h1>TourGuide</h1>""")
    gr.Markdown("""<h2>Your one spot to find plan next vacation!</h2>""" )
    chatInf = gr.ChatInterface(fn=chat_bot, type="messages", editable=True, multimodal=True,
                               textbox=chat_input, examples=examples, additional_inputs=additional_inputs)

if __name__ == "__main__":
    demo.launch()
