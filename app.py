import openai
import flask
import logging
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

app = flask.Flask(__name__)

logging.basicConfig(level=logging.INFO)

@app.route("/", methods=["GET", "POST"])

def generate_description():
    try:
        input_text = flask.request.form.get("input_text")

        if input_text:

            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": f"Give me 2 line Quotes and 10 Hashtags for an Instagram post for the following text:\n{input_text}\n\nThe description should be no more than 100 characters."}
            ]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", 
                messages=messages,
                temperature=0.7,
                max_tokens=100,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )
            description = response["choices"][0]["message"]["content"]
        else:
            description = "Please enter some text to generate a description for."

        return flask.render_template("index.html", input_text=input_text, description=description)
    except Exception as e:
        logging.error(f"Error generating description: {e}")
        return flask.render_template("index.html", input_text=None, description="Error generating description.")
    
if __name__ == "__main__":
    app.run(debug=True)