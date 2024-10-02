import asyncio
import websockets
import os
from dotenv import load_dotenv
from anthropic import Anthropic

# Load variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv('API_KEY')
client = Anthropic(api_key=api_key)

lore_context = """
THE BOOK OF EVERYTHING:
Gather 'round, adventurers, and let me spin you a tale of the Realm of Aethoria, a world where magic flows like rivers and technology soars on the winds of innovation. It's a place of wonder and danger, of ancient mysteries and new discoveries waiting to be made.

Let's start with the jewel of the skies, the Shimmering Citadel. Imagine a city of crystal spires and golden domes, floating serenely above the clouds. It's a marvel of magical engineering, held aloft by a combination of ancient ley lines and cutting-edge levitation tech. The streets are paved with luminescent stones that glow softly at night, and fountains of light dance in the squares. 

Queen Lyra Stormborn rules from the Heart of Tempests, a palace at the city's center where storms rage eternally, contained within magical barriers. They say she can pluck lightning from the air and weave it into spells of devastating power. But for all her might, she's got her hands full keeping the peace and fending off those blasted sky pirates.

Speaking of which, let me tell you about the most notorious of these aerial brigands - Captain Zephyr the Windwalker. He's a legend among both criminals and commoners, known for his daring heists and Robin Hood-like generosity. His ship, the Stormchaser, is said to be faster than the wind itself, able to outrun even the Queen's elite skyguard.

Now, if you're more of a landlubber, you might find yourself wandering into the Whispering Woods. But let me warn you, it's not your ordinary forest. The trees there are old, older than memory, and they've got a consciousness all their own. They whisper secrets to each other in a language of rustling leaves and creaking branches. 

The elves who dwell there, led by Eldrin Moonwhisper, are as mysterious as the woods themselves. They're masters of nature magic, able to shape living wood and communicate with plants and animals. But lately, they've got their hands full with this Whispering Plague. It starts with losing your voice, then your skin starts to roughen like bark, and before you know it, you're putting down roots literally!

But if you think that's weird, wait till you hear about the Ashen Wastes. Picture a vast expanse of gray, lifeless land, where the ground crunches like charcoal under your feet and the air tastes of old magic gone sour. It wasn't always like this, mind you. A thousand years ago, it was a thriving kingdom called Solaria, renowned for its sun magic.

That all changed with the Sundering. No one knows exactly what happened, but in a single day and night, Solaria was reduced to ash and the continent was split into floating islands. Some say it was a spell gone wrong, others blame a vengeful god. Whatever the cause, it left behind a wasteland teeming with mutated creatures and echoes of past power.

One man who calls this desolate place home is Grimlock the Ashen. He's a warlock of fearsome repute, said to have made pacts with entities from beyond the veil of reality. He's always on the hunt for artifacts from Solaria's glory days, convinced that the key to ultimate power lies hidden in the ashes.

Now, if you prefer your adventures with a splash of saltwater, there's always the Coral Kingdom. Beneath the waves lies a realm of breathtaking beauty and deadly intrigue. The merfolk who dwell there have built a civilization in and around giant coral structures, their cities glowing with bioluminescent light.

Captain Mira Coralhart is the realm's fiercest protector, commanding a fleet of living ships grown from enchanted coral. She led the Coral Rebellion a decade ago, fighting for the rights of the common merfolk against the oppressive nobility. The rebellion was successful, but tensions still simmer beneath the surface.

But land, sea, and sky aren't the only realms in Aethoria. There's also the Ethereal Plane, a dimension that overlaps with our own. Most can't perceive it, but those with the Sight can see the spirits and elementals that inhabit this ghostly realm. The boundaries between planes grow thin during the Great Convergence, leading to all sorts of magical mayhem.

Speaking of which, we're due for another Convergence any day now. It happens every 500 years when the moons align and magic surges throughout the realm. New species have been born, islands have appeared out of thin air, and in one case, an entire city vanished, only to reappear 50 years later not a day older. Who knows what'll happen this time?

If you're looking to prepare for the Convergence, you might want to seek out the Clockwork Oracle in the Shimmering Citadel. It's a bizarre contraption of gears and crystals, tended to by the enigmatic Keepers of the Cog. The Oracle spouts prophecies in riddles and rhymes, and while they're often cryptic, they've never been wrong.

For those of you with a thirst for knowledge, don't miss the Great Library of Aetherium, suspended between realities in a pocket dimension. It's said to contain every book ever written and some that have yet to be. The Librarians are a secretive bunch, masters of chronomancy who can step between moments in time.

Now, if you're feeling really adventurous, you could try scaling Mount Skyhammer. It's the tallest peak in Aethoria, its summit forever shrouded in storm clouds. Legend has it that the gods forged the world on its peak, and their ancient forge still burns at the heart of the eternal storm. Many have tried to reach the top, lured by promises of godly artifacts, but none have returned to tell the tale.

Lastly, let me tell you about the Nexus Points. These are spots where the ley lines of Aethoria intersect, creating wells of pure magical energy. They're unpredictable and dangerous, causing wild surges of magic that can reshape reality itself. The most powerful mages in the realm study these Nexus Points, hoping to unlock their secrets and harness their power.

So, brave souls, where do you fit into this tapestry of wonder and peril? Are you a sky-born noble from the Shimmering Citadel, or perhaps a reformed sky pirate looking for redemption? Maybe you're an elven tree-whisperer from the Whispering Woods, racing to find a cure for the plague? Or a treasure hunter braving the dangers of the Ashen Wastes? 

Perhaps you're a merfolk rebel from the Coral Kingdom, fighting for equality beneath the waves? Or an ethereal-touched seer, blessed (or cursed) with visions of the spirit realm? You could be a chronomancer from the Great Library, safeguarding the knowledge of ages, or a bold explorer determined to uncover the secrets of Mount Skyhammer.

Whoever you are, whatever your story, know this: in Aethoria, every tale is one of magic, of courage, of discovery. So tell me, adventurer, what's your story?
"""

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
                "text": lore_context,
                "cache_control": {"type": "ephemeral"}
            },
        ],
        messages=conversation_history
    )
    print(response)
    assistant_response = response.content[0].text

    # Append assistant response to the conversation history
    conversation_history.append({
        "role": "assistant",
        "content": assistant_response
    })
    print(conversation_history)
    return assistant_response

async def handler(websocket, path):
    async for message in websocket:
        response = await process_prompt(message)
        await websocket.send(response)

start_server = websockets.serve(handler, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
