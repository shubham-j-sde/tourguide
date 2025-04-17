import os

import gradio as gr
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from google import genai
from google.genai import types
from io import BytesIO
import base64

load_dotenv()

GEMINI_API_KEY= os.getenv('GEMINI_API_KEY') or os.environ['GEMINI_API_KEY']

client = genai.Client(api_key=GEMINI_API_KEY)

def chat_bot(message, history):
    contents = [message["text"]]
    if message.get("files"):
        for file in message["files"]:
            contents.append(client.files.upload(file=file))
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
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
examples = ["Create a week vacation plan for a young couple to visit Paris, also show some Images",
            "A family trip to Egypt, where to go, show photos"]

with gr.Blocks(title='Tourguide') as tourguide:
    gr.Markdown("""<h1>TourGuide</h1>""")
    gr.Markdown("""<h2>Your one spot to find plan next vacation!</h2>""" )
    chatInf = gr.ChatInterface(fn=chat_bot, type="messages", editable=True, multimodal=True,
                               textbox=chat_input, examples=examples)

if __name__ == "__main__":
    tourguide.launch()
