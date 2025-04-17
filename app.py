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


def getDesc(name):
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents="describe " + name + " in a sentence and generate a related image",
        config=types.GenerateContentConfig(
            response_modalities=['Text', 'Image']
        )
    )
    desc = ''
    image = Image.open('static/imageErrorTemplate.webp')
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            desc = part.text
        elif part.inline_data is not None:
            image = Image.open(BytesIO((part.inline_data.data)))
    return desc, image



def chat_bot(message, history):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=message,
        config=types.GenerateContentConfig(
            response_modalities=['Text']
        )
    )
    return response.text


# places = client.models.generate_content(
#     model="gemini-2.0-flash",
#     contents=["list me 2 tourist places with in 1 line each to visit in "+ name +
#               (" for a group of" + (f" {men} men " if men>0 else "") + (f" {women} women " if women>0 else "") + (f" {kids} kids " if kids>0 else "") + (f" {other} lgbtq members " if other>0 else "") if (men or women or kids or other) else "")
#               + (f" going on a {category} trip" if category else "")]
# )
#
# return desc, places.text, image


def on_click():
    desc, img = getDesc(str(place.value))
    gr.Image(img)

background_images = ['https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExYWxnbzk3b3EzMDlqNWh6ZjY2MXdiZjV6MHdvbmkwZ3FmZHFiYXF5aiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/xCSmYQlc6jFW2q6t8e/giphy.gif',
                     'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWtramF5amwwZm55YWxzbGNoNGJkNDFzcDB6cGh6NXRqMHE3cmE0NiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AwcsYcx6k8GhFpcWaO/giphy.gif',
                     'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXB3ZXN2dHg5NTRnczdjeWIxd3RuN2dianlmNWxrZGlwbHNkZnUxbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/5YbQYuAnMfNkUU6GpT/giphy.gif',
                     'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ29xNmFpbHZobGZiYTEzbjdjcW0yMmRyYjU5aHl2b2EyNWljc21ybCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/NPXU8zJgkHa9BqilG1/giphy.gif',
                     'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTNlYWNnNjBkYnZidzc3d3Ixc29zYmgweXJwcDZhMTdyazh6cDVzdyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/YRPfpvlaHIBErZ3Z0O/giphy.gif',
                     'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExYmZyaWg5MWN0d2s2czJiOHcxcDQyZnd0dWNwZWRpeXUycDd2b2ZtbSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l41lNrIXNwTs0PWPm/giphy.gif',
                     'https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExcGV6Z2llbzBpc3R2cW4wbmxpcm0zcTZnZG1leTJpcWZ3cDkxM24zMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/t8n9fhtUuWfxO0XiSp/giphy.gif',
                     'https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmQ4aTY5a3F2cjc5Nmlpb2g2bnFuN3V3cTVmZTR1a2hxZXFlaXAyYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/XybCiflA321nKfACZK/giphy.gif'
                     ]

with gr.Blocks(title='Tourguide') as demo:
    chat_vis = False
    gr.Markdown("""<h1>TourGuide</h1>""")
    gr.Markdown("""<h2>Your one spot to find plan next vacation!</h2>""", visible= not chat_vis)
    place = gr.Textbox(visible=not chat_vis)
    inputPrompt = gr.Textbox(lines=3, label="Custom Text Prompt", interactive=True, show_copy_button=True, visible= not chat_vis)
    radio = gr.Radio(label="Travelling Alone?", choices=['alone', 'group'], value='alone', visible=not chat_vis)
    @gr.render(inputs=[radio])
    def group(choice, input_text=str(inputPrompt.value)):
        if choice=='group':
            with gr.Row(equal_height=True, visible= not chat_vis):
                count = ''
                for e in ['Men', 'Women', 'Kids', 'Other']:
                    ec = gr.Number(label=f'{e}', value=None, minimum=0)
                    if ec:
                        count += f"{ec} {e}"
                input_text += " travelling in a group of " + count
                days = gr.Number(label='Number of Days', value=None, minimum=1)
                input_text += f" for {days} number of days"
        prompt = f"Help me with tour plan to visit {str(place.value)}"
        gr.ChatInterface(fn=chat_bot, type="messages", examples=[prompt], fill_height=True)


if __name__ == "__main__":
    demo.launch()
