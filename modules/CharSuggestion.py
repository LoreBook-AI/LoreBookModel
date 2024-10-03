import asyncio
import websockets
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic

import json
import os

# Get the path to the current directory (where file.py is located)
current_dir = os.path.dirname(__file__)

json_file_path = os.path.join(current_dir, '../src/input.json')
with open(json_file_path, 'r') as file:
    input_json = json.load(file)

json_file_path = os.path.join(current_dir, '../src/output.json')
with open(json_file_path, 'r') as file:
    output_json = json.load(file)

lore_file_path = os.path.join(current_dir, '../src/lore_context.json')
with open(lore_file_path, 'r') as file:
    lore_context = json.load(file)

# Load variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')
client = Anthropic(api_key=api_key)

async def process_prompt(prompt_text):
    response = client.beta.prompt_caching.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        system=[
            {
                "type": "text",
"text": """ 

You are an AI character generator for Dungeons & Dragons 5e. Based on the following input, create a detailed character sheet in JSON format that includes the character's race, class, background, alignment, ability scores, personality traits, physical appearance, backstory, goals, relationships, skills, weapons, flaws, bonds, and character name. 

Here are the example inputs from the player:
INPUT JSON:
{input_json}

Based on this information, please generate a well-organized D&D character sheet in JSON format, following this structure:

OUTPUT JSON:
{output_json}

Ensure that the generated JSON is well-organized and includes all relevant details from the input while fitting within the context of the BOOK OF EVERYTHING. YOU MUST NOT SAY ANYTHING the output must be ONLY and nothing more than the JSON

"""
            },
            {
                "type": "text",
                "text": lore_context['text'],
                "cache_control": {"type": "ephemeral"},
            },
        ],
        messages=[{"role": "user", "content": prompt_text}],
    )

    print(response)
    return response.content[0].text

async def handler(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        response = await process_prompt(message)
        await websocket.send(response)
        print(f"Sent response: {response}")

start_server = websockets.serve(handler, "localhost", 8767)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
