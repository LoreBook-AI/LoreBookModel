from flask import Flask, render_template, request
import asyncio
import websockets

app = Flask(__name__)

async def send_message(prompt_text):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(prompt_text)
        response = await websocket.recv()
        return response

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt_text = request.form['prompt']
        response = asyncio.run(send_message(prompt_text))
        return render_template('index.html', prompt=prompt_text, response=response)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
