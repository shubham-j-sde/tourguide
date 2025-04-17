# Tourguide

<!--TOC-->
* [Tourguide](#tourguide)
  * [Installation](#installation)
  * [Run Application](#run-application)
    * [Gemini Setup](#setup-gemini_api_key-)
  * [User Guide](#user-guide)
  * [Development](#development)
<!--TOC-->

Tourguide is a not simply a Chatbot, it supports Text/ Image and Audio prompts for all supported Google Gemini models which defaults to Gemini-2.0 Flash Image Generation allowing custom configuration parameters.
You can ask Gemini to plan your next vacation, may be book tickets or even carry you there...

Application is live on Huggingface space : [shubhamjsde/tourguide](https://huggingface.co/spaces/shubhamjsde/tourguide)

> It's important to keep your Gemini API key secure. Thus, it is recommended to run your app locally following instructions below.
> For some general best practices, you can also review this [support article.](https://support.google.com/googleapi/answer/6310037)

## Installation

Clone the repository

```
git clone https://github.com/shubham-j-sde/tourguide.git
cd tourguide
```

Prerequisite: Gradio requires Python 3.10 or higher. If you do not have it installed, you can download it from [python.org](https://www.python.org/).

We recommend installing Gradio and other requirements using pip (which is included by default in Python) in a virtual environment.

```commandline
python -m venv gradio-env
source gradio-env/bin/activate
pip install -r requirements.txt
```
If you are running on Windows, use `.\gradio-env\Scripts\activate` instead of the `source` command.

## Run Application

### Setup `GEMINI_API_KEY` 
The application will automatically fetch `GEMINI_API_KEY` if present as system environment variable. to check this run `echo GEMINI_API_KEY` in your terminal.
if it returns an empty string, set it in [.env](./.env) file.


Run `python app.py` from the terminal at root of repository.

The application below will launch in a browser on http://localhost:7860.

## User Guide

Give a custom text/ image or audio file as prompt for Gemini Chatbot.

Tourguide supports using varied Gemini Models by selecting desired in Additional Inputs, along with other [Configuration Parameters](https://ai.google.dev/gemini-api/docs/text-generation#configuration-parameters) supported by Gemini

Supported [Gemini Models](https://ai.google.dev/gemini-api/docs/models):
- Gemini 2.5 Flash Preview
- Gemini 2.0 Flash Image Generation
- Gemini 2.0 Flash
- Gemini 1.5 Flash
- Gemini 1.5 Pro


Supported Custom [Configuration Parameters](https://ai.google.dev/gemini-api/docs/text-generation#configuration-parameters):
- Max Output tokes
- Temperature
- topP
- topK
- Stop Sequences

Tourguide application supports all image/audio format MIME types supported by Gemini:

[Image:](https://ai.google.dev/gemini-api/docs/image-understanding#supported-formats)

- PNG - image/png
- JPEG - image/jpeg
- WEBP - image/webp
- HEIC - image/heic
- HEIF - image/heif

[Audio:](https://ai.google.dev/gemini-api/docs/audio#supported-formats)

- WAV - audio/wav
- MP3 - audio/mp3
- AIFF - audio/aiff
- AAC - audio/aac
- OGG Vorbis - audio/ogg
- FLAC - audio/flac

## Development

Run `gradio app.py` in root of your repository to run Gradio in <b>hot reload mode</b>, learn more [here](https://www.gradio.app/guides/developing-faster-with-reload-mode).

If your desired Gemini Model is not in the list, add in the [main](./app.py) file.