# client.py
from flask import Flask, render_template, request
import asyncio
import websockets

app = Flask(__name__)

async def send_message(uri, prompt_text):
    async with websockets.connect(uri) as websocket:
        await websocket.send(prompt_text)
        response = await websocket.recv()
        return response

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/single-question', methods=['POST'])
def single_question():
    prompt_text = request.form['prompt']
    response = asyncio.run(send_message('ws://localhost:8765', prompt_text))
    return render_template('index.html', single_prompt=prompt_text, single_response=response)

@app.route('/chat', methods=['POST'])
def chat():
    prompt_text = request.form['prompt']
    response = asyncio.run(send_message('ws://localhost:8766', prompt_text))
    return render_template('index.html', chat_prompt=prompt_text, chat_response=response)

@app.route('/new-chat', methods=['POST'])  # New endpoint for the additional chat
def new_chat():
    prompt_text = request.form['prompt']
    response = asyncio.run(send_message('ws://localhost:8767', prompt_text))
    return render_template('index.html', new_chat_prompt=prompt_text, new_chat_response=response)

if __name__ == '__main__':
    app.run(debug=True)
