# main.py

import google.generativeai as genai

# pip install -q -U google-generativeai

model = genai.GenerativeModel('gemini-pro')

GOOGLE_API_KEY="your-key-here"
genai.configure(api_key=GOOGLE_API_KEY)

def prompt():
    input="How are you doing today?"
    response = model.generate_content(input)
    print(response.text)
    return response

# https://ai.google.dev/tutorials/python_quickstart

if __name__ == "__main__":
    prompt()
