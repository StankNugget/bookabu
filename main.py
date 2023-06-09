import openai
import os
import markdown
import logging
from flask import Flask, request, render_template, Markup
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY")
csrf = CSRFProtect(app)

logging.basicConfig(level=logging.DEBUG)

openai.api_key = os.environ.get('OPENAI_API_KEY')

def init_conversation():
    return [{"role": "system", "content": "You are a real estate guru. refrain from referring to yourself in any instance"}]

messages = init_conversation()

class InputForm(FlaskForm):
    user_input = StringField('Your question:')
    submit = SubmitField('Submit')

def CustomChatGPT(user_input):
    global messages
    messages = init_conversation()
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

@app.route('/', methods=['GET', 'POST'])
def index():
    form = InputForm()
    response = None
    if form.validate_on_submit():
        user_input = form.user_input.data
        response_text = CustomChatGPT(user_input)
        response = Markup(markdown.markdown(response_text))  # Convert the response to HTML using markdown
    return render_template('index.html', form=form, response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
