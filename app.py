import os
import json
from flask import Flask, render_template, request, jsonify, Response, stream_with_context
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
app = Flask(__name__)

client = InferenceClient(api_key=os.getenv("HF_TOKEN"), provider="groq")

SYSTEM_PROMPT = """You are AnchorAI, a warm and calm crisis companion. Help people through stress and anxiety. Use the 5-4-3-2-1 grounding technique personalised to what you see in their environment. Never diagnose. Always encourage professional help. Speak in short calm sentences."""

conversation_history = []
user_schedule = ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/schedule', methods=['POST'])
def set_schedule():
    global user_schedule
    user_schedule = request.json.get('schedule', '')
    return jsonify({'status': 'Schedule saved'})

@app.route('/api/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.json
    user_message = data.get('message', '')
    image_data = data.get('image', None)

    schedule_context = f"\n\nUser schedule today: {user_schedule}" if user_schedule else ""
    environment_context = "\n\nThe user has their camera on. Ask them to describe one object they can see near you and use it in your grounding exercise." if image_data else ""
    system = SYSTEM_PROMPT + schedule_context + environment_context

    conversation_history.append({"role": "user", "content": user_message})

    messages = [{"role": "system", "content": system}]
    for msg in conversation_history[-10:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    def generate():
        full_response = ""
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct",
            messages=messages,
            max_tokens=500,
            stream=True
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                token = chunk.choices[0].delta.content
                full_response += token
                yield f"data: {json.dumps({'token': token})}\n\n"
        
        conversation_history.append({"role": "assistant", "content": full_response})
        yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(stream_with_context(generate()), mimetype='text/event-stream')

@app.route('/api/report', methods=['POST'])
def generate_report():
    if not conversation_history:
        return jsonify({'report': 'No session data.'})

    history_text = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in conversation_history])
    
    messages = [
        {"role": "system", "content": "You are a clinical psychologist writing structured session reports."},
        {"role": "user", "content": f"Generate a therapist report with these sections:\n1. Session Summary\n2. Emotional Arc\n3. Triggers Identified\n4. Techniques Used\n5. Recommended Next Steps\n\nSESSION TRANSCRIPT:\n{history_text}"}
    ]
    
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        messages=messages,
        max_tokens=800
    )
    
    return jsonify({'report': response.choices[0].message.content})

@app.route('/api/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'Reset'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
