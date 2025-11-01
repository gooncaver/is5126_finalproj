from langchain.agents import create_agent
from dotenv import load_dotenv, find_dotenv
import os
import requests
import json

# Load environment variables from a .env file
dotenv_path = find_dotenv()

# 2. load_dotenv() takes that path and loads the variables into os.environ.
load_dotenv(dotenv_path)

# Verification
print(f"Loaded .env from path: {dotenv_path}")
print(f"Key loaded: {bool(os.getenv('OPENAI_API_KEY'))}")

# FastAPI endpoint URL
FASTAPI_URL = "http://localhost:8000/predict"

# Create a tool that calls the FastAPI endpoint
def predict_number_of_children(gender: str, Q217: bool, Q281: bool) -> str:
    """
    Predict the number of children based on the given parameters.
    Calls the FastAPI service at localhost:8000/predict
    
    Args:
        gender: Gender of the person ('male' or 'female')
        Q217: WVS feature Q217 (boolean)
        Q281: WVS feature Q281 (boolean)
    
    Returns:
        String with prediction and interpretation
    """
    try:
        # Prepare request payload
        payload = {
            "gender": gender,
            "Q217": Q217,
            "Q281": Q281
        }
        
        # Call FastAPI endpoint
        response = requests.post(FASTAPI_URL, json=payload, timeout=5)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Format response for the agent
        predicted = result["predicted_children"]
        ci = result["confidence_interval"]
        drivers = result["drivers"]
        
        # Build interpretation string
        interpretation = f"Predicted children: {predicted} (95% CI: [{ci[0]}, {ci[1]}])\n"
        interpretation += "\nKey drivers:\n"
        for driver in drivers:
            interpretation += f"- {driver['name']}: {driver['interpretation']}\n"
        
        return interpretation
        
    except requests.exceptions.ConnectionError:
        return "Error: FastAPI server not running. Start it with: python fastapi.py"
    except requests.exceptions.Timeout:
        return "Error: API request timed out"
    except Exception as e:
        return f"Error calling prediction API: {str(e)}"

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