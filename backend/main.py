# import flast module
from flask_cors import CORS
from flask import Flask, request
import google.generativeai as genai
from IPython.display import Markdown
import textwrap
from PIL import Image
import io
import torch

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
genai.configure(api_key="AIzaSyDUIy8e6M5KTS348R1rQFWabw1KtYExXx4")
loaded_model = torch.load('model.pth', map_location=device)

from transformers import AutoTokenizer, AutoModelForCausalLM

# USE_CPU = False
# device = "xpu:0" if torch.xpu.is_available() else "cpu"
# if USE_CPU:
#     device = "cpu"
# print(f"using device: {device}")

model_id = "google/gemma-2b"
tokenizer = AutoTokenizer.from_pretrained(model_id)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"


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
        print("Request received")
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
        response = to_markdown(response.text).data
        print("Got response from gemini")
        # print(response)
        print("Running custom model")
        # for text in test_inputs:
        inputs = tokenizer(response, return_tensors="pt").to(device)
        print("feeding inputs")
        outputs = loaded_model.generate(**inputs, max_new_tokens=100, 
                                do_sample=False, top_k=50, 
                                eos_token_id=tokenizer.eos_token_id)
        print(tokenizer.decode(outputs[0], skip_special_tokens=True))
        return {
            "data": response
        }
    return "Not allowed"
 
if __name__ == '__main__':  
   app.run()