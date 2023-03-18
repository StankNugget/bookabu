import openai
from flask import Flask, request, jsonify

app = Flask(__name__)
openai.api_key = "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"

messages = [{"role": "system", "content": "You are a financial expert that specializes in real estate investment and negotiation"}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('user_input', '')
    if not user_input:
        return jsonify({"error": "Please provide user input."}), 400
    response = CustomChatGPT(user_input)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
