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

lore_file_path = os.path.join(current_dir, '../src/lore_context.json')
with open(lore_file_path, 'r') as file:
    lore_context = json.load(file)

load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')
client = Anthropic(api_key=api_key)

async def process_prompt(prompt_text):
    response = client.beta.prompt_caching.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=2000,
        temperature=0.2,
        system=[
            {
                "type": "text",
"text": """ 

You are an AI character advisor for Dungeons & Dragons 5e. Based on the following input, 
INPUT JSON:

{
  "character_creation_questions": [
    {
      "question": "What kind of race do you want?",
      "answer": "I want a weird race!"
    },
    {
      "question": "What class are you interested in?",
      "answer": "I want a class that is not into magic at all"
    },
    {
      "question": "What background do you prefer?",
      "answer": "I want a background that involves being a hero"
    },
    {
      "question": "What alignment do you envision for your character?",
      "answer": "I want my character to be good and generous"
    },
    {
      "question": "What personality traits do you want your character to have?",
      "answer": "I want my character to be friendly, but cautious"
    },
    {
      "question": "What physical appearance do you imagine for your character?",
      "answer": "I want my character to be tall and in good shape, wide shoulders but with a friendly german like face"
    },
    {
      "question": "What kind of backstory do you have in mind?",
      "answer": "I want a backstory involving being the son of a dethroned dinasty"
    },
    {
      "question": "What are your character's goals or motivations?",
      "answer": "I want my character to seek undoing past wrongs"
    },
    {
      "question": "What kind of relationships does your character have?",
      "answer": "I want my character to have a loyal companion"
    },
    {
      "question": "What special abilities or skills do you want your character to possess?",
      "answer": "I want my character to be talented with his body but not the most intelectual, really strong and quick to think but objective and simple"
    },
    {
      "question": "What is your character's name?",
      "answer": "I want my character to be named Frugo"
    },
    {
      "question": "What are your character's ability scores?",
      "answer": "I want high strenght and carisma"
    },
    {
      "question": "What type of weapon do you prefer?",
      "answer": "I want big weapons : )"
    },
    {
      "question": "What is a personal flaw of your character?",
      "answer": "My character is sometimes too simple"
    },
    {
      "question": "Does your character have any strong bonds with others?",
      "answer": "My character has a group of friends, the party members, a cleric, a paladin, a rogue and a bard"
    }
  ]
}

generate suggestions for the character in the format of the OUTPUT JSON in JSON format that strictly 
adheres to the structure of the OUTPUT JSON. Do not deviate from this structure or add any additional fields.
Make sure to pay attention to the character's ability scores. You must only use the base books of Dungeons & Dragons
(Players Handbook, Monster's Manual, Dungeon Master's Guide) and THE BOOK OF EVERYTHING to generate the output.
You must pay strict attention to output the 'new elements' added to the BOOK OF EVERYTHING. If you need to create anything
for the players backstory that is not in the BOOK OF EVERYTHING, you must say that you created it inside "new elements".
Each of the topics in "new elements" can have many records. for example:

            "added locations": [
                [
                    "The Shadowmarket",
                    "A secret, ever-moving marketplace in the lower levels of the Shimmering Citadel where thieves, fences, and other criminals gather to trade stolen goods and information."
                ],
                [
                    "The Crystal Dungeons",
                    "A high-security prison in the Shimmering Citadel, where magical crystals suppress the abilities of inmates and create illusions to disorient escape attempts."
                ],

                .... following...

                [
                     "The Whispering Alley",
                     "A hidden street in the lower levels of the Shimmering Citadel, known only to the criminal underworld. It's a marketplace for illegal goods and a hub for planning heists and other illicit activities."
                ]

            ]

Following there will be the output model:

OUTPUT JSON EXAMPLE:

{
  "character sugestion1": {
    "explanation": "explain here why you choose the following sugestions, and make a small brief of the character, no more than 4 sentences.",
    "name": "Character Name",
    "alignment": "alignment",
    "class": "Class sugestion1",
    "subclass": "Subclass sugestion1",
    "race": "race sugestion1",
    "subrace": "subrace sugestion1",
    "background": "background sugestion1",
    "skills": [
        "insight",
        "arcane",
        "nature",
        "skills that reflect the character's ability scores choosen in the input"
    ],
    "proficiencies": [
        "heavy armor",
        "martial weapons"
    ],
    "languages": [
        "abissal",
        "comum"
    ],
    "spells": [
        "fireball", "wish"
    ],
    "items": [
      "druidic pouch",
      "diamond", 
      "great axe" 
    ],
    "character Lore": "create a descriptive and contextualized with THE BOOK OF EVERYTHING character lore, at least one paragraph and at max 2 paragraphs",
    "personality trais": "description of the personality",
    "bonds": "create an inventive story speaking in detail about the bonds of the character. Create emotional and touching stories relating THE BOOK OF EVERYTHING and the ideas the JSON input had",
    "goals": "description of goals",
    "flaw": "description of flaw",
    "new elements": {
        "added events": [
            [
                "Name of the event,
                "A brief of the event created now."
            ]
        ],
        "added items": [
            [
                "item name",
                "a brief of the item created now."
            ]
        ],
        "added NPC": [
            [
                "NPC name",
                "a brief of the NPC created now."
            ]
        ],
        "added locations": [
            [
                "locations name",
                "a brief of the locations created now."
            ]
        ]
    },
    "description": "description of appearance with details"
  }
}

Based on this information, please generate an output containing suggestions for the D&D character in the OUTPUT JSON format. 
You must not change the name of any fields nor add fields in the structure of the OUTPUT. 

The output must be exactly in the OUTPUT JSON format, just change the content stored in each field of the json to fit the 
ideais contained in the user input while also relating it to the BOOK OF EVERYTHING. Creating a characther that fits in the world based 
on the player input. Ensure that the output generated is in the structure of the OUTPUT JSON  and includes all relevant details from the 
input while fitting within the context of the BOOK OF EVERYTHING. 

YOU MUST NOT SAY ANYTHING; the output must be ONLY and nothing more than the JSON.
""",

"cache_control": {"type": "ephemeral"},
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
        response = await process_prompt(message)
        await websocket.send(response)

start_server = websockets.serve(handler, "localhost", 8767)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
