from langchain.agents import create_agent
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables from a .env file
dotenv_path = find_dotenv()

# 2. load_dotenv() takes that path and loads the variables into os.environ.
load_dotenv(dotenv_path)

# Verification
print(f"Loaded .env from path: {dotenv_path}")
print(f"Key loaded: {bool(os.getenv('OPENAI_API_KEY'))}")

# Create a tool that returns a single value
def predict_number_of_children(gender: str, Q217: bool, Q281: bool) -> int:
    """
    Predict the number of children based on the given parameters.
    Dummy function to test agent integration.
    """
    return 1

agent = create_agent(
    model="gpt-5",
    tools=[predict_number_of_children],
    system_prompt="You are a helpful for predicting number of children based on model parameters.",
)

# Run the agent
output = agent.invoke(
    {"messages": [{"role": "user", "content": "I am male, Q217 is True, Q281 is False. How many children will I have?"}]}
)

# Print all messages in the conversation
print("\n=== Full Conversation ===")
for i, msg in enumerate(output['messages']):
    print(f"\nMessage {i}: {type(msg).__name__}")
    if hasattr(msg, 'content'):
        print(f"Content: {msg.content}")
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        print(f"Tool Calls: {msg.tool_calls}")
    if hasattr(msg, 'name'):
        print(f"Tool Name: {msg.name}")

# Extract specific messages
print("\n=== Tool Message ===")
tool_message = [msg for msg in output['messages'] if type(msg).__name__ == 'ToolMessage'][0]
print(f"Tool returned: {tool_message.content}")

print("\n=== Final AI Response ===")
final_ai_message = [msg for msg in output['messages'] if type(msg).__name__ == 'AIMessage'][-1]
print(f"AI says: {final_ai_message.content}")