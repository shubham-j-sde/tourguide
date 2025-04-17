# tourguide
Gemini Flash 2.0 based Chat-Image bot to help you plan your next vacation conveniently. 

## Installation

Clone th repository from 

```
git clone https://github.com/shubham-j-sde/tourguide.git
cd tourguide
```

Prerequisite: Gradio requires Python 3.10 or higher.

We recommend installing Gradio using pip, which is included by default in Python. Run this in your terminal or command prompt:


`pip install --upgrade gradio`

> Tip: It is best to install Gradio in a virtual environment. Detailed installation instructions for all common operating systems are provided [here](https://www.gradio.app/main/guides/installing-gradio-in-a-virtual-environment).
 
## Run Application

### Setup `GEMINI_API_KEY` 
The application will automatically fetch if present as system environment variable. to check run `echo GEMINI_API_KEY`
if it returns an empty string, set it in [.env](/.env) file.


Run `python app.py` from the terminal at root of repository.

The demo below will open in a browser on http://localhost:7860.

## 

## Using Application



Tourguide all supports the following audio format MIME types:

WAV - audio/wav
MP3 - audio/mp3
AIFF - audio/aiff
AAC - audio/aac
OGG Vorbis - audio/ogg
FLAC - audio/flac

