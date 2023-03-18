import openai
import os
from flask import Flask, request, render_template
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'your-secret-key'
csrf = CSRFProtect(app)

openai.api_key = "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"

messages = [{"role": "system", "content": "You are a financial expert that specializes in real estate investment and negotiation"}]

class InputForm(FlaskForm):
    user_input = StringField('Your question:')
    submit = SubmitField('Submit')

def CustomChatGPT(user_input):
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
        response = CustomChatGPT(user_input)
    return render_template('index.html', form=form, response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 80)))
