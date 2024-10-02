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

json_file_path = os.path.join(current_dir, '../src/QnA.json')
with open(json_file_path, 'r') as file:
    # Load the JSON data
    data = json.load(file)

current_dir = os.path.dirname(__file__)
lore_file_path = os.path.join(current_dir, '../src/lore_context.json')
with open(lore_file_path, 'r') as file:
    # Load the JSON data
    lore_context = json.load(file)

# Load variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')
client = Anthropic(api_key=api_key)

async def process_prompt(prompt_text):
    response = client.beta.prompt_caching.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        system=[
            {
                "type": "text",
"text": """ 

You are an AI character generator for Dungeons & Dragons 5e. Based on the following input, create a detailed character sheet in JSON format that includes the character's race, class, background, alignment, ability scores, personality traits, physical appearance, backstory, goals, relationships, skills, weapons, flaws, bonds, and character name. 

Here are the example inputs from the player:
INPUT JSON:
{
  "character_creation_questions": [
    {
      "question": "What kind of race do you want?",
      "answer": "I want a small and cute race"
    },
    {
      "question": "What class are you interested in?",
      "answer": "I want a class that is good at magic"
    },
    {
      "question": "What background do you prefer?",
      "answer": "I want a background that involves adventure and exploration"
    },
    {
      "question": "What alignment do you envision for your character?",
      "answer": "I want my character to be chaotic and free-spirited"
    },
    {
      "question": "What personality traits do you want your character to have?",
      "answer": "I want my character to be friendly and curious"
    },
    {
      "question": "What physical appearance do you imagine for your character?",
      "answer": "I want my character to be tall with bright red hair"
    },
    {
      "question": "What kind of backstory do you have in mind?",
      "answer": "I want a backstory involving a lost family heirloom"
    },
    {
      "question": "What are your character's goals or motivations?",
      "answer": "I want my character to seek revenge for a past wrong"
    },
    {
      "question": "What kind of relationships does your character have?",
      "answer": "I want my character to have a loyal companion"
    },
    {
      "question": "What special abilities or skills do you want your character to possess?",
      "answer": "I want my character to be skilled in archery"
    },
    {
      "question": "What is your character's name?",
      "answer": "I want my character to be named Elara"
    },
    {
      "question": "What are your character's ability scores?",
      "answer": "I want high Dexterity and Charisma"
    },
    {
      "question": "What type of weapon do you prefer?",
      "answer": "I want a bow and arrows"
    },
    {
      "question": "What is a personal flaw of your character?",
      "answer": "My character is overly trusting"
    },
    {
      "question": "Does your character have any strong bonds with others?",
      "answer": "My character has a mentor they look up to"
    }
  ]
}

Based on this information, please generate a well-organized D&D character sheet in JSON format, following this structure:

OUTPUT JSON:
{
  "Character": {
    "name": "Elara",
    "level": 1,
    "alignment": "Chaotic Good",
    "background": "Explorer",
    "maxLife": 10,
    "actualLife": 10,
    "attributes": {
      "strength": 8,
      "dexterity": 16,
      "constitution": 12,
      "intelligence": 10,
      "wisdom": 10,
      "charisma": 18,
      "proficiency": 2,
      "initiative": 3
    },
    "inventory": {
      "items": [
        {
          "name": "Bow",
          "weight": 2,
          "description": "A sturdy longbow."
        },
        {
          "name": "Arrows",
          "weight": 1,
          "description": "A quiver of arrows."
        }
      ]
    },
    "proficiencies": {
      "others": ["Archery", "Magic"]
    }
  },
  "Bard": {
    "skill": "Archery",
    "multiClass": false,
    "cantripsKnown": 2,
    "spellsKnown": 4,
    "spellSlots": [2, 0, 0, 0, 0, 0, 0, 0, 0],
    "bardicInspirationDie": 6
  },
  "Lore": {},
  "Valor": {},
  "Spells": {
    "spellName": "",
    "spellEffect": "",
    "multiClass": false
  },
  "Flaws": [
    "Overly trusting"
  ],
  "Bonds": [
    "Mentor"
  ],
  "Goals": [
    "Seek revenge for a past wrong",
    "Recover lost family heirloom"
  ]
}

Ensure that the generated JSON is well-organized and includes all relevant details from the input while fitting within the context of the BOOK OF EVERYTHING.

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
