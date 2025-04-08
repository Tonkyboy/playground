from openai import OpenAI
import json
from tavily import TavilyClient
# pip install tavily-python

OPENAI_API_KEY = "your-api-key-here"
TAVILY_API_KEY = "your-api-key-here"

def initialize_agent(api_key):
    return OpenAI(api_key=api_key)

def search_web(query, api_key, max_results=3):
    try:
        tavily_client = TavilyClient(api_key=api_key)
        response = tavily_client.search(query=query, topic="news", search_depth="advanced", time_range="day")
        results = response.get("results", [])[:max_results]
        return "\n".join([result["content"] for result in results]) if results else "No relevant content found."
    except Exception as e:
        return f"Web search failed: {str(e)}"

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information on a given topic",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "The search query"}},
                "required": ["query"]
            }
        }
    }
]

def blog_post_agent(api_key, web_api_key, topic, output_file="blog_draft.txt", model="gpt-4o", word_count="200-300"):
    if not topic.strip():
        raise ValueError("Topic cannot be empty.")
    
    client = initialize_agent(api_key)
    
    # Research
    research_prompt = f"Research the topic '{topic}' and gather key information for a blog post."
    research_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": research_prompt}],
        tools=tools,
        tool_choice="auto"
    )
    
    research_content = ""
    if research_response.choices[0].message.tool_calls:
        for tool_call in research_response.choices[0].message.tool_calls:
            if tool_call.function.name == "search_web":
                query = json.loads(tool_call.function.arguments)["query"]
                research_content += search_web(query, web_api_key) + "\n"
    else:
        research_content = research_response.choices[0].message.content
    
    # Draft
    draft_prompt = (
        f"Using this research: '{research_content}', write a short blog post ({word_count} words) "
        f"about '{topic}'. Include an engaging intro, key points, and a conclusion."
    )
    draft_response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": draft_prompt}]
    )
    blog_draft = draft_response.choices[0].message.content
    
    # Save
    with open(output_file, "w") as file:
        file.write(blog_draft)
    
    return f"Blog post drafted and saved to '{output_file}'. Content:\n\n{blog_draft}"

if __name__ == "__main__":
    topic = "sustainable python coding trends"
    result = blog_post_agent(OPENAI_API_KEY, TAVILY_API_KEY, topic)
    print(result)
