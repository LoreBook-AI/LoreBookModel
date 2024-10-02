import asyncio
import websockets
import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic


# Load variables from .env file
load_dotenv()

current_dir = os.path.dirname(__file__)
lore_file_path = os.path.join(current_dir, '../src/lore_context.json')
with open(lore_file_path, 'r') as file:
    # Load the JSON data
    lore_context = json.load(file)

# Access the API key
api_key = os.getenv('API_KEY')
client = Anthropic(api_key=api_key)

# Initialize conversation history
conversation_history = []

async def process_prompt(prompt_text):
    # Append user message to the conversation history
    conversation_history.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": prompt_text,
            }
        ]
    })
    
    response = client.beta.prompt_caching.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=500,
        system=[
            {
                "type": "text",
                "text": """You are a mystical storyteller for Dungeons and Dragons. In this conversation, you will only respond based on the lore of Aethoria and in the rules of Dungeons and Dragons fifth edition. If you do not know the answer based on the lore provided, you must state that the information is not available in Aethoria. If a question pertains to topics outside this realm, such as programming languages or concepts not found in Aethoria, you should say that such things do not exist. For example, if asked about 'JavaScript,' your response should indicate that you have never heard of it before. All answers must strictly relate to the magical and fantastical elements of the Realm of Aethoria as described in the lore provided.
                
Act as a narrator or a citizen of Aethoria, and remain ignorant of any matters that would not exist in Aethoria. Always cite the source of your information. For example: 'The Ashen Wastes is a place without life, as described in the Book of Everything: "Wait till you hear about the Ashen Wastes. Picture a vast expanse of gray, lifeless land..."' If you do not have a specific source to cite, simply state that the information is not known within Aethoria. Do not create or assume information beyond what is provided.""",
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": lore_context['text'],
                "cache_control": {"type": "ephemeral"}
            },
        ],
        messages=conversation_history
    )
    assistant_response = response.content[0].text

    # Append assistant response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    return assistant_response

async def handler(websocket, path):
    async for message in websocket:
        response = await process_prompt(message)
        await websocket.send(response)

start_server = websockets.serve(handler, "localhost", 8766)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
