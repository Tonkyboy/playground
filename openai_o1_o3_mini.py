from openai import OpenAI
import time
# pip install openai

client = OpenAI(api_key="paste-your-api-key-here")

# # Function to stream output from a model
# def stream_model_output(model, prompt, reasoning="medium"):
#     stream = client.chat.completions.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": """You are a helpful assistant 
#             skilled in reasoning."""},
#             {"role": "user", "content": prompt}
#         ],
#         stream=True,
#         reasoning_effort=reasoning
#     )
#     for chunk in stream:
#         content = chunk.choices[0].delta.content or ""
#         if content:
#             print(content, end="", flush=True)
# 
# prompt = """Solve this step-by-step: A store has a sale where every item’s price is reduced by 20%. 
# After the sale, the store increases prices by 25% to return to normal. 
# If a shirt originally costs $40, what’s its price after the sale and after the increase? 
# Then, explain why the final price isn’t $40 again."""
# 
# # stream_model_output("o1", prompt, reasoning="high")
# # stream_model_output("o3-mini", prompt, reasoning="low")


# Store chat history
chat_history = [
    {"role": "system", "content": "You are a helpful assistant skilled in reasoning."}
]

# Function to stream output and update history
def stream_model_output(model, prompt, reasoning="medium"):
    global chat_history
    chat_history.append({"role": "user", "content": prompt})
    
    print(f"\n=== {model} (Reasoning Effort: {reasoning}) ===")
    start_time = time.time()
    
    stream = client.chat.completions.create(
        model=model,
        messages=chat_history,
        stream=True,
        reasoning_effort=reasoning
    )
    
    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content or ""
        if content:
            print(content, end="", flush=True)
            response += content
    
    end_time = time.time()
    print(f"\nTime taken: {end_time - start_time:.2f} seconds")
    
    # Add assistant's response to history
    chat_history.append({"role": "assistant", "content": response})

# Interactive chat loop with o3-mini
print("Starting an interactive chat (type 'exit' to stop)...\n")

while True:
    # Get user input
    user_prompt = input("You: ")
    
    # Check for exit condition
    if user_prompt.lower() == "exit":
        break
    
    # Stream response from o3-mini with medium reasoning effort (adjustable)
    stream_model_output("o3-mini", user_prompt, reasoning="low")

# Print the full chat history after the loop ends
print("\n=== Full Chat History ===")
for message in chat_history:
    print(f"{message['role'].capitalize()}: {message['content']}")
