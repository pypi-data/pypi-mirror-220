# Jam.AI

Jam is an experimental collaboration tool to use multiple AI personnel together equipped with instructed function calls.

> Create Jam session with AI

[View Changelog](https://github.com/abhishtagatya/jam/blob/master/CHANGELOG.md)

![Demo](https://raw.githubusercontent.com/abhishtagatya/jam/master/docs/demo.png)

## Quick Start

```python
from jam import Jam
from jam.personnel import BasicPersonnel, AutoPersonnel
from jam.instrument import PromptPainter

jam_room = Jam(
    members=[
        BasicPersonnel.from_json(filepath='example/personnel/claude-monet.json'),  # Using custom JSON
        BasicPersonnel.from_preset(name='pablo-picasso'),  # Using example presets from Git
        AutoPersonnel.from_prompt(uid='wkandinsky', prompt='Wassily Kandinsky')  # Using GPT to build prompt
    ],
    instruments=[PromptPainter()]
)

prompt = jam_room.compose(
    message='who are you!',
    multi=True
)

print(prompt) # List of Prompts from Characters

```

Don't forget to use your credentials. Primarily for OpenAI, the core engine of this project. 
https://platform.openai.com/account/api-keys

```bash
export OPENAI_KEY=YOUR_KEY
```

## Installation

```bash
pip install jam-ai --upgrade
```
You need to use Pip to install jam. Conda package is currently unavailable.

### Requirements
* Python >= 3.8
* OpenAI
* Requests
* Pillow

Extra Requirements for Function Calls
* Psycopg2
* PyMySQL
* Stability SDK

### Extension

Optional dependencies to fit any requirement needed.

```bash
pip install jam-ai[database] # Using Postgres, MySQL, Redis ...
pip install jam-ai[function] # Using Extended Function Calls requiring SDKs / Packages
```

For the use of other libraries, please consider to always feed in your API Keys respectively. See below for example.

```bash
export STABILITY_KEY=YOUR_STABILITY_AI_KEY # If you are using Stability SDK
export WRITESONIC_KEY=YOUR_WRITE_SONIC_KEY # If you are using WriteSonic API
export CUSTOM_KEY=YOUR_CUSTOM_KEY          # If there are any other added functionalities
```


## Author
* Abhishta Gatya ([Email](mailto:abhishtagatya@yahoo.com)) - Software and Machine Learning Engineer
