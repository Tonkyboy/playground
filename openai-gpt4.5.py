from openai import OpenAI, APIError, AuthenticationError
# pip3 install openai

client = OpenAI(
    api_key="paste-your-API-key-here",
)

prompt = input("\nUser: ")

while True:
  try:   
      stream = client.chat.completions.create(
          model="gpt-4.5-preview",
          messages=[
          {"role": "system", "content": "Act like a personal assistant."},
          {"role": "user", "content": prompt}
          ],
          temperature=0.7,
          max_tokens=100,
          stream=True
      )
  
      if stream:    
          print("Response: ", end="", flush=True)
          for chunk in stream:
              if chunk.choices[0].delta.content:
                  print(chunk.choices[0].delta.content, end="", flush=True)
          
  except AuthenticationError:
      print("Authentication failed - check your API key")
  except APIError as e:
      print(f"API error: {e}")
  except Exception as e:
      print(f"Unexpected error: {e}")

# https://platform.openai.com/settings/
# https://platform.openai.com/docs/models
# https://platform.openai.com/settings/organization/api-keys
# https://platform.openai.com/settings/organization/billing/overview
# https://platform.openai.com/settings/organization/usage?startDate=2025-02-13&endDate=2025-02-28
