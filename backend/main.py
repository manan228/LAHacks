# import flast module
from flask_cors import CORS
from flask import Flask, request
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
from PIL import Image
import io
genai.configure(api_key="AIzaSyDUIy8e6M5KTS348R1rQFWabw1KtYExXx4")
# instance of flask application
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
 
# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

@app.route("/upload", methods=['POST'])
def uploadPhoto():
    # img = PIL.Image.open('image.jpg')
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        # Read the uploaded image
        img = Image.open(io.BytesIO(file.read()))

        # Use Generative AI to generate information about the image
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(["Give detailed information about the image.", img], stream=True)
        response.resolve()
        formatted_response = to_markdown(response.text)
        print(formatted_response.data)
        return {
            "data": formatted_response.data
        }
 
if __name__ == '__main__':  
   app.run()